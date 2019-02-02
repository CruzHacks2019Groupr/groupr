from ..models import Graph, Node, Edge, Event, EventProfile, Profile, Group
from django.db.models import Q
from django.contrib.auth.models import User
import networkx as nx
import random, string, json

#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_one/
#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_many/


def genHash(len):
	return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(len))


class GroupHandler:

	@staticmethod
	#takes the list of UserHandlers and an eventHandler
	def createGroup(usersList, event):
		g = Group()

		g.uniqueHash = genHash(8)
		while Group.objects.filter(uniqueHash=g.uniqueHash):
			g.uniqueHash = genHash(8)

		g.event = event.event
		g.save()
		for user in usersList:
			g.users.add(user._getEventProfile(event))
		g.save()
		return GroupHandler(g.id)

	def __init__(self, groupId):
		if type(groupId) is GroupHandler:
			groupId = groupId.id
		self.id = groupId
		self.group = Group.objects.get(id=groupId)
		self.event = EventHandler(self.group.event.id)

	def __str__(self):
		return("Group: " + str(self.id) + " part of Event: " + str(self.event.id))

	def __repr__(self):
		return str(self)

	#returns a list of UserHandler objects
	def getUsers(self):
		#EventProfile objects
		users = self.group.users.all()
		#This is getting messy. Hopefully this will be the worst of it.
		#EventProfile -> Profile -> User -> UserHandler
		return [UserHandler(u.user.user.id) for u in users]


class UserHandler:

	def __init__(self, userId):
		if type(userId) is UserHandler:
			userId = userId.id
		try:
			self.id = userId
			self.user = User.objects.get(id=userId)
			self.profile = self.user.profile
			self.exists = True
		except User.DoesNotExist:
			self.exists = False
		

	def __str__(self):
		return("User: " + self.getName() + " ID: " + str(self.id))

	def __repr__(self):
		return str(self)

	def getEventsOwner(self):
		db_events = Event.objects.filter(owner=self.id)
		eventHandlers = [EventHandler(e.id) for e in db_events]
		return eventHandlers

	def getEvents(self):
		all_events = Event.objects.all()
		userEvents = []
		for e in all_events:
			eh = EventHandler(e.id)
			if self.id in eh.getUserIds():
				userEvents.append(eh)
		return userEvents

	def joinEvent(self, addCode):
		addCode = addCode.strip()
		try:
			e = Event.objects.get(addCode=addCode)
		except Event.DoesNotExist:
			return
		ev = EventHandler(e.id)
		ev._addUserToGraph(self.id)
		ep = EventProfile()
		ep.user = self.profile
		ep.event = ev.event
		ep.save()
		self.setCustomInfo(ev, {})

	#takes eventHandler, returns dict of custom info
	def getCustomInfo(self, ev):
		ev = EventHandler(ev)
		eventProfile = self._getEventProfile(ev)
		info = eventProfile.customInfo
		if info is not "":
			return json.loads(info)
		else:
			return {}

	#takes eventHandler and a dict
	def setCustomInfo(self, ev, d):
		ev = EventHandler(ev)
		info = json.dumps(d)
		eventProfile = self._getEventProfile(ev)
		eventProfile.customInfo = info
		eventProfile.save()

	def getBio(self):
		return self.profile.bio

	def setBio(self, bio):
		self.profile.bio = bio
		self/profile.bio.save()

	def getName(self):
		if self.profile.name is not None:
			return self.profile.name
		return self.user.username

	def setName(self, name):
		self.profile.name = name
		self.profile.save()

	def getGroups(self):
		groups = Group.objects.filter(users__id=self.id)
		return [GroupHandler(g.id) for g in groups]

		#Takes EventHandler object, returns reference to db. Don't use this
	def _getEventProfile(self, ev):
		ep = EventProfile.objects.get(event=ev.event, user=self.profile)
		return ep



