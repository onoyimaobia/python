from rest_framework import serializers
from .models import last


class EmbedSerializer(serializers.ModelSerializer):
    class Meta:
        model = last
