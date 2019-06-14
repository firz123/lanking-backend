from rest_framework import generics
from .models import Users, Landlords, Ratings, Properties
from .serializers import UsersSerializer, LandlordsSerializer, RatingsSerializer, PropertiesSerializer

class ListAllUsersView(generics.ListAPIView):
    queryset = Users.objects.all()
    serializer_class = UsersSerializer