#=========== event functions ===============
class EventHandler:
	#create event
	@staticmethod
	def createEvent(name, groupSize, creator):
		e = Event()

		e.addCode = genHash(5)
		while Event.objects.filter(addCode=e.addCode):
			e.addCode = genHash(5)
			

		e.name = name
		e.group_size = groupSize
		di = Graph()
		di.save()
		undi = Graph()
		undi.save()
		e.di = di
		e.undi = undi
		e.owner = creator
		e.save()
		return EventHandler(e.id)

	def __init__(self, event_id):
		if type(event_id) is EventHandler:
			event_id = event_id.id
		self.event = Event.objects.get(id=event_id)
		self.id = self.event.id
		self.di = GraphHandler(self.event.di.id)
		self.undi = GraphHandler(self.event.undi.id)
		self.name = self.event.name
		self.groupSize = self.event.group_size
		self.addCode = self.event.addCode

	def __str__(self):
		return ("Event Name: " + self.event.name + " ID: " + str(self.id) + " Add Code: " + self.addCode) 

	def __repr__(self):
		return str(self)

	#returns list of ids (depreciated)
	def getUserIds(self):
		return self.di.getNodes()

	#returns list of UserHandlers
	def getUsers(self):
		return [UserHandler(n) for n in self.di.getNodes()]

	#takes ids
	def addEdge(self, sourceUser, destinationUser):
		self.di.addEdge(sourceUser, destinationUser)

		#Checks if inverse edge exists in DG
		if (destinationUser, sourceUser) in self.di.getEdges():
			self.undi.addEdge(destinationUser, sourceUser)

	#takes ids
	def removeEdge(self, sourceUser, destinationUser):
		self.di.deleteEdge(sourceUser, destinationUser)
		undiEdges = self.undi.getEdges()
		if (destinationUser, sourceUser) in undiEdges:
			self.undi.deleteEdge(destinationUser, sourceUser)
		if (sourceUser, destinationUser) in undiEdges:
			self.undi.deleteEdge(sourceUser, destinationUser)

	def G(self):
		g = nx.parse_edgelist(self.undi.getNodes())
		return g

	def DG(self):
		dg = nx.parse_edgelist(self.di.getNodes())
		return dg

	def delete(self):
		self.event.delete()
		self.event = None
		self.id = None
		self.name = None
		self = None
		#also this will throw an error if you try to do anything with the object after deletion so be careful

	def getGroups(self):
		groups = Group.objects.filter(event=self.event)
		return [GroupHandler(g.id) for g in groups]
	#get/set user profile

	def addUser(self, userId):
		UserHandler(userId).joinEvent(self.addCode)


	#DO NOT USE, use addUser
	def _addUserToGraph(self, userId):
		self.di.addNode(userId)
		self.undi.addNode(userId)

	#DO NOT USE (unless you really mean to)
	def _removeUserFromGraph(self, userId):
		self.di.deleteNode(userId)
		self.undi.deleteNode(userId)



	#update event info

#Don't use this class unless you really need to
class GraphHandler:
	def __init__(self, graph_id=None):
		if(graph_id is None):
			self.graph = Graph()
			self.graph.save()
		else:
			self.graph = Graph.objects.get(id=graph_id)
		self.id = self.graph.id

	#takes id and prints graph
	def print(self):
		print(self.graph)

	def __str__(self):
		return str(self.graph)

	#add user id node to graph
	def addNode(self, usr_id, silent = False):
		if self.graph.node_set.filter(userId=usr_id):
			if not silent:
				print("Error, graph", self.id, "already has node", usr_id)
			return
		n = Node(userId=usr_id, graph=self.graph)
		n.save()


	def addEdge(self, usr_id1, usr_id2):

		#create nodes if it doesn't have them
		self.addNode(usr_id1, silent=True)
		self.addNode(usr_id2, silent=True)

		#stay safe kids
		if usr_id1 == usr_id2:
			return

		#check if already exists
		if self.graph.edge_set.filter(a=usr_id1, b=usr_id2):
			print("Error, graph", self.id, "already has edge (", usr_id1, ", ", usr_id2, ")")
			return
		e = Edge(a=usr_id1, b=usr_id2, graph=self.graph)
		e.save()


	#Deletes node. First deletes edges
	def deleteNode(self, usr_id, silent=False):
		try:
			n = self.graph.node_set.get(userId=usr_id)
			n.delete()
			edgesToDelete = self.graph.edge_set.filter(Q(a=usr_id) | Q(b=usr_id))
			for e in edgesToDelete:
				e.delete()
		except Node.DoesNotExist:
			if not silent:
				print("NODE ", usr_id, " DOES NOT EXIST IN GRAPH")

	#deletes an edge. Does not delete underlying nodes.
	def deleteEdge(self, usr_id1, usr_id2, silent=False):
		try:
			e = self.graph.edge_set.get(a=usr_id1, b=usr_id2)
			e.delete()
		except Edge.DoesNotExist:
			if not silent:
				print("Edge (", usr_id1, ", ", usr_id2, ")",  " DOES NOT EXIST IN GRAPH")

	#list of ints
	def getNodes(self):
		nodes = [n.userId for n in self.graph.node_set.all()]
		return nodes

	#returns a list of tuples
	def getEdges(self):
		edges = [e.tuple() for e in self.graph.edge_set.all()]
		return edges
