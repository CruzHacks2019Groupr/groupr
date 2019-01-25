from ..models import Graph, Node, Edge, Event

#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_one/
#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_many/

#=========== event functions ===============
class EventHandler:
	#create event
	def __init__(self, event_id=None):
		if(event_id is None):
			self.event = Event()
			self.event.save()
			self.event.di = Graph()
			self.event.di.save()
			self.event.undi = Graph()
			self.event.undi.save()
		else:
			pass


	#add user


	#delete user


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

		#check if already exists
		if self.graph.edge_set.filter(a=usr_id1, b=usr_id2):
			print("Error, graph", self.id, "already has edge (", usr_id1, ", ", usr_id2, ")")
			return
		e = Edge(a=usr_id1, b=usr_id2, graph=self.graph)
		e.save()


	#Deletes node. DOES NOT CHECK FOR PREEXISTING EDGES! BE CAREFUL!
	def deleteNode(self, usr_id, silent=False):
		try:
			n = self.graph.node_set.get(userId=usr_id)
			n.delete()
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
