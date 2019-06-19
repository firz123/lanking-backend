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


class BaseLandlordTest(APITestCase):
	client = APIClient()
	@staticmethod
	def create_landlord(first="", last=""):
		if first != "" and last != "":
			Landlord.objects.create(first=first, last=last, 
				avg_rating=None, sum_rating=0, num_rating=0)

	def setUp(self):
		self.create_landlord("John", "Doe")
		self.create_landlord("Jane", "Doe")
		self.create_landlord("Andrew", "Smith")
		self.create_landlord("Abby", "Smith")
		self.valid_payload = {
			'first': 'Jane',
			'last': 'Smith'
        }
		self.invalid_payload = {
        	'first': '',
        	'last': '',
        }

class BaseRatingsTest(BaseLandlordTest):
	@staticmethod
	def create_rating(author_id="", landlord_id="", 
		prop_id="", comment="", rating=""):
		if all([author_id!="", landlord_id!="", prop_id!="", comment!="", rating!=""]):
			Rating.objects.create(author_id=author_id, landlord_id=landlord_id, 
									prop_id=prop_id, comment=comment, rating=rating)

	def setUp(self):
		self.create_landlord("John", "Smith")
		self.create_landlord("Jane", "Doe")
		self.ll_ids = []
		for ll in Landlord.objects.all():
			self.ll_ids.append(ll.id)
		self.ll_ids.sort()
		self.create_rating(1, self.ll_ids[0], 1, "rating 1", 3)
		self.create_rating(2, self.ll_ids[0], 2, "rating 2", 2)
		self.create_rating(3, self.ll_ids[1], 3, "rating 3", 4)
		self.create_rating(4, self.ll_ids[1], 4, "rating 4", 5)
		self.valid_payload = {
			'author_id': '5', 
			'landlord_id': '' + str(self.ll_ids[1]), 
			'prop_id': '4', 
			'comment': 'Also lived in property 4 from landlord 13, another comment', 
			'rating': '5'
        }
		self.invalid_payload = {
        	'author_id': '', 
			'landlord_id': '', 
			'prop_id': '', 
			'comment': 'This comment should not appear', 
			'rating': ''
        }

class BasePropertyTest(BaseRatingsTest):
	@staticmethod
	def create_property(add="", city="", 
		zipcode="", state="", ll_id=""):
		if all([add!="", city!="", zipcode!="", state!="", ll_id!=""]):
			prop = Property(landlord_id=ll_id, addressline=add, 
							city=city, state=state, zipcode=zipcode)
			landlord = Landlord.objects.get(id__exact=ll_id)
			landlord.save()
			prop.save()
			landlord.properties.add(prop)

	def setUp(self):
		self.create_landlord("John", "Doe")
		self.create_landlord("Jane", "Doe")
		self.create_landlord("Andrew", "Smith")
		self.create_landlord("Abby", "Smith")
		self.ll_ids = []
		for ll in Landlord.objects.all():
			self.ll_ids.append(ll.id)
		self.ll_ids.sort()
		self.create_property("122 Sample St.", "Townville", 
			"00000", "AL", str(self.ll_ids[0]))
		self.create_property("456 Block Boulevard", "Cityopolis", 
			"11111", "NY", str(self.ll_ids[1]))
		self.create_property("67 Center Ct.", "Suburb", 
			"22222", "CA", str(self.ll_ids[2]))
		self.create_property("789 Road Rd.", "Placeville", 
			"33333", "TX", str(self.ll_ids[3]))
		self.prop_ids = []
		for prop in Property.objects.all():
			self.prop_ids.append(prop.id)
		self.prop_ids.sort()
		self.create_rating(1, str(self.prop_ids[0]), 1, "rating 1", 3)
		self.create_rating(2, str(self.prop_ids[0]), 2, "rating 2", 2)
		self.create_rating(3, str(self.prop_ids[1]), 3, "rating 3", 4)
		self.create_rating(4, str(self.prop_ids[1]), 4, "rating 4", 5)
		self.valid_payload = {
			'landlord_id': '' + str(self.ll_ids[0]), 
			'addressline': '123 Example St.', 
			'city': 'Townville', 
			'state': 'AL', 
			'zipcode': '00000'
        }
		self.invalid_payload = {
        	'landlord_id': '', 
			'addressline': '', 
			'city': '', 
			'state': '', 
			'zipcode': ''
        }

class CreateLandlordTest(BaseLandlordTest):
	def test_create_valid_landlord(self):
		response = self.client.post(
            reverse('landlords'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
		self.assertEqual(len(Landlord.objects.all()), 5)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_invalid_landlord(self):
		response = self.client.post(
            reverse('landlords'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
		self.assertEqual(len(Landlord.objects.all()), 4)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class QueryLandlordTest(BaseLandlordTest):
	def test_query_landlords_first(self):
		response = self.client.get(
            reverse("landlords") + "?first=jane"
        )
		expected = Landlord.objects.filter(first__icontains="jane")
		serialized = LandlordSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_query_landlords_last(self):
		response = self.client.get(
            reverse("landlords") + "?last=doe"
        )
		expected = Landlord.objects.filter(last__icontains="Doe")
		serialized = LandlordSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_query_landlords_missing(self):
		response = self.client.get(
            reverse("landlords") + "?last=Johnson"
        )
		self.assertEqual(response.data, [])
		self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateRatingTests(BaseRatingsTest):
	def test_create_valid_rating(self):
		response = self.client.post(
            reverse('ratings'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
		self.assertEqual(Landlord.objects.get(id__exact=self.ll_ids[0]).avg_rating, None)
		self.assertEqual(Landlord.objects.get(id__exact=self.ll_ids[0]).num_rating, 0)
		self.assertEqual(Landlord.objects.get(id__exact=self.ll_ids[1]).avg_rating, 5)
		self.assertEqual(Landlord.objects.get(id__exact=self.ll_ids[1]).num_rating, 1)
		self.assertEqual(len(Rating.objects.all()), 5)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_invalid_rating(self):
		response = self.client.post(
            reverse('ratings'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
		self.assertEqual(len(Rating.objects.all()), 4)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class CreatePropertyTests(BasePropertyTest):
	def test_create_valid_property(self):
		response = self.client.post(
            reverse('properties'),
            data=json.dumps(self.valid_payload),
            content_type='application/json'
        )
		
		self.assertEqual(len(Landlord.objects.get(
			id__exact=self.ll_ids[0]).properties.all()), 2)
		self.assertEqual(len(Property.objects.all()), 5)
		self.assertEqual(response.status_code, status.HTTP_201_CREATED)

	def test_create_invalid_property(self):
		response = self.client.post(
            reverse('properties'),
            data=json.dumps(self.invalid_payload),
            content_type='application/json'
        )
		self.assertEqual(len(Property.objects.all()), 4)
		self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

class QueryLandlordIDTest(BasePropertyTest):
	def test_query_ratings_by_landlord(self):
		response = self.client.get(
            reverse("landlord-id") + 
            "?id=%d&get_ratings=true" % (self.ll_ids[0])
        )
		expected = Landlord.objects.get(id__exact=self.ll_ids[0]).ratings.all()
		serialized = RatingSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

	def test_query_properties_by_landlord(self):
		response = self.client.get(
            reverse("landlord-id") + 
            "?id=%d&get_properties=true" % (self.ll_ids[0])
        )
		expected = Landlord.objects.get(id__exact=self.ll_ids[0]).properties.all()
		serialized = PropertySerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

class QueryPropertyIDTest(BasePropertyTest):
	def test_query_landlord_by_property(self):
		response = self.client.get(
            reverse("property-id") + "?id=%d" % (self.prop_ids[0])
        )
		expected = Property.objects.get(id__exact=self.prop_ids[0]).landlord_set.all()
		serialized = LandlordSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)

class QueryUserRatingsTest(BasePropertyTest):
	def test_query_ratings_by_user(self):
		response = self.client.get(
            reverse("user-ratings") + "?id=1"
        )
		expected = Rating.objects.filter(author_id__exact=1)
		serialized = RatingSerializer(expected, many=True)
		self.assertEqual(response.data, serialized.data)
		self.assertEqual(response.status_code, status.HTTP_200_OK)