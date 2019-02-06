from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
import random, string

import os
from django.core.validators import int_list_validator

# Create your models here.


class Graph(models.Model):
	def __str__(self):
		return("Nodes: " + str(self.node_set.all()) + " Edges: " + str(self.edge_set.all()))


class Event(models.Model):
	def __str__(self):
		return str(self.id)

	name = models.TextField(max_length=50)
	description = models.TextField(max_length=200)
	group_size = models.IntegerField()
	owner = models.IntegerField( default=0)
	#not actually checked for uniqueness, pls fix
	addCode = models.CharField(max_length=10)


	di = models.OneToOneField(
		Graph,
		on_delete=models.CASCADE,
		related_name = 'di',
	)
	
	undi = models.OneToOneField(
		Graph,
		on_delete=models.CASCADE,
		related_name = 'undi',
	)
	

#Edge (a,b)
class Edge(models.Model):
	a = models.IntegerField()
	b = models.IntegerField()

	graph = models.ForeignKey(Graph, on_delete=models.CASCADE)

	def __str__(self):
		return (str(self.a) + ", " + str(self.b))

	def tuple(self):
		return (self.a, self.b)

#Node just holds the user id
class Node(models.Model):
	userId = models.IntegerField()
	graph = models.ForeignKey(Graph, on_delete=models.CASCADE)

	def __str__(self):
		return(str(self.userId))

#this is the user profile
class Profile(models.Model):
	user = models.OneToOneField(User, on_delete=models.CASCADE)
	name = models.TextField(max_length=30, blank=True,null=True)
	bio = models.TextField(max_length=500,blank=True,null=True)

	age = models.IntegerField(blank=True,null=True)
	pic = models.ImageField(upload_to = 'static/uploads/', default = 'static/uploads/no-img.jpg')


	@receiver(post_save, sender=User)
	def create_user_profile(sender, instance, created, **kwargs):
		if created:
			Profile.objects.create(user=instance)

	@receiver(post_save, sender=User)
	def save_user_profile(sender, instance, **kwargs):
		instance.profile.save()

#this is the profile tied to each event
class EventProfile(models.Model):
	# using foreignkeys because I'm a good boy
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	event = models.ForeignKey(Event, on_delete=models.CASCADE)

	#store as JSON
	customInfo = models.TextField(max_length=2000, default="{}")

#the much-feared manyToMany
class Group(models.Model):
	event = models.ForeignKey(Event, on_delete=models.CASCADE)
	users = models.ManyToManyField(EventProfile)
	title = models.TextField(max_length=50,blank=True,null=True)
	uniqueHash = models.TextField(max_length=10)
	customInfo = models.TextField(max_length=2000, default="{}")

class GroupVote(models.Model):
	user = models.ForeignKey(Profile, on_delete=models.CASCADE)
	group = models.ForeignKey(Group, on_delete=models.CASCADE)
	vote = models.IntegerField(blank=True,null=True)