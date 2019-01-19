from django.db import models
from django.contrib.auth.models import AbstractUser
#import networkx as nx


from django.core.validators import int_list_validator

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


class Graph(models.Model):
	nodes = models.CharField(max_length=500)
	edges_a = models.CharField(max_length=5000)
	edges_b = models.CharField(max_length=5000)
	def __str__(self):
		pass
	def getEdges(self):
		a = [int(i) for i in self.edges_a.split(' ')]
		b = [int(i) for i in self.edges_b.split(' ')]
		return list(zip(a, b))

	def setEdges(self, edges):
		(a, b) = list(zip(*edges))

		self.edges_a = ' '.join(map(str,a))
		self.edges_b = ' '.join(map(str,b))

	def getNodes(self):
		return list([int(i) for i in self.nodes.split(' ')])

	def setNodes(self, nodes):
		self.nodes = ' '.join(map(str,nodes))
