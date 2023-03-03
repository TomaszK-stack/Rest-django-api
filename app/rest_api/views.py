from rest_framework import generics, viewsets
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser
from .models import Image
from .serializers import ImageSerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view, parser_classes, authentication_classes, permission_classes
from django.core.signing import Signer, SignatureExpired, BadSignature
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse
import time


class ImageApiView(generics.ListAPIView):
    serializer_class = ImageSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [authentication.TokenAuthentication]

    def get_queryset(self):
        user = self.request.user

        return Image.objects.filter(user_id=user)


class ImageCreateView(generics.CreateAPIView):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer
    authentication_classes = [authentication.TokenAuthentication]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        data = request.data

        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        return Response("Succesfully added image", status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        serializer.save()

    def post(self, request, *args, **kwargs):
        print(request.data)
        return self.create(request, *args, **kwargs)


@api_view(http_method_names=["POST"])
@authentication_classes([authentication.TokenAuthentication])
@parser_classes([JSONParser])
@permission_classes([IsAuthenticated])
def generate_exp_links(request):
    if request.user.tier.generate_exp_links:
        data = request.data["link"]
        link = data.split("images/")[1]
        signer = Signer()
        signed_value = signer.sign_object({'file': link, 'time': time.time() + 30})

        return Response('http://localhost:8000/api/v1/image/' + signed_value)
    else:
        return Response("You do not have permissions to create expiring links.")


def get_image(request, signature):
    signer = Signer()
    try:
        value = signer.unsign_object(signature)

        if value["time"] < time.time():
            raise SignatureExpired

    except [SignatureExpired, BadSignature]:
        return HttpResponseNotFound('The link provided has expired or is invalid.')
    with open("static/images/" + value["file"], 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type='image/jpeg')

