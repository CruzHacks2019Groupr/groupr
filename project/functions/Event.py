import networkx as nx
import matplotlib as mpl

class Event:
	#Event member variables:
	#	DG: Graph of users and their connections

	def __init__(self):
		self.DG = nx.DiGraph()

	def add_user(self, userId):
		self.DG.add_node(userId)

	def add_edge(self, sourceUser, destinationUser):
		self.DG.add_edge(sourceUser, destinationUser)

	#Returns list of ints
	def export_users(self):
		nodesList = list(self.DG.nodes(self.DG))

		for x in range(len(nodesList)):
			nodesList[x] = nodesList[x][0]

		return nodesList

	#Returns list of int tuples
	def export_edges(self):
		return list(self.DG.edges(self.DG))

	#Draws graph
	def visualize(self):
		nx.draw_networkx(self.DG)