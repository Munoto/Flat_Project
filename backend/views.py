from rest_framework.authentication import TokenAuthentication
from rest_framework.decorators import api_view, permission_classes
from rest_framework.generics import RetrieveAPIView, CreateAPIView, DestroyAPIView, UpdateAPIView, ListAPIView, \
    get_object_or_404, RetrieveUpdateAPIView
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework import pagination, status
from rest_framework.views import APIView

from backend.models import Apartment, About, CustomUser
from backend.permissions import IsOwnerOrReadOnly
from backend.serializers import ApartmentSerializer, AboutSerializer, CustomUserSerializer, ProfileImageSerializer
from media.profile_images.utils import verify_identity


class PagePagination(pagination.PageNumberPagination):
    def get_paginated_response(self, data):
        return Response({
            'links': {
                'next': self.get_next_link(),
                'previous': self.get_previous_link()
            },
            'count': self.page.paginator.count,
            'total_pages': self.page.paginator.num_pages,
            'results': data,
        })


# Возвращает один обьект (Apartment и About)
# class ApartmentRetrieveAPIView(RetrieveAPIView):
#     queryset = Apartment.objects.all()
#     serializer_class = ApartmentSerializer
#
#     def retrieve(self, request, *args, **kwargs):
#         instance = self.get_object()
#         about_instance = About.objects.get(apartment=instance)
#         about_serializer = AboutSerializer(about_instance)
#         serializer = self.get_serializer(instance)
#         data = serializer.data
#         data['about'] = about_serializer.data
#         return Response(data)

# class UserApartmentListAPIView(generics.ListCreateAPIView):
#     serializer_class = YourModelSerializer
#
#     def get_queryset(self):
#         user = self.request.user
#         return YourModel.objects.filter(user=user)


class ApartmentRetrieveAPIView(RetrieveAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer

    def retrieve(self, request, *args, **kwargs):
        instance = self.get_object()

        try:
            user_instance = CustomUser.objects.get(apartment=instance)
            about_instance = About.objects.get(apartment=instance)
            about_serializer = AboutSerializer(about_instance)
            user_serializer = CustomUserSerializer(user_instance)
            about_data = about_serializer.data
            user_data = user_serializer.data
        except About.DoesNotExist:
            about_data = None

        serializer = self.get_serializer(instance)
        data = serializer.data
        data['landowner'] = user_data
        if about_data:
            data['about'] = about_data



        return Response(data)


# Возвращает все обьекты (для главной страницы)
class ApartmentListAPIView(ListAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    pagination_class = PagePagination


# Создание обьекта Apartment
class ApartmentCreateAPIView(CreateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated]


# Удаление обьекта Apartment
class ApartmentDeleteAPIView(DestroyAPIView):
    queryset = Apartment.objects.all()
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'


# Обновление обьекта Apartment
class ApartmentUpdateAPIView(UpdateAPIView):
    queryset = Apartment.objects.all()
    serializer_class = ApartmentSerializer
    authentication_classes = [TokenAuthentication]
    permission_classes = [IsAuthenticated, IsOwnerOrReadOnly]
    lookup_field = 'id'

# Вывод обьявлений пользователя
class UserApartmentListAPIView(ListAPIView):
    serializer_class = ApartmentSerializer
    pagination_class = PagePagination
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        return Apartment.objects.filter(user=user)


# Создание обьекта About

class AboutCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, apartment_id):
        apartment = get_object_or_404(Apartment, id=apartment_id)
        if apartment.user != request.user:
            return Response({"detail": "You do not have permission to add about for this apartment."},
                            status=status.HTTP_403_FORBIDDEN)

        serializer = AboutSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(apartment=apartment)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


#Обновление обьекта About
class AboutUpdateAPIView(UpdateAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'apartment_id'
    lookup_url_kwarg = 'apartment_id'

    def get_object(self):
        apartment = get_object_or_404(Apartment, id=self.kwargs['apartment_id'])
        if apartment.user != self.request.user:
            raise PermissionDenied({"detail": "You do not have permission to update about for this apartment."})
        return get_object_or_404(About, apartment=apartment)



# Удаление обьекта About
class AboutDeleteAPIView(DestroyAPIView):
    queryset = About.objects.all()
    serializer_class = AboutSerializer
    permission_classes = [IsAuthenticated]
    lookup_field = 'apartment_id'
    lookup_url_kwarg = 'apartment_id'

    def get_object(self):
        apartment = get_object_or_404(Apartment, id=self.kwargs['apartment_id'])
        if apartment.user != self.request.user:
            raise PermissionDenied({"detail": "You do not have permission to delete about for this apartment."})
        return get_object_or_404(About, apartment=apartment)


# Редактирование пользователя
class CustomUserUpdateAPIView(RetrieveUpdateAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user

# Вернуть пользователя
class CustomUserDetailView(RetrieveAPIView):
    serializer_class = CustomUserSerializer
    permission_classes = [IsAuthenticated]

    def get_object(self):
        return self.request.user


class VerifyIdentityView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        user = request.user
        image = request.FILES.get('image')
        if image and verify_identity(user, image):
            user.is_verified = True
            user.save()
            return Response({'status': 'verified'}, status=status.HTTP_200_OK)
        return Response({'status': 'failed'}, status=status.HTTP_400_BAD_REQUEST)
