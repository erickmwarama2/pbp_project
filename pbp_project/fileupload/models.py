from django.db import models
import enum
import datetime


class FileUpload(models.Model):
    class UploadStatus(enum.Enum):
        PENDING = 1
        PROCESSED = 2
        FAILED = 3

    file_path = models.CharField()
    uploaded_by = models.ForeignKey("auth.User")
    upload_date = models.DateTimeField(auto_now_add=True)
    upload_status = models.IntegerField(
        choices=UploadStatus, default=UploadStatus.PENDING
    )
    processing_message = models.TextField(blank=True, null=True)
    num_records = models.PositiveIntegerField()
    start_date_time = models.DateTimeField(null=True)
    end_date_time = models.DateTimeField(null=True)

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

    def upload(self):
        self.start_date_time = datetime.datetime.now()

        try:
            pass
        except Exception as e:
            self.mark_failed(str(e))
        else:
            self.mark_processed(0)


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
            models.UniqueConstraint(fields=["national_id"]),
            models.UniqueConstraint(fields=["phone_number"]),
            models.UniqueConstraint(fields=["email"]),
        ]

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}, ID: {self.national_id}"
