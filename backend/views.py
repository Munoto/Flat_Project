from rest_framework.generics import RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import Apartment, About
from backend.serializers import ApartmentSerializer, AboutSerializer


# Возвращает один обьект
class ApartmentRetrieveAPIView(RetrieveAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()
        about_instance = About.objects.get(apartment=instance)
        about_serializer = AboutSerializer(about_instance)
        serializer = self.get_serializer(instance)
        data = serializer.data
        data['about'] = about_serializer.data
        return Response(data)


# Возвращает все обьекты
class ApartmentAPIView(APIView):
    def get(self, request):
        lst = Apartment.objects.all().values()
        return Response({'lists': list(lst)})


