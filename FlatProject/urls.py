from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, re_path, include
from rest_framework.routers import DefaultRouter

from backend.views import ApartmentListAPIView, ApartmentRetrieveAPIView, ApartmentCreateAPIView, \
    ApartmentDeleteAPIView, ApartmentUpdateAPIView, UserApartmentListAPIView, AboutCreateAPIView, AboutUpdateAPIView, \
    AboutDeleteAPIView, CustomUserUpdateAPIView, CustomUserDetailView, VerifyIdentityView, ApartmentViewSet



urlpatterns = [
    path('admin/', admin.site.urls), # Админская панель
    path('api/v1/apartment/list/', ApartmentListAPIView.as_view()), # Список всех квартир
    path('api/v1/myapartment/list/', UserApartmentListAPIView.as_view()), # Мои обьявления
    path('api/v1/apartment/create/', ApartmentCreateAPIView.as_view()), # Создание обьекта Apartment
    path('api/v1/apartment/delete/<int:id>/', ApartmentDeleteAPIView.as_view()), # Удаление обьекта Apartment
    path('api/v1/apartment/update/<int:id>/', ApartmentUpdateAPIView.as_view()), # Обновление обьекта Apartment
    path('api/v1/apartment/list/<int:pk>/', ApartmentRetrieveAPIView.as_view()), # Возвращает обьект Apartment и About
    path('api/v1/apartment/list/<int:apartment_id>/about/', AboutCreateAPIView.as_view()), # Создает обьект About
    path('api/v1/apartment/list/<int:apartment_id>/about/update/', AboutUpdateAPIView.as_view()), # Обновление обьекта About
    path('api/v1/apartment/list/<int:apartment_id>/about/delete/', AboutDeleteAPIView.as_view()), # Удаление обьекта About
    path('api/v1/profile/', CustomUserDetailView.as_view()),
    path('api/v1/profile/update/', CustomUserUpdateAPIView.as_view()),
    path('api/v1/verify-identity/', VerifyIdentityView.as_view()),
    path('api/v1/auth/', include('djoser.urls')), # / auth/users/
    re_path(r'^auth/', include('djoser.urls.authtoken')), # / auth/token/login/ Логин
                                                            # / auth/token/logout/  Выход из аккаунта
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
