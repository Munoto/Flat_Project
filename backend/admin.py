from django.contrib import admin

from backend.models import Apartment, About, CustomUser

# Register your models here.
admin.site.register(Apartment)
admin.site.register(CustomUser)
admin.site.register(About)