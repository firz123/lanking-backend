from rest_framework import serializers
from .models import UserAccount, Landlord, Rating, Property


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserAccount 
		fields = ['username', 'password', 'realnameVisible', 'is_staff']


class LandlordSerializer(serializers.ModelSerializer):
	class Meta:
		model = Landlord 
		fields = ['first', 'last']

class RatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rating
		fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
	class Meta:
		model = Property
		fields = '__all__'