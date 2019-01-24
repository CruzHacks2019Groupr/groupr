from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
#import project.models_.graph as Graph
#import networkx as nx

import os
from django.core.validators import int_list_validator

# Create your models here.


class Graph(models.Model):
	nodes = models.CharField(max_length=500)
	edges_a = models.CharField(max_length=5000)
	edges_b = models.CharField(max_length=5000)
	def __str__(self):
		return("Nodes: " + str(self.node_set.all()) + " Edges: " + str(self.edge_set.all()))

	def getEdges(self):
		if len(self.edges_a) == 0:
			return[]
		else:
			a = [int(i) for i in self.edges_a.split(' ')]

		if len(self.edges_b) == 0:
			return[]
		else:
			b = [int(i) for i in self.edges_b.split(' ')]
		return list(zip(a, b))

	def setEdges(self, edges):
		(a, b) = list(zip(*edges))

		self.edges_a = ' '.join(map(str,a))
		self.edges_b = ' '.join(map(str,b))

	def getNodes(self):
		if len(self.nodes) == 0:
			return []
		else:
			return list([int(i) for i in self.nodes.split(' ')])

	def setNodes(self, nodes):
		self.nodes = ' '.join(map(str,nodes))
		self.save()



class Event(models.Model):
	def __str__(self):
		return str(self.id)

	name = models.TextField(max_length=50)
	group_size = models.IntegerField()
	di = models.OneToOneField(
		Graph,
		on_delete=models.PROTECT,
		related_name = 'di',
	)
	
	undi = models.OneToOneField(
		Graph,
		on_delete=models.PROTECT,
		related_name = 'undi',
	)
	
	users = models.CharField(max_length=5000, default="", blank = True) #optional
	creator = models.CharField(max_length=150, blank=False)
	userson = models.CharField(max_length=5000, default="", blank = True) #optional

	def getUsers(self):

		a = self.users.split(' ')
		if(len(a) == 0 or self.users == ""):
			return []
		for i in range(len(a)):
			a[i] = int(a[i])
		return a

	def getUsersOn(self):
		a = self.userson.split(' ')
		for i in range(len(a)):
			a[i] = int(a[i])
		return a

	def setUserOn(self, pos, num):
		print(self.userson)
		a = self.userson.split(' ')
		a[pos] = num
		self.userson = ' '.join(str(x) for x in a)
		self.save()

	def addUser(self, id):
		if len(self.getUsers()) == 0:
			print(self.users)
			self.users = self.users + str(id)
			self.userson = self.userson + str(-1)
		elif len(self.getUsers()) == 1:
			self.users = self.users + " " + str(id)
			self.userson = self.userson + " " + str(0)
			self.setUserOn(0,1)
		else:
			self.users = self.users + " " + str(id)
			self.userson = self.userson + " " + str(0)
		self.save()





#Edge (a,b)
class Edge(models.Model):
	a = models.IntegerField()
	b = models.IntegerField()

	graph = models.ForeignKey(Graph, on_delete=models.CASCADE)

	def __str__(self):
		return (str(self.a) + ", " + str(self.b))

#Node just holds the user id
class Node(models.Model):
	userId = models.IntegerField()
	graph = models.ForeignKey(Graph, on_delete=models.CASCADE)

	def __str__(self):
		return(str(self.userId))




class Groups(models.Model):
	linkedEventId = models.TextField(max_length=50)
	users = models.CharField(max_length=5000);

	def getEventId(self):
		return self.linkedEventId

	def getUsers(self):
		a = self.users.split(' ')
		return a

	def addUser(self, id):
		if len(self.users) == 0:
			self.users = self.users + id
		else:
			self.users = self.users + " " + id
		self.save()

class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	bio = models.TextField(max_length=500,blank=True,null=True)
	age = models.IntegerField(blank=True,null=True)
	#pic = models.ImageField(upload_to = 'demo/', default = 'demo/no-img.jpg')

	def getBio(self):
		return self.bio
	def setBio(self,id):
		self.bio=id
	def getAge(self):
		return self.age
	def getPicture(self):
		return self.pic.url
	
	def test(self):
		print("test")


	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()