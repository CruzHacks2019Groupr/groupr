from django.db import models
from django.contrib.auth.models import AbstractUser
#import networkx as nx

# Create your models here.

class Test(models.Model):
	count = models.IntegerField(default=0)

#class User(AbstractUser):
#	bio = models.TextField(max_length=500, blank=True)
#	birth_date = models.DateField(null=True, blank=True)
	#pic = models.ImageField(null=True)

#class Event(models.Model):
#	name = models.TextField(max_length=20)
#	group_size = models.IntegerField()


