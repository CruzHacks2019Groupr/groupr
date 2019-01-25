from ..models import Graph, Node, Edge, Event
from django.db.models import Q
import networkx as nx

#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_one/
#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_many/



class UserHandler:
	#returns a list of all events (as EventHandlers) that the user owns
	@staticmethod
	def getEventsOwner(usrId):
		db_events = Event.objects.filter(owner=usrId)
		eventHandlers = [EventHandler(e.id) for e in db_events]
		return eventHandlers



#=========== event functions ===============
class EventHandler:
	#create event
	@staticmethod
	def createEvent(name, groupSize, creator):
		e = Event()
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
		self.event = Event.objects.get(id=event_id)
		self.id = self.event.id
		self.di = GraphHandler(self.event.di.id)
		self.undi = GraphHandler(self.event.undi.id)
		self.name = self.event.name
		self.groupSize = self.event.group_size

	def __str__(self):
		return ("Event Name: " + self.event.name + " ID: " + str(self.id))

	def export_users(self):
		return self.di.getNodes()

	def add_user(self, userId):
		self.di.addNode(userId)
		self.undi.addNode(userId)

	def remove_user(self, userId):
		self.di.deleteNode(userId)
		self.undi.deleteNode(userId)

	def add_edge(self, sourceUser, destinationUser):
		self.di.addEdge(sourceUser, destinationUser)

		#Checks if inverse edge exists in DG
		if (destinationUser, sourceUser) in self.di.getEdges():
			self.undi.addEdge(destinationUser, sourceUser)

	def remove_edge(self, sourceUser, destinationUser):
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
		#deeeeeeeep
		#also this will throw an error if you try to do anything with it so be careful
		

	#get/set user profile


	#update event info

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
