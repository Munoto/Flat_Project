from django.contrib import admin
from django.urls import path, re_path, include

from backend.views import ApartmentListAPIView, ApartmentRetrieveAPIView, ApartmentCreateAPIView, \
    ApartmentDeleteAPIView, ApartmentUpdateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/apartment/list/', ApartmentListAPIView.as_view()), # Список всех квартир
    path('api/v1/apartment/create/', ApartmentCreateAPIView.as_view()), # Создание обьекта Apartment
    path('api/v1/apartment/delete/<int:id>/', ApartmentDeleteAPIView.as_view()), # Удаление обьекта Apartment
    path('api/v1/apartment/update/<int:id>/', ApartmentUpdateAPIView.as_view()), # Обновление обьекта Apartment
    path('api/v1/apartment/list/<int:pk>/', ApartmentRetrieveAPIView.as_view()), # Возвращает обьект Apartment и About
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]
