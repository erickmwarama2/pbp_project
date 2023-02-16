from django.db import models, transaction
import enum
import datetime
import os
import csv
import uuid
import json
from django.contrib.auth.models import User


class FileUploadModel(models.Model):
    class UploadStatus(models.IntegerChoices):
        PENDING = 1
        PROCESSED = 2
        FAILED = 3

    file_path = models.CharField(max_length=255)
    uploaded_by = models.ForeignKey("auth.User", on_delete=models.SET_NULL, null=True)
    upload_date = models.DateTimeField(auto_now_add=True)
    upload_status = models.IntegerField(
        choices=UploadStatus.choices, default=UploadStatus.PENDING
    )
    processing_message = models.TextField(blank=True, null=True)
    num_records = models.PositiveIntegerField(default=0)
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)

    @property
    def filename(self):
        return os.path.basename(self.filename)

    def create_file_upload_model(self, user_id, filepath):
        return FileUploadModel.objects.create(
            file_path=filepath, uploaded_by=User.objects.get(pk=user_id)
        )

    def mark_processed(self, num_records):
        self.upload_status = self.UploadStatus.PROCESSED
        self.end_date_time = datetime.datetime.now()
        self.num_records = num_records
        self.processing_message = None
        self.save()

    def mark_failed(self, message):
        self.upload_status = self.UploadStatus.FAILED
        self.processing_message = message
        self.save()

    def upload_json(self, body):
        self.start_date_time = datetime.datetime.now()
        customers = []
        num_records = 0

        try:
            with open(self.file_path, "rb") as f:
                decoded_file = json.load(f)

                for row in decoded_file:
                    customer = Customer(
                        first_name=row.get("first_name", None),
                        last_name=row.get("last_name", None),
                        national_id=row.get("national_id", None),
                        birth_date=row.get("birth_date", None),
                        address=row.get("address", None),
                        country=row.get("country", None),
                        phone_number=row.get("phone_number", None),
                        email=row.get("email", None),
                        finger_print_signature=str(uuid.uuid1()),
                    )
                    customers.append(customer)
                    num_records += 1

                with transaction.atomic():
                    Customer.objects.bulk_create(customers, ignore_conflicts=True)
        except Exception as e:
            self.mark_failed(str(e))
            raise CreateCustomerException(
                f"Error occured while creating customer records: \n {str(e)}"
            )
        else:
            self.mark_processed(num_records)

    def upload(self):
        self.start_date_time = datetime.datetime.now()
        customers = []
        num_records = 0

        try:
            with open(self.file_path, "rb") as f:
                decoded_file = f.read().decode("utf-8").splitlines()
                reader = csv.DictReader(decoded_file)

                for row in reader:
                    customer = Customer(
                        first_name=row.get("first_name", None),
                        last_name=row.get("last_name", None),
                        national_id=row.get("national_id", None),
                        birth_date=row.get("birth_date", None),
                        address=row.get("address", None),
                        country=row.get("country", None),
                        phone_number=row.get("phone_number", None),
                        email=row.get("email", None),
                        finger_print_signature=str(uuid.uuid1()),
                    )
                    customers.append(customer)
                    num_records += 1

                with transaction.atomic():
                    Customer.objects.bulk_create(customers, ignore_conflicts=True)
        except Exception as e:
            self.mark_failed(str(e))
            raise CreateCustomerException(
                f"Error occured while creating customer records: \n {str(e)}"
            )
        else:
            self.mark_processed(num_records)


class Customer(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    national_id = models.CharField(max_length=30)
    birth_date = models.DateField(db_index=True)
    address = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    finger_print_signature = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        indexes = [
            models.Index(fields=["first_name"]),
            models.Index(fields=["last_name"]),
            models.Index(fields=["national_id"]),
            models.Index(fields=["birth_date"]),
            models.Index(fields=["address"]),
            models.Index(fields=["country"]),
            models.Index(fields=["phone_number"]),
            models.Index(fields=["email"]),
        ]

        constraints = [
            models.UniqueConstraint(fields=["national_id"], name="unique_national_id"),
            models.UniqueConstraint(
                fields=["phone_number"], name="unique_phone_number"
            ),
            models.UniqueConstraint(fields=["email"], name="unique_email"),
        ]

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}, ID: {self.national_id}"


class CreateCustomerException(Exception):
    def __init__(self, message):
        super().__init__(message)


class FileUploadException(Exception):
    def __init__(self, message):
        super().__init__(message)
