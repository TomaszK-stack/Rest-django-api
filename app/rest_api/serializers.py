from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    user = serializers.HiddenField(default=serializers.CurrentUserDefault())


    class Meta:
        model = Image
        fields = ('image', "user")
    def create(self, validated_data):
        return Image.objects.create(**validated_data)
