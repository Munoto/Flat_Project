import django_filters
from .models import Apartment

class ApartmentFilter(django_filters.FilterSet):
    class Meta:
        model = Apartment
        fields = {
            'type': ['exact', 'icontains'], # Селект
            'rent_type': ['exact', 'icontains'], #Селект
            'price': ['exact', 'lte', 'gte'], #интервал от и до
            'count_of_rooms': ['exact', 'lt', 'gt'], #
            'region': ['exact', 'icontains'],
            'house_number': ['exact'],
            'year_of_construction': ['exact'],
            'max_floor': ['exact'],
            'floor': ['exact'],
            'height': ['exact'],
            'apartment_area': ['exact'],
            'kitchen_area': ['exact'],
        }