from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager, PermissionsMixin
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import FileExtensionValidator
import os


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError('The Email field must be set')
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(email, password, **extra_fields)


class CustomUser(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)
    city = models.CharField(max_length=150)
    phone_number = models.CharField(max_length=30)
    profile_image = models.ImageField(upload_to='profile_images/', null=True, blank=True)
    is_vip = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(
        upload_to='avatars/',
        blank = True,
        null = True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg', 'png'])]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'city', 'birth_date', 'phone_number']

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name


def apartment_image_upload_path(instance, filename):
    return f'images/apartments/{instance.apartment.name}/{filename}'


class Apartment(models.Model):
    type = models.CharField(max_length=100)
    rent_type = models.CharField(max_length=100, null=True)
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    count_of_rooms = models.CharField(max_length=255)
    region = models.CharField(max_length=100)
    street = models.CharField(max_length=100)
    house_number = models.CharField(max_length=100)
    longitude = models.IntegerField(null=True)
    latitude = models.IntegerField(null=True)
    year_of_construction = models.IntegerField(validators=[MaxValueValidator(2024)])
    max_floor = models.IntegerField(validators=[MaxValueValidator(38)])
    floor = models.IntegerField(validators=[MaxValueValidator(38)])
    height = models.IntegerField()
    apartment_area = models.IntegerField()
    kitchen_area = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Image(models.Model):
    apartment = models.ForeignKey(Apartment, related_name='images', on_delete=models.CASCADE)
    image = models.ImageField(upload_to=apartment_image_upload_path)

    def __str__(self):
        return f"Image for {self.apartment.name}"


class About(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE, related_name='about', null=True)
    status = models.CharField(max_length=255)
    balcony = models.CharField(max_length=255)
    internet = models.CharField(max_length=255)
    bathroom = models.CharField(max_length=255)
    parking = models.CharField(max_length=255)
    furnished_type = models.CharField(max_length=255)
    floor = models.CharField(max_length=255)


