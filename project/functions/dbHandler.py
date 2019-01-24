from ..models import Graph, Node, Edge

#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_one/
#https://docs.djangoproject.com/en/2.1/topics/db/examples/many_to_many/

#=========== event functions ===============
#create event



#get user and nodes


#set user


#set node


#add user


#update event info



#graph functions (private?)

#creates graph and returns id
def createGraph():
	g = Graph()
	g.save()
	return g.id

#takes id and prints graph
def printGraph(graph_id):
	g = Graph.objects.get(id=graph_id)
	print(g)

#add user id node to graph
def addNodeToGraph(graph_id, usr_id, silent = False):

	graph = Graph.objects.get(id=graph_id)
	if graph.node_set.filter(userId=usr_id):
		if not silent:
			print("Error, graph", graph_id, "already has node", usr_id)
		return
	n = Node(userId=usr_id, graph=graph)
	n.save()


def addEdgeToGraph(graph_id, usr_id1, usr_id2):
	graph = Graph.objects.get(id=graph_id)
	#create nodes if it doesn't have them
	addNodeToGraph(graph_id, usr_id1, silent=True)
	addNodeToGraph(graph_id, usr_id2, silent=True)

	#check if already exists
	if graph.edge_set.filter(a=usr_id1, b=usr_id2):
		print("Error, graph", graph_id, "already has edge (", usr_id1, ", ", usr_id2, ")")
		return
	e = Edge(a=usr_id1, b=usr_id2, graph=Graph.objects.get(id=graph_id))
	e.save()

