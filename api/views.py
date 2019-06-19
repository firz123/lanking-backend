#from rest_framework import generics
from .models import UserAccount, Landlord, Rating, Property
from rest_framework.authtoken.models import Token
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated 
from .serializers import UserSerializer, LandlordSerializer, RatingSerializer, PropertySerializer
from django.http import Http404
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status


class UserView(APIView):
	"""
	Create users from POST data
	"""
	def post(self, request, format=None):
		serializer = UserSerializer(data=request.data)
		if serializer.is_valid():
			user_acct = UserAccount(**serializer.validated_data)
			user_acct.set_password(user_acct.password)
			user_acct.save()
			Token.objects.create(user=user_acct)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserAuthView(APIView):
	"""
	Login users from POST data
	"""
	def post(self, request, format=None):
		username = request.data.get("username")
		password = request.data.get("password")
		if username is None or password is None:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		try:
			user = UserAccount.objects.get(username=username)
		except Exception as e:
			return Response(status=status.HTTP_403_FORBIDDEN)
		token = Token.objects.get(user=user)
		return Response({'token': token.key},
                    status=status.HTTP_200_OK)

class UserRatingsView(APIView):
	"""
	Get user ratings from user ID as GET parameter
	"""
	def get(self, request, format=None):
		ratings = Rating.objects.all()
		user_id = self.request.query_params.get('id', None)
		if user_id is not None:
			ratings = ratings.filter(author_id__exact=user_id)
			serializer = RatingSerializer(ratings, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		serializer = RatingSerializer(ratings, many=True)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class LandlordView(APIView):
	"""
	Query landlords by name
	"""
	def get(self, request, format=None):
		landlords = Landlord.objects.all()
		first = self.request.query_params.get('first', None)
		last = self.request.query_params.get('last', None)
		if last is not None:
			try:
				landlords = landlords.filter(last__icontains=last)
			except Exception as e:
				landlords = Landlord.objects.none()
		if first is not None:
			try:
				landlords = landlords.filter(first__icontains=first)
			except Exception as e:
				pass
		serializer = LandlordSerializer(landlords, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)

	"""
	Create landlords from POST data
	"""
	def post(self, request, format=None):
		serializer = LandlordSerializer(data=request.data)
		if serializer.is_valid():
			serializer.save()
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class LandlordIDView(APIView):
	"""
	Get landlord ratings or properties from ID
	"""
	def get(self, request, format=None):
		landlord_id = self.request.query_params.get('id', None)
		ratings = self.request.query_params.get('get_ratings', None)
		properties = self.request.query_params.get('get_properties', None)
		if landlord_id is None:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		landlord = Landlord.objects.get(id__exact=landlord_id)
		serializer = None
		if ratings is not None:
			serializer = RatingSerializer(landlord.ratings, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		if properties is not None:
			serializer = PropertySerializer(landlord.properties, many=True)
			return Response(serializer.data, status=status.HTTP_200_OK)
		return Response(status=status.HTTP_200_OK)

class RatingView(APIView):
	"""
	Create rating from POST data, update landlord ratings
	"""
	authentication_classes = (TokenAuthentication,)
	permission_classes = (IsAuthenticated,)   

	def post(self, request, format=None):
		serializer = RatingSerializer(data=request.data)
		if serializer.is_valid():
			#now add it to the landlord's many to many field
			rating = Rating(**serializer.validated_data)
			if request.user.id != rating.author_id:
				return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

			landlord = Landlord.objects.get(id__exact=rating.landlord_id)
			landlord.sum_rating = landlord.sum_rating + rating.rating
			landlord.num_rating = landlord.num_rating + 1
			landlord.avg_rating = landlord.sum_rating / landlord.num_rating
			landlord.save()
			rating.save()
			landlord.ratings.add(rating)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PropertyView(APIView):
	"""
	Query the properties by address, ZIP, city, state
	"""
	def get(self, request, format=None):	
		props = Property.objects.all()
		address = self.request.query_params.get('address', None)
		state = self.request.query_params.get('state', None)
		city = self.request.query_params.get('city', None)
		zipcode = self.request.query_params.get('zip', None)
		if state is not None:
			props = props.filter(state__exact=state)
		if city is not None:
			props = props.filter(city__icontains=city)
		if zipcode is not None:
			props = props.filter(zipcode__exact=zipcode)
		if address is not None:
			props = props.filter(addressline__icontains=address)
		serializer = PropertySerializer(props, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)
	"""
	Create property from POST data, update landlord properties
	"""
	def post(self, request, format=None):
		serializer = PropertySerializer(data=request.data)
		if serializer.is_valid():
			#now add it to the landlord's many to many field
			prop = Property(**serializer.validated_data)
			landlord = Landlord.objects.get(id__exact=prop.landlord_id)
			landlord.save()
			prop.save()
			landlord.properties.add(prop)
			return Response(serializer.data, status=status.HTTP_201_CREATED)
		return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class PropertyIDView(APIView):
	"""
	Get the landlord from the property ID
	"""
	def get(self, request, format=None):	
		property_id = self.request.query_params.get('id', None)
		if property_id is None:
			return Response(status=status.HTTP_400_BAD_REQUEST)
		prop = Property.objects.get(id__exact=property_id)
		landlord = prop.landlord_set.all()
		serializer = LandlordSerializer(landlord, many=True)
		return Response(serializer.data, status=status.HTTP_200_OK)