#import everything we need
import networkx as nx

def newSwipe(ID_1, ID_2) #Update swipe occurs, giving a first and second ID

	#DiG is digraph from database
	#G is undirected graph from database
	DiG.add_edge(ID_1, ID_2)
	if ID_1 in DiG.neighbors(ID_2)
		G.add_edge(ID_1, ID_2)
	List = cliques_containing_node(G, nodes=None)
	if not List
		return None;
	else
		for i in List[0]:
			G.remove_node(i)
			DiG.remove_node(i)
		return List[0];