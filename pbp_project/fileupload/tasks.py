from .models import User
from celery import shared_task
from django.core.serializers import serialize
from .serializers import UserSerializer
import json


@shared_task
def get_users(pk=None, search=None, order=None):
    response = None

    if search is None:
        search = {}
    if order is None:
        order = {}

    if pk is None:
        response = User.objects.all().filter(**search).order_by(**order)
        serializer = UserSerializer(response, many=True)
    else:
        response = User.objects.get(pk=pk)
        serializer = UserSerializer(response)

    return serializer.data


@shared_task
def update_user(pk, user):
    User.objects.update(pk, user)
    return True


@shared_task
def upload_users_json(data):
    users = []

    for obj in data:
        user = User(**obj)
        users.append(user)

    try:
        User.objects.bulk_create(users)
    except Exception:
        raise Exception("Exception occured while inserting users")

    return True


@shared_task
def upload_users(data):
    users = []
    for text in data:
        if text == "":
            continue

        read_values = text.split(",")
        first_name = read_values[0]
        last_name = read_values[1]
        national_id = read_values[2]
        birth_date = read_values[3]
        address = read_values[4]
        country = read_values[5]
        phone_number = read_values[6]
        email = read_values[7]
        finger_print_signature = "hhhhhhofe"

        user = User(
            first_name=first_name,
            last_name=last_name,
            national_id=national_id,
            birth_date=birth_date,
            address=address,
            country=country,
            phone_number=phone_number,
            email=email,
            finger_print_signature=finger_print_signature,
        )
        users.append(user)

    try:
        User.objects.bulk_create(users)
    except Exception:
        raise Exception("Exception occured while inserting users")

    return True