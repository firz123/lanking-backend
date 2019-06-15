from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Users, Landlords, Ratings, Properties
from .serializers import UsersSerializer, LandlordsSerializer, RatingsSerializer, PropertiesSerializer


class BaseUserTest(APITestCase):
	client = APIClient()
	@staticmethod
	def create_user(username="", password="", realnameVisible=""):
		if all([username!="", password!="", realnameVisible!=""]):
			Users.objects.create(username=username, password=password, 
				realnameVisible=False, is_staff=False)

	def setUp(self):
		self.create_user("user1", "password1", False)
		self.create_user("user2", "password2", False)
		self.create_user("user3", "password3", False)
		self.create_user("user4", "password4", False)

class GetAllUsersTest(BaseUserTest):
	def test_get_all_users(self):
		response = self.client.get(
            reverse("users-all")
        )
		expected = Users.objects.all()
		serialized = UsersSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

class BaseLandlordTest(APITestCase):
	client = APIClient()
	@staticmethod
	def create_landlord(name=""):
		if name != "":
			Landlords.objects.create(name=name, avgRating=None, sumRating=0, numRating=0)

	def setUp(self):
		self.create_landlord("ll1")
		self.create_landlord("ll2")
		self.create_landlord("ll3")
		self.create_landlord("ll4")


class GetAllLandlordsTest(BaseLandlordTest):
	def test_get_all_landlords(self):
		response = self.client.get(
            reverse("landlords-all")
        )
		expected = Landlords.objects.all()
		serialized = LandlordsSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)