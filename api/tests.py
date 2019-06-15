import json
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
		self.valid_payload = {
			'name': 'll5'
        }
		self.invalid_payload = {
        	'name': ''
        }

class LandlordTests(BaseLandlordTest):
	def test_get_all_landlords(self):
		response = self.client.get(
            reverse("landlords-all")
        )
		expected = Landlords.objects.all()
		serialized = LandlordsSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_valid_landlord(self):
		response = self.client.post(
            reverse('landlords-all'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
		self.assertEqual(len(Landlords.objects.all()), 5)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_invalid_landlord(self):
		response = self.client.post(
            reverse('landlords-all'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
		self.assertEqual(len(Landlords.objects.all()), 4)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BaseRatingsTest(APITestCase):
	client = APIClient()
	@staticmethod
	def create_rating(authorID="", landlordID="", 
		propID="", comment="", rating=""):
		if all([authorID!="", landlordID!="", propID!="", comment!="", rating!=""]):
			Ratings.objects.create(authorID=authorID, landlordID=landlordID, 
									propID=propID, comment=comment, rating=rating)

	def setUp(self):
		self.create_rating(1, 1, 1, "Landlord 1's property 1", 3)
		self.create_rating(2, 1, 2, "Landlord 1's property 2", 2)
		self.create_rating(3, 2, 3, "Landlord 2's property 3", 4)
		self.create_rating(4, 2, 4, "Landlord 2's property 4", 5)
		self.valid_payload = {
			'authorID': '5', 
			'landlordID': '2', 
			'propID': '4', 
			'comment': 'Also lived in property 4 from landlord 2, another comment', 
			'rating': '5'
        }
		self.invalid_payload = {
        	'authorID': '', 
			'landlordID': '', 
			'propID': '', 
			'comment': 'This comment should not appear', 
			'rating': ''
        }

class RatingTests(BaseRatingsTest):
	def test_get_all_ratings(self):
		response = self.client.get(
            reverse("ratings-all")
        )
		expected = Ratings.objects.all()
		serialized = RatingsSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_valid_rating(self):
		response = self.client.post(
            reverse('ratings-all'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
		for x in Ratings.objects.all():
			print(x)
		self.assertEqual(len(Ratings.objects.all()), 5)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_invalid_rating(self):
		response = self.client.post(
            reverse('ratings-all'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
		self.assertEqual(len(Ratings.objects.all()), 4)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)