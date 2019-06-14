from django.contrib import admin

# Register your models here.
from .models import Users, Landlords, Ratings, Properties

admin.site.register(Users)
admin.site.register(Landlords)
admin.site.register(Ratings)
admin.site.register(Properties)