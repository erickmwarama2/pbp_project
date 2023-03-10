from .models import Customer, FileUploadModel
from celery import shared_task, signals
from celery.signals import task_postrun
from django.core.serializers import serialize
from .serializers import CustomerSerializer
import uuid
from .models import CreateCustomerException, FileUploadException
import csv


@signals.worker_init.connect
def on_worker_init(sender, **kwargs):
    signals.task_postrun.connect(create_file_upload_success_handler, sender=None)
    signals.task_postrun.connect(create_json_upload_success_handler, sender=None)


@shared_task(name="create_file_upload", ignore_result=False)
def create_file_upload(filepath, user_id):
    fileupload_model = FileUploadModel()
    fileupload = fileupload_model.create_file_upload_model(user_id, filepath)
    # res = task_postrun.send(retval=fileupload.id, sender=create_file_upload)
    return fileupload.id


@shared_task(name="create_json_upload", ignore_result=False)
def create_json_upload(filepath, user_id):
    fileupload_model = FileUploadModel()
    fileupload = fileupload_model.create_file_upload_model(user_id, filepath)
    # res = task_postrun.send(retval=fileupload.id, sender=create_file_upload)
    return fileupload.id


@shared_task
def process_file_upload_json(upload_id):
    upload = FileUploadModel.objects.get(id=upload_id)
    upload.upload_json()


@task_postrun.connect(sender=create_file_upload)
def create_file_upload_success_handler(sender=None, **kwargs):
    upload_id = kwargs.get("upload_id", 1)
    upload = FileUploadModel.objects.get(id=upload_id)
    upload.upload()


@task_postrun.connect()
def create_json_upload_success_handler(sender=None, **kwargs):
    upload_id = kwargs.get("upload_id", 1)
    upload = FileUploadModel.objects.get(id=upload_id)
    upload.upload()


@shared_task
def get_customers(
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
        query_set = Customer.objects.all()

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

        serializer = CustomerSerializer(query_set, many=True)
    else:
        response = Customer.objects.get(pk=pk)
        serializer = CustomerSerializer(response)

    return serializer.data


@shared_task
def update_customer(pk, customer):
    Customer.objects.update(pk, customer)
    return True


@shared_task
def upload_customers_json(data):
    customers = []

    for obj in data:
        obj["finger_print_signature"] = str(uuid.uuid1())
        customer = Customer(**obj)
        customers.append(customer)

    try:
        Customer.objects.bulk_create(customers)
    except Exception as e:
        raise CreateCustomerException(
            f"Exception occured while inserting customers: \n {str(e)}"
        )

    return True


@shared_task
def upload_customers(data):
    customers = []
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

        customer = Customer(
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
        customers.append(customer)

    try:
        Customer.objects.bulk_create(customers)
    except Exception as e:
        raise CreateCustomerException(
            f"Exception occured while inserting customers : \n {str(e)}"
        )

    return True
