from . import Event
from ..models import Event as EventModel
from .matcher import *

EVENT_ID = 1

def makeConnection(user1, user2):

	print("Making Connection Between ", str(user1), " and ", str(user2))
	print(EventModel.objects.all())
	obj = EventModel.objects.get(id=EVENT_ID)
	print(obj.name)


"""
	obj.getEdges
	obj.setEdges
	obj.getNodes
	obj.setNodes
	"""

	#cool so obj is the event database object

	#time to make shit more confusing

	#myEvent = Event()
	