from django.contrib import admin

# Register your models here.
from .models import UserAccount, Landlord, Rating, Property

admin.site.register(UserAccount)
admin.site.register(Landlord)
admin.site.register(Rating)
admin.site.register(Property)