from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from django.http import JsonResponse
from .serializers import UploadSerializer
from .tasks import upload_users, get_users, update_user, upload_users_json
import json


class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer

    def list(self, request):
        first_name = request.query_params.get("first_name", None)
        last_name = request.query_params.get("last_name", None)
        national_id = request.query_params.get("national_id", None)
        country = request.query_params.get("country", None)
        birth_date = request.query_params.get("birth_date", None)
        phone_number = request.query_params.get("phone_number", None)
        email = request.query_params.get("email", None)

        users = get_users.delay(
            pk=None,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            national_id=national_id,
            country=country,
            birth_date=birth_date,
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
            except CreateCustomerException as ce:
                raise ce
        else:
            res = upload_users_json.delay(req_data)

        res.get(propagate=True)

        if res.successful():
            return JsonResponse({"message": "users succesfully created in the db"})
        else:
            raise CreateCustomerException("Error occured while creating users")


class CreateCustomerException(Exception):
    def __init__(self, message):
        super().__init__(message)
