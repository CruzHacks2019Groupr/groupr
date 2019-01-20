from django.db import models
from django.contrib.auth.models import AbstractUser
import models.graph as Graph
#import networkx as nx


from django.core.validators import int_list_validator

# Create your models here.

class Test(models.Model):
	count = models.IntegerField(default=0)

#class User(AbstractUser):
#	bio = models.TextField(max_length=500, blank=True)
#	birth_date = models.DateField(null=True, blank=True)
#	pic = models.ImageField(null=True)

class Event(models.Model):
	name = models.TextField(max_length=50)
	group_size = models.IntegerField()
	di = models.OneToOneField(
        Graph,
        on_delete=models.PROTECT,
    )
	undi = models.OneToOneField(
        Graph,
        on_delete=models.PROTECT,
    )
	users = models.CharField(max_length=5000, default='')
	creator = models.CharField(max_length=150, blank=False)
	userson = models.CharField(max_length=5000, default='')

	def getUsers():
		a = users.split(' ')

	def getUsersOn():
		a = userson.split(' ')