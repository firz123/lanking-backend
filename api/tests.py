from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Users, Landlords, Ratings, Properties
from .serializers import UsersSerializer, LandlordsSerializer, RatingsSerializer, PropertiesSerializer


class SetupTest(APITestCase):
	client = APIClient()
	def create_user(username="", password="", realnameVisible="" ):
		if all(username, password, realnameVisible):
			Users.objects.create(username=username, password=password, 
				realnameVisible=False, is_staff=false)