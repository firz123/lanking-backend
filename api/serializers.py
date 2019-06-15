from rest_framework import serializers
from .models import UserAccount, Landlord, Rating, Property


class UserSerializer(serializers.ModelSerializer):
	class Meta:
		model = UserAccount 
		fields = '__all__'

class LandlordSerializer(serializers.ModelSerializer):
	class Meta:
		model = Landlord 
		fields = ['name']

class RatingSerializer(serializers.ModelSerializer):
	class Meta:
		model = Rating
		fields = '__all__'

class PropertySerializer(serializers.ModelSerializer):
	class Meta:
		model = Property
		fields = '__all__'