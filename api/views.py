#from rest_framework import generics
from .models import UserAccount, Landlord, Rating, Property
from .serializers import UserSerializer, LandlordSerializer, RatingSerializer, PropertySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status

class UserView(APIView):
	"""
	Create users, list all users (for testing purposes)
	"""
	def get(self, request, format=None):
		users = UserAccount.objects.all()
		serializer = UserSerializer(users, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LandlordView(APIView):
	"""
	Create landlords, list all landlords (for testing purposes)
	"""
	def get(self, request, format=None):
		landlords = Landlord.objects.all()
		serializer = LandlordSerializer(landlords, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = LandlordSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class RatingView(APIView):
	"""
	Create rating, list all ratings (for testing purposes)
	"""
	def get(self, request, format=None):
		ratings = Rating.objects.all()
		serializer = RatingSerializer(ratings, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = RatingSerializer(data=request.data)
		if serializer.is_valid():
			#now add it to the landlord's many to many field
			rating = Rating(**serializer.validated_data)
			landlord = Landlord.objects.get(id__exact=rating.landlord_id)
			landlord.sumRating = landlord.sumRating + rating.rating
			landlord.numRating = landlord.numRating + 1
			landlord.avgRating = landlord.sumRating / landlord.numRating
			landlord.save()
			rating.save()
			landlord.ratings.add(rating)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PropertyView(APIView):
	"""
	Create property, list all properties (for testing purposes)
	"""
	def get(self, request, format=None):
		props = Property.objects.all()
		serializer = PropertySerializer(props, many=True)
		return Response(serializer.data)

	def post(self, request, format=None):
		serializer = PropertySerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)