from django.contrib.auth.base_user import AbstractBaseUser
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models
from django.core.validators import MaxValueValidator
from django.core.validators import FileExtensionValidator


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


class CustomUser(AbstractBaseUser):
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    birth_date = models.DateField(null=True)
    city = models.CharField(max_length=150)
    is_vip = models.BooleanField(default=False)
    is_verified = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    avatar = models.ImageField(
        upload_to='',
        blank = True,
        null = True,
        validators=[FileExtensionValidator(allowed_extensions=['jpg'])]
    )

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name', 'city', 'birth_date']

    objects = CustomUserManager()

    def __str__(self):
        return self.first_name



class Image(models.Model):
    image = models.ImageField(upload_to='images/')


class Apartment(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    description = models.TextField()
    count_of_rooms = models.CharField(max_length=255)
    location = models.CharField(max_length=100)
    year_of_construction = models.IntegerField(validators=[MaxValueValidator(2024)])
    max_floor = models.IntegerField(validators=[MaxValueValidator(38)])
    floor = models.IntegerField(validators=[MaxValueValidator(38)])
    height = models.IntegerField()
    apartment_area = models.IntegerField()
    kitchen_area = models.IntegerField()
    image = models.ForeignKey(Image, on_delete=models.CASCADE, null=True, blank=True)
    bathroom = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.name



class About(models.Model):
    apartment = models.OneToOneField(Apartment, on_delete=models.CASCADE)
    status = models.CharField(max_length=255)
    balcony = models.CharField(max_length=255)
    phone_status = models.CharField(max_length=255)
    internet = models.CharField(max_length=255)
    bathroom = models.CharField(max_length=255)
    door = models.CharField(max_length=255)
    parking = models.CharField(max_length=255)
    furnished_type = models.CharField(max_length=255)
    floor = models.CharField(max_length=255)


