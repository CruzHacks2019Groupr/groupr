#import everything we need
import networkx as nx

def findPerfectGroup(int) #takes in a UserID and finds if a perfect group exists via DFS

	#Load userID Have Eric write this part
	G = nx.Graph()
	# N = Node of the UserID
	D = G.to_undirected()
	List = cliques_containing_node(D, nodes=None)
	if not List
		return None;
	else
		return List[0];