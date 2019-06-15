import json
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APITestCase, APIClient
from rest_framework.views import status
from .models import UserAccount, Landlord, Rating, Property
from .serializers import UserSerializer, LandlordSerializer, RatingSerializer, PropertySerializer


class BaseUserTest(APITestCase):
	client = APIClient()
	@staticmethod
	def create_user(username="", password="", realnameVisible=""):
		if all([username!="", password!="", realnameVisible!=""]):
			UserAccount.objects.create(username=username, password=password, 
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
		expected = UserAccount.objects.all()
		serialized = UserSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

class BaseLandlordTest(APITestCase):
	client = APIClient()
	@staticmethod
	def create_landlord(name=""):
		if name != "":
			Landlord.objects.create(name=name, avgRating=None, sumRating=0, numRating=0)

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
		expected = Landlord.objects.all()
		serialized = LandlordSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_valid_landlord(self):
		response = self.client.post(
            reverse('landlords-all'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
		self.assertEqual(len(Landlord.objects.all()), 5)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_invalid_landlord(self):
		response = self.client.post(
            reverse('landlords-all'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
		self.assertEqual(len(Landlord.objects.all()), 4)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class BaseRatingsTest(APITestCase):
	client = APIClient()
	@staticmethod
	def create_rating(author_id="", landlord_id="", 
		prop_id="", comment="", rating=""):
		if all([author_id!="", landlord_id!="", prop_id!="", comment!="", rating!=""]):
			Rating.objects.create(author_id=author_id, landlord_id=landlord_id, 
									prop_id=prop_id, comment=comment, rating=rating)

	@staticmethod
	def create_landlord(name=""):
		if name != "":
			Landlord.objects.create(name=name, avgRating=None, sumRating=0, numRating=0)

	def setUp(self):
		self.create_landlord("ll1")
		self.create_landlord("ll2")
		self.create_rating(1, 16, 1, "Landlord 16's property 1", 3)
		self.create_rating(2, 16, 2, "Landlord 16's property 2", 2)
		self.create_rating(3, 17, 3, "Landlord 17's property 3", 4)
		self.create_rating(4, 17, 4, "Landlord 17's property 4", 5)
		self.valid_payload = {
			'author_id': '5', 
			'landlord_id': '17', 
			'prop_id': '4', 
			'comment': 'Also lived in property 4 from landlord 17, another comment', 
			'rating': '5'
        }
		self.invalid_payload = {
        	'author_id': '', 
			'landlord_id': '', 
			'prop_id': '', 
			'comment': 'This comment should not appear', 
			'rating': ''
        }

class RatingTests(BaseRatingsTest):
	def test_get_all_ratings(self):
		response = self.client.get(
            reverse("ratings-all")
        )
		expected = Rating.objects.all()
		serialized = RatingSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_create_valid_rating(self):
		response = self.client.post(
            reverse('ratings-all'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
		self.assertEqual(Landlord.objects.get(id__exact=16).avgRating, None)
		self.assertEqual(Landlord.objects.get(id__exact=16).numRating, 0)
		self.assertEqual(Landlord.objects.get(id__exact=17).avgRating, 5)
		self.assertEqual(Landlord.objects.get(id__exact=17).numRating, 1)
		self.assertEqual(len(Rating.objects.all()), 5)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_invalid_rating(self):
		response = self.client.post(
            reverse('ratings-all'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
		self.assertEqual(len(Rating.objects.all()), 4)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)