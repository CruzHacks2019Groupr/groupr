from ..models import Graph, Node, Edge, Event, EventProfile, Profile, Group, GroupVote
from django.db.models import Q
from django.contrib.auth.models import User
import networkx as nx
import random, string, json


from django.contrib.auth.models import User
#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_one/
#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_many/

def genHash(len):
	return ''.join(random.choice(string.ascii_uppercase + string.ascii_lowercase + string.digits) for _ in range(len))

def dropAllTables():
	#delete groups
	groups = Group.objects.all()
	for g in groups:
		g.delete()

	eventProfiles = EventProfile.objects.all()
	for e in eventProfiles:
		e.delete()

	events = Event.objects.all()
	for e in events:
		e.delete()
	
	users = User.objects.all()
	for u in users: 
		u.delete()

#Deletes everything but userId passed
def dropMostTables(userId):
	#delete groups
	groups = Group.objects.all()
	for g in groups:
		g.delete()

	eventProfiles = EventProfile.objects.all()
	for e in eventProfiles:
		e.delete()

	events = Event.objects.all()
	for e in events:
		e.delete()
	
	users = User.objects.all()
	for u in users: 
		if u.id != userId:
			u.delete()


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
			g.users.add(UserHandler(user)._getEventProfile(event))
		g.save()
		g = GroupHandler(g)
		g.setCustomInfo({})
		return GroupHandler(g.id)


	def __init__(self, groupId):
		if type(groupId) is GroupHandler:
			groupId = groupId.id
		self.id = groupId
		try:
			self.group = Group.objects.get(id=groupId)
			self.event = EventHandler(self.group.event.id)
			self.hash = group.uniqueHash
			self.exists = True
			if self.event.exists == False:
				self.exists = False
		except Group.DoesNotExist:
			self.exists = False

		
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

	#returns dict of custom info
	def getCustomInfo(self):
		info = self.group.customInfo
		if info is not "":
			return json.loads(info)
		else:
			return {}

	#takes  a dict
	def setCustomInfo(self, d):
		info = json.dumps(d)
		self.group.customInfo = info
		group.save()

	#lets a user vote
	def userVote(self, user, boolean):
		user = UserHandler(user)
		try:
			vote = GroupVote.objects.get(group=self.group, user=user.profile)
		except GroupVote.DoesNotExist:
			vote = GroupVote()
		vote.user = user.profile
		vote.group = self.group
		vote.vote = boolean
		vote.save()

	#returns dict of users' votes
	def getVotes(self):
		votes = GroupVote.objects.filter(group=self.group)
		allVotes = {}
		for v in votes:
			allVotes[str(v.user.user.id)] = v.vote
		return allVotes

	def delete(self):
		self.group.delete()
		self.exists = False


class UserHandler:

	@staticmethod
	def createUser(username, password):
		user = User.objects.create_user(username=username,
		password=password)
		user.save()
		return UserHandler(user.id)

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
		#check if user is already in the event
		if self.id in ev.getUserIds():
			return
		ev._addUserToGraph(self.id)
		ep = EventProfile()
		ep.user = self.profile
		ep.event = ev.event
		ep.save()
		self.setCustomInfo(ev, {})
		generateList(ev, self.id)
		userJoinedEvent(ev, self.id)
		

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
		eventProfile.save(force_update=True)

	def getBio(self):
		return self.profile.bio

	def setBio(self, bio):
		self.profile.bio = bio
		self.profile.bio.save()

	def getName(self):
		if self.profile.name is not None:
			return self.profile.name
		return self.user.username

	def setName(self, name):
		self.profile.name = name
		self.profile.save()

	def getGroups(self, event=None):
		groups = Group.objects.filter(users__id=self.id)
		if(event is not None):
			event = EventHandler(event)
			if event.exists:
				groups = [g for g in groups if g.event == event.event]
		return [GroupHandler(g.id) for g in groups]

		#Takes EventHandler object, returns reference to db. Don't use this

	def delete(self):
		self.profile.delete()

	def _getEventProfile(self, ev):
		ep = EventProfile.objects.get(event=ev.event, user=self.profile)
		return ep

#================= Helper funcs for list generation ================
def userJoinedEvent(e, userID):
	event = EventHandler(e)
	user = UserHandler(userID)

	users = event.getUsers()
	for u in users:
		if u.id != user.id:
			profile = u.getCustomInfo(event)			
			rec = profile["reccomendList"]
			rec.append(user.id)
			profile["reccomendList"] = rec
			u.setCustomInfo(event, profile)

def generateList(e, userID):
	event = EventHandler(e)
	user = UserHandler(userID)
	profile = user.getCustomInfo(event)
	profile["reccomendList"] = event.getUserIds()
	user.setCustomInfo(event, profile)

	return profile["reccomendList"]

#=================================================

#=========== event functions ===============
class EventHandler:
	#create event
	@staticmethod
	def createEvent(name, desc, groupSize, creator):
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
		e.description = desc
		e.save()
		return EventHandler(e.id)

	def __init__(self, event_id):
		if type(event_id) is EventHandler:
			event_id = event_id.id
		try:
			self.event = Event.objects.get(id=event_id)
			self.owner = self.event.owner
			self.id = self.event.id
			self.di = GraphHandler(self.event.di.id)
			self.undi = GraphHandler(self.event.undi.id)
			self.name = self.event.name
			self.groupSize = self.event.group_size
			self.addCode = self.event.addCode
			self.description = self.event.description
			self.exists = True
		except Event.DoesNotExist:
			self.exists = False

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
		g = nx.Graph()
		g.add_nodes_from(self.undi.getNodes())
		g.add_edges_from(self.undi.getEdges())
		return g

	def DG(self):
		dg = nx.Graph()
		dg.add_nodes_from(self.di.getNodes())
		dg.add_edges_from(self.di.getEdges())
		return dg

	def delete(self):
		self.event.delete()
		self.event = None
		self.id = None
		self.name = None
		self.exists = False
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
