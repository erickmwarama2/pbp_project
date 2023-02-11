from django.test import TestCase, RequestFactory
from .models import User
from .views import UploadViewSet
from django.forms.models import model_to_dict
import uuid


class UserUnitTestCase(TestCase):
    def setUp(self):
        super().setUp()
        self.factory = RequestFactory()
        self.user = User(
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
        self.user.save()

    def test_user_inserted(self):
        # test user was inserted into db
        db_user = User.objects.get(pk=self.user.id)
        self.assertEqual(db_user.id, self.user.id)

    def test_create_user(self):
        users = [model_to_dict(self.user)]

        request = self.factory.post("/users", users, content_type="application/json")

        response = UploadViewSet.as_view({"post": "create"})(request)

        self.assertEqual(response.status_code, 200)

    def test_get_user(self):
        # test GET /users/:id endpoint
        request = self.factory.get("/users")

        response = UploadViewSet.as_view({"get": "retrieve"})(request, self.user.id)
        self.assertEqual(response.status_code, 200)
