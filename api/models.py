from django.db import models
from django.contrib.auth.models import AbstractUser

# Create your models here.
class Rating(models.Model):
	author_id = models.IntegerField()
	landlord_id = models.IntegerField()
	prop_id = models.IntegerField()
	comment = models.CharField(max_length=800, null=True)
	rating = models.IntegerField()
	def __str__(self):
		return "rating: {}, landlord id: {}, author id: {} : {}".format(
			self.rating,
			self.landlord_id, 
			self.author_id, 
			self.comment)

class Property(models.Model):
	landlord_id = models.IntegerField(null=True)
	addressline = models.CharField(max_length=255, null=False)
	city = models.CharField(max_length=255, null=False)
	STATES = [
	    ('AL', 'Alabama'),
	    ('AK', 'Alaska'),
	    ('AZ', 'Arizona'),
	    ('AR', 'Arkansas'),
	    ('CA', 'California'),
	    ('CO', 'Colorado'),
	    ('CT', 'Connecticut'),
	    ('DE', 'Delaware'),
	    ('FL', 'Florida'),
	    ('GA', 'Georgia'),
	    ('HI', 'Hawaii'),
	    ('ID', 'Idaho'),
	    ('IL', 'Illinois'),
	    ('IN', 'Indiana'),
	    ('IA', 'Iowa'),
	    ('KS', 'Kansas'),
	    ('KY', 'Kentucky'),
	    ('LA', 'Louisiana'),
	    ('ME', 'Maine'),
	    ('MD', 'Maryland'),
	    ('MA', 'Massachusetts'),
	    ('MI', 'Michigan'),
	    ('MN', 'Minnesota'),
	    ('MS', 'Mississippi'),
	    ('MO', 'Missouri'),
	    ('MT', 'Montana'),
	    ('NE', 'Nebraska'),
	    ('NV', 'Nevada'),
	    ('NH', 'New Hampshire'),
	    ('NJ', 'New Jersey'),
	    ('NM', 'New Mexico'),
	    ('NY', 'New York'),
	    ('NC', 'North Carolina'),
	    ('ND', 'North Dakota'),
	    ('OH', 'Ohio'),
	    ('OK', 'Oklahoma'),
	    ('OR', 'Oregon'),
	    ('PA', 'Pennsylvania'),
	    ('RI', 'Rhode Island'),
	    ('SC', 'South Carolina'),
	    ('SD', 'South Dakota'),
	    ('TN', 'Tennessee'),
	    ('TX', 'Texas'),
	    ('UT', 'Utah'),
	    ('VT', 'Vermont'),
	    ('VA', 'Virginia'),
	    ('WA', 'Washington'),
	    ('WV', 'West Virginia'),
	    ('WI', 'Wisconsin'),
	    ('WY', 'Wyoming')
	]
	state = models.CharField(
        max_length=2,
        choices=STATES,
        default='CA'
    )
	zipcode = models.IntegerField()

	def __str__(self):
		return "{} {} {} {} owned by {}".format(self.addressline, 
              self.city, self.state, self.zipcode, self.landlord_id)

class UserAccount(AbstractUser):
	realnameVisible = models.BooleanField()
	def __str__(self):
		return "un: {}, name: {} (visible: {})".format(self.get_username(), 
              self.get_full_name(), self.realnameVisible)


class Landlord(models.Model):
	first = models.CharField(max_length=255, null=False)
	last = models.CharField(max_length=255, null=False)
	ratings = models.ManyToManyField(Rating)
	properties = models.ManyToManyField(Property)
	avg_rating = models.IntegerField(null=True)
	sum_rating = models.IntegerField(null=True)
	num_rating = models.IntegerField(null=True)

	def __str__(self):
		return "id: {} name: {} avgRating: {}, numRating: {}".format(self.id, 
			self.first + " " + self.last, self.avg_rating, self.num_rating)
	