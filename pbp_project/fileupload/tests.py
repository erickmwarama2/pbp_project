from django.test import TestCase, RequestFactory
from .models import Customer
from .views import UploadViewSet
from django.forms.models import model_to_dict
import uuid
from django.urls import resolve
from django.contrib.auth.models import AnonymousUser, User


class UserUnitTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.customer = Customer(
            first_name="first",
            last_name="last",
            national_id=1,
            birth_date="2020-01-01",
            address="address",
            country="country",
            phone_number="00100",
            email="user@email.com",
            finger_print_signature=str(uuid.uuid1()),
        )
        self.customer.save()

    def test_user_inserted(self):
        # test user was inserted into db
        db_customer = Customer.objects.get(pk=self.customer.id)
        self.assertEqual(db_customer.id, self.customer.id)

    def test_create_user(self):
        customers = [model_to_dict(self.customer)]
        match = resolve("/customers/")

        headers = {"content-type": "application/json"}
        request = self.factory.post(match.url_name, customers, **headers)
        request.user = AnonymousUser()

        response = UploadViewSet.as_view({"post": "create"})(request)

        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        # test GET /customers/:id endpoint
        match = resolve("/customers/")

        headers = {"content-type": "application/json"}
        request = self.factory.get(match.url_name, **headers)
        request.user = AnonymousUser()

        response = UploadViewSet.as_view({"get": "retrieve"})(request, self.customer.id)
        self.assertEqual(response.status_code, 200)
