from rest_framework import serializers
from .models import Image


class ImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField()
    image_th_200 = serializers.ImageField()
    image_th_400 = serializers.ImageField()

    class Meta:
        model = Image
        exclude_unset = True
        fields = ('image', "image_th_200", "image_th_400")

    def to_representation(self, instance):
        ret = super().to_representation(instance)
        new_ret = {key: ret[key] for key in ret.keys() if ret[key] != None}

        return new_ret

    def create(self, validated_data):
        return Image.objects.create(**validated_data)
