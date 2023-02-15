from django.db import models


class FileUpload(models.Model):
    pass


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
