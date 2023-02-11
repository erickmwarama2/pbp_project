from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import UploadSerializer
from .tasks import upload_users, get_users, update_user, upload_users_json
import json


class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        users = get_users.delay(
            request.query_params.get("search", None),
            request.query_params.get("order", None),
        )
        response = users.get(propagate=True)
        return JsonResponse(response, safe=False)

    def retrieve(self, request, pk=None):
        user = get_users.delay(pk)
        response = user.get(propagate=True)
        return JsonResponse(response)

    def update(self, request, pk=None):
        res = update_user.delay(pk, request.body)
        return res.get(propagate=True)

    def create(self, request):
        file_uploaded = None
        req_body = request.body
        req_data = request.data
        if "file" in request.FILES:
            file_uploaded = request.FILES["file"]
            content_type = file_uploaded.content_type
            try:
                if content_type == "text/csv":
                    file_data = file_uploaded.read().decode("utf-8").strip().split("\n")
                    res = upload_users.delay(file_data)
                else:
                    res = upload_users.delay(req_body)
            except Exception:
                raise Exception("Exception occured while fetching users")
        else:
            res = upload_users_json.delay(req_data)

        res.get(propagate=True)

        if res.successful():
            return JsonResponse({"message": "users succesfully created in the db"})
        else:
            raise Exception("Error occured while creating users")
