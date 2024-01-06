from rest_framework import serializers
from .models import Item

class ItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = Item
        fields = '__all__'


class UserCredentialsSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=100)
    password = serializers.CharField(max_length=100)



class VideoGenerationSerializer(serializers.Serializer):
    url = serializers.CharField(max_length=700)
    title = serializers.CharField(max_length=100)