from rest_framework.authentication import TokenAuthentication
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, ListAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from backend.models import Apartment, About
from backend.serializers import ApartmentSerializer, AboutSerializer


# Возвращает один обьект (Apartment и About)
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


# Возвращает все обьекты (для главной страницы)
class ApartmentListAPIView(ListAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer


# Создание обьекта Apartment
class ApartmentCreateAPIView(CreateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]

# Удаление обьекта Apartment
class ApartmentDeleteAPIView(DestroyAPIView):
    queryset = Apartment.objects.all()
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# Обновление обьекта Apartment
class ApartmentUpdateAPIView(UpdateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    lookup_field = 'id'
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]