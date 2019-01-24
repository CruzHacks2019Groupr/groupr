from ..models import Graph, Node, Edge


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
	pass

#add user id node to graph
def addNodeToGraph(graph_id, usr_id):
	n = Node(userId=usr_id, graph=Graph.objects.get(id=graph_id))
	n.save()


def addEdgeToGraph(id, usr_id):
	pass
