from django.test import TestCase, RequestFactory, Client
from .models import Customer
from .views import UploadViewSet
from django.forms.models import model_to_dict
import uuid
from django.urls import resolve


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
        self.client = Client()
        self.client.login(username="erick", password="erick")
        self.customer.save()

    def test_user_inserted(self):
        # test user was inserted into db
        db_customer = Customer.objects.get(pk=self.customer.id)
        self.assertEqual(db_customer.id, self.customer.id)

    def test_create_user(self):
        customers = [model_to_dict(self.customer)]
        match = resolve("/customers/")

        response = self.client.post(
            match.url_name, customers, content_type="application/json"
        )
        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        # test GET /customers/:id endpoint
        match = resolve("/customers/" + self.customer.id)

        response = self.client.get(match.url_name)
        self.assertEqual(response.status_code, 200)
