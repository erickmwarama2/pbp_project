from rest_framework.serializers import FileField, ModelSerializer
from .models import User


class UploadSerializer(ModelSerializer):
    file = FileField()

    class Meta:
        fields = ["file"]
        model = User


class UserSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
