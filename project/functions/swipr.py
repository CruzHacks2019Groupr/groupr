from . import Event
from ..models import Event as EventModel
from .matcher import *

EVENT_ID = 1

def makeConnection(user1, user2):

	print("Making Connection Between ", str(user1), " and ", str(user2))
	print(EventModel.objects.all())
	obj = EventModel.objects.get(id=EVENT_ID)

	#Creates Event object from EventModel
	testEvent = Event(obj.di.getNodes(), obj.di.getEdges())
	
	for x in range(1,21):
		testEvent.add_user(x);

	testEvent.add_edge(user1, user2)

	#DEBUG#
	print("Graph dump:")
	print(testEvent.export_users())
	print(testEvent.export_edges_directed())
	print(testEvent.export_edges_undirected())
	print("")

	obj.di.setNodes(testEvent.export_users());
	obj.di.setEdges(testEvent.export_edges_directed());

	obj.di.save();

	print(obj.name)
	print(obj.di.getNodes())
	print(obj.di.getEdges())


"""
	obj.getEdges
	obj.setEdges
	obj.getNodes
	obj.setNodes
	"""

	#cool so obj is the event database object

	#time to make shit more confusing

	#myEvent = Event()
	