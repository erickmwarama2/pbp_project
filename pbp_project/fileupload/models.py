from django.db import models


class User(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    national_id = models.CharField(max_length=30)
    birth_date = models.DateField()
    address = models.CharField(max_length=30)
    country = models.CharField(max_length=30)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField(max_length=50)
    finger_print_signature = models.CharField(max_length=50)

    def __str__(self):
        return f"{self.first_name} {self.last_name}, {self.national_id}, {self.birth_date} {self.address}, {self.email}"
