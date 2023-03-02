from rest_framework import generics, viewsets
from rest_framework.parsers import MultiPartParser, FormParser
from .models import Image
from .serializers import ImageSerializer
from rest_framework.response import Response
from rest_framework import status, authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.decorators import api_view
from django.core.signing import Signer
from django.http import HttpResponseBadRequest, HttpResponseNotFound, HttpResponse

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
        return self.create(request, *args, **kwargs)

@api_view(http_method_names=["GET", "POST"])
def generate_exp_links(request):
    serializer = ImageSerializer()
    if request.user.tier.generate_exp_links:
        if request.method == "POST":
            signer = Signer()
            signed_value = signer.sign("http://127.0.0.1:8000/static/images/326811043_5719292304862868_8427228551201173610_n_1_p5iMSLq.png")
            seconds = 60
            signed_value_with_expiry = f"{signed_value};{seconds}"
            print(signed_value)
            return Response(signed_value_with_expiry)
        return Response("Create your expiring links")

    else:
        return Response("You do not have permissions to create expiring links.")


def get_image(request, signed_value):
    # Rozdzielenie podpisu i czasu wygaśnięcia
    signer = Signer()
    try:
        value, expiry = signed_value.split(';')
        # Sprawdzenie podpisu i czasu wygaśnięcia
        value = signer.unsign(value)
    except Exception as e:
        print(e)
        return HttpResponseNotFound('Podpisany link wygasł lub jest nieprawidłowy.')
    # Pobranie i zwrócenie obrazu
    with open(value, 'rb') as f:
        image_data = f.read()
    return HttpResponse(image_data, content_type='image/jpeg')

def image_test(request):


    with open("static\\images\\326811043_5719292304862868_8427228551201173610_n.png", 'rb') as f:
        image_data = f.read()
        return HttpResponse(image_data, content_type='image/jpeg')