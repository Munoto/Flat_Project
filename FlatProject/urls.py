from django.contrib import admin
from django.urls import path, re_path, include

from backend.views import ApartmentAPIView, ApartmentRetrieveAPIView, ApartmentCreateAPIView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/apartmentlist/', ApartmentAPIView.as_view()),
    path('api/v1/apartmentlist/<int:pk>/', ApartmentRetrieveAPIView.as_view()),
    path('api/v1/apartmentcreate/', ApartmentCreateAPIView.as_view()),
    path('api/v1/auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')),

]
