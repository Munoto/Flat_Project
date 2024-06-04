from rest_framework import serializers
from rest_framework.exceptions import ValidationError

from backend.models import Apartment, About, Image, CustomUser


class ApartmentImageSerializer(serializers.ModelSerializer):
    image_url = serializers.SerializerMethodField()

    class Meta:
        model = Image
        fields = ['image_url']

    def to_representation(self, instance):
        request = self.context.get('request')
        return request.build_absolute_uri(instance.image.url)


class AboutSerializer(serializers.ModelSerializer):
    class Meta:
        model = About
        fields = '__all__'


class ApartmentSerializer(serializers.ModelSerializer):
    images = ApartmentImageSerializer(many=True, read_only=True)

    class Meta:
        model = Apartment
        fields = '__all__'
        extra_kwargs = {'user': {'required': False}}

    def create(self, validated_data):
        request = self.context.get('request')
        images_data = request.FILES.getlist('images')

        if not images_data:
            raise ValidationError("No images provided")

        user = request.user
        apartment = Apartment.objects.create(user=user, **validated_data)

        for image_data in images_data:
            Image.objects.create(apartment=apartment, image=image_data)

        return apartment

    def update(self, instance, validated_data):
        request = self.context.get('request')
        images_data = request.FILES.getlist('images')

        # Обновляем поля объекта
        for attr, value in validated_data.items():
            setattr(instance, attr, value)
        instance.save()

        if images_data:
            # Удаляем старые изображения
            instance.images.all().delete()

            # Добавляем новые изображения
            for image_data in images_data:
                Image.objects.create(apartment=instance, image=image_data)

        return instance


# Сериализатор для профиля

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = [
            'pk', 'email', 'first_name', 'last_name', 'birth_date',
            'city', 'phone_number', 'avatar', 'profile_image', 'is_verified'
        ]
        read_only_fields = ['email']


class UserVerificationSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['is_verified', 'profile_image']


class ProfileImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['profile_image', 'avatar']
        extra_kwargs = {
            'profile_image': {'required': False},
            'avatar': {'required': False}
        }
