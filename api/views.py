#from rest_framework import generics
from .models import Users, Landlords, Ratings, Properties
from .serializers import UsersSerializer, LandlordsSerializer, RatingsSerializer, PropertiesSerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserView(APIView):
	"""
	Create users, list all users (for testing purposes)
	"""
	def get(self, request, format=None):
		users = Users.objects.all()
		serializer = UsersSerializer(users, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = UsersSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)