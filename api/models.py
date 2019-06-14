from django.db import models

# Create your models here.
class Users(models.Model):
	username = models.CharField(max_length=255, null=False)
	realnameVisible = forms.BooleanField(initial=True)
    realname = models.CharField(max_length=255, null=True)
    email = models.EmailField(max_length=70,blank=False)

    def __str__(self):
        return "un: {}, {} (visible: {})".format(self.username, self.realname, self.realnameVisible)

class Landlords(models.Model):
    name = models.CharField(max_length=255, null=False)
    def __str__(self):
        return "un: {}, {} (visible: {})".format(self.name)

class Ratings(models.Model):
	authorID = models.IntegerField()
	landlordID = models.IntegerField()
	propID = models.IntegerField()
	comment = models.CharField(max_length=800, null=True)
	rating = models.IntegerField()

    def __str__(self):
        return "{} of {}, by {} : {}".format(self.rating, self.landlordID, self.authorID, self.comment)

class Properties(models.Model):
	landlordID = models.IntegerField(null=True)
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
        	self.city, self.state, self.zipcode, self.landlordID)