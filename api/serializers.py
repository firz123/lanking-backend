from rest_framework import serializers
from .models import Users, Landlords, Ratings, Properties


class UsersSerializer(serializers.ModelSerializer):
	class Meta:
		model = Users 
		fields = '__all__'

class LandlordsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Landlords 
		fields = '__all__'

class RatingsSerializer(serializers.ModelSerializer):
	class Meta:
		model = Ratings
		fields = '__all__'

class PropertiesSerializer(serializers.ModelSerializer):
	class Meta:
		model = Properties 
		fields = '__all__'