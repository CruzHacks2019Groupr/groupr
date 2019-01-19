import networkx as nx
import matplotlib as mpl

class Event:
	#Event member variables:
	#	DG: Graph of users and their connections (Directed)
	#	G: Graph of users and their connections (Undirected, edge only exists if omnidirectional edge exists in DG)

	def __init__(self):
		self.DG = nx.DiGraph()
		self.G = nx.Graph()

	def add_user(self, userId):
		self.DG.add_node(userId)
		self.G.add_node(userId)

	def remove_user(self, userId):
		self.DG.remove_node(userId)
		self.G.remove_node(userId)

	def add_edge(self, sourceUser, destinationUser):
		self.DG.add_edge(sourceUser, destinationUser)

		#Checks if inverse edge exists in DG
		if (destinationUser, sourceUser) in self.DG.edges():
			self.G.add_edge(sourceUser, destinationUser)

	#Returns list of ints
	def export_users(self):
		nodesList = list(self.DG.nodes(self.DG))

		for x in range(len(nodesList)):
			nodesList[x] = nodesList[x][0]

		return nodesList

	#Returns list of int tuples
	def export_edges_directed(self):
		return list(self.DG.edges(self.DG))

	#Returns list of int tuples
	def export_edges_undirected(self):
		return list(self.G.edges(self.DG))

	#Draws graph
	def visualize(self):
		nx.draw_networkx(self.DG)