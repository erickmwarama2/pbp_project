from django.db import models


class Customer(models.Model):
    first_name = models.CharField(max_length=30, db_index=True)
    last_name = models.CharField(max_length=30, db_index=True)
    national_id = models.CharField(max_length=30, db_index=True, unique=True)
    birth_date = models.DateField(db_index=True)
    address = models.CharField(max_length=30, db_index=True)
    country = models.CharField(max_length=30, db_index=True)
    phone_number = models.CharField(max_length=20, db_index=True, unique=True)
    email = models.EmailField(max_length=50, db_index=True, unique=True)
    finger_print_signature = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Name: {self.first_name} {self.last_name}, ID: {self.national_id}"
