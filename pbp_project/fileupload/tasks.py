from .models import User
from celery import shared_task
from django.core.serializers import serialize
from .serializers import UserSerializer
import uuid
from .views import CreateCustomerException


@shared_task
def get_users(
    pk=None,
    first_name=None,
    last_name=None,
    country=None,
    national_id=None,
    email=None,
    phone_number=None,
    birth_date=None,
):
    response = None

    if pk is None:
        query_set = User.objects.all()

        if first_name is not None:
            query_set = query_set.filter(first_name=first_name)

        if last_name is not None:
            query_set = query_set.filter(last_name=last_name)

        if country is not None:
            query_set = query_set.filter(country=country)

        if email is not None:
            query_set = query_set.filter(email=email)

        if national_id is not None:
            query_set = query_set.filter(national_id=national_id)

        if phone_number is not None:
            query_set = query_set.filter(phone_number=phone_number)

        if birth_date is not None:
            query_set = query_set.filter(birth_date=birth_date)

        serializer = UserSerializer(query_set, many=True)
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
        obj["finger_print_signature"] = str(uuid.uuid1())
        user = User(**obj)
        users.append(user)

    try:
        User.objects.bulk_create(users)
    except Exception as e:
        raise CreateCustomerException(
            f"Exception occured while inserting users: \n {str(e)}"
        )

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
        finger_print_signature = str(uuid.uuid1())

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
    except Exception as e:
        raise CreateCustomerException(
            f"Exception occured while inserting users : \n {str(e)}"
        )

    return True
