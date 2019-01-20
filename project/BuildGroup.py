import networkx as nx
import itertools
from .models import Groups 

def buildGroup(EventID, GroupList):
	g = Groups()
	for i in GroupList:
		g.addUser(i)
	g.linkedEventId = EventID
	g.save()
	return g