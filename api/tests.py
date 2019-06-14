from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import Users, Landlords, Ratings, Properties
from .serializers import UsersSerializer, LandlordsSerializer, RatingsSerializer, PropertiesSerializer


class BaseTest(APITestCase):
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

class GetAllUsersTest(BaseTest):
	def test_get_all_songs(self):
		response = self.client.get(
            reverse("users-all")
        )
		expected = Users.objects.all()
		serialized = UsersSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)