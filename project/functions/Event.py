import networkx as nx

class Event:
	#Event member variables:
	#	name: Event name
	#	DG: Graph of users and their connections

	def __init__(self):
		self DG = nx.DiGraph()

	def add_user(userId):
		DG.add_node(userId)

	def add_edge(sourceUser, destinationUser):
		DG.add_edge(sourceUser, destinationUser)