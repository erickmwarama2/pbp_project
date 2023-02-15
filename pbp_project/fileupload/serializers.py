from rest_framework.serializers import FileField, ModelSerializer
from .models import Customer, FileUploadModel


class UploadSerializer(ModelSerializer):
    file = FileField()

    class Meta:
        fields = ["file"]
        model = FileUploadModel


class CustomerSerializer(ModelSerializer):
    class Meta:
        model = Customer
        fields = "__all__"
