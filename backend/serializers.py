from rest_framework import serializers

from backend.models import Apartment, About


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Apartment
        fields = '__all__'

    def create(self, validated_data):
        return Apartment.objects.create(**validated_data)


