from rest_framework import serializers
from app1.models import Ishchi


class IshchiSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ishchi
        fields = "__all__"
