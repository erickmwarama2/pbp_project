from rest_framework.viewsets import ViewSet
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.http import JsonResponse
from .serializers import UploadSerializer
from .tasks import (
    upload_customers,
    get_customers,
    update_customer,
    upload_customers_json,
    create_file_upload,
    create_json_upload,
)
from .models import CreateCustomerException, FileUploadException


class UploadViewSet(ViewSet):
    serializer_class = UploadSerializer
    permission_classes = (IsAuthenticated,)

    def list(self, request):
        first_name = request.query_params.get("first_name", None)
        last_name = request.query_params.get("last_name", None)
        national_id = request.query_params.get("national_id", None)
        country = request.query_params.get("country", None)
        birth_date = request.query_params.get("birth_date", None)
        phone_number = request.query_params.get("phone_number", None)
        email = request.query_params.get("email", None)

        customers = get_customers.delay(
            pk=None,
            first_name=first_name,
            last_name=last_name,
            email=email,
            phone_number=phone_number,
            national_id=national_id,
            country=country,
            birth_date=birth_date,
        )
        response = customers.get(propagate=True)
        return JsonResponse(response, safe=False)

    def retrieve(self, request, pk=None):
        customer = get_customers.delay(pk)
        response = customer.get(propagate=True)
        return JsonResponse(response)

    def update(self, request, pk=None):
        res = update_customer.delay(pk, request.body)
        return res.get(propagate=True)

    def create(self, request):
        file_uploaded = None
        req_body = request.body
        req_data = request.data

        if "file" in request.FILES:
            file_uploaded = request.FILES["file"]
            content_type = file_uploaded.content_type
            if content_type == "text/csv":
                try:
                    create_file_upload.delay(file_uploaded, request.user)
                except FileUploadException as fe:
                    raise fe
            else:
                try:
                    res = upload_customers.delay(req_body)
                except CreateCustomerException as ce:
                    raise ce
        else:
            try:
                res = create_json_upload.delay(request.user, req_data)
            except CreateCustomerException as ce:
                raise ce

        res.get(propagate=True)

        if res.successful():
            return JsonResponse({"message": "customers succesfully created in the db"})
        else:
            raise CreateCustomerException("Error occured while creating customers")
