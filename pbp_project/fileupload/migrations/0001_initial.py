# Generated by Django 4.0 on 2023-02-10 13:59

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="User",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("first_name", models.CharField(max_length=30)),
                ("last_name", models.CharField(max_length=30)),
                ("national_id", models.CharField(max_length=30)),
                ("birth_date", models.DateField()),
                ("address", models.CharField(max_length=30)),
                ("country", models.CharField(max_length=30)),
                ("phone_number", models.CharField(max_length=20)),
                ("email", models.EmailField(max_length=50)),
                ("finger_print_signature", models.CharField(max_length=30)),
            ],
        ),
    ]