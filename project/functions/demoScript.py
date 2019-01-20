from django.contrib.auth.models import User
from . import Event

#Demo script for presentation. Create the event, join it with your user then run script with parameters to populate with dummy users
def demoScript():
	__MAINUSERID__ = 1
	__DEMOEVENTID__ = 1
	__TOTALUSERS__ = 30

	#Gets references to mainUser and demoEvent
	mainUserModel = User.objects.get(id=mainUserId)
	demoEventModel = EventModel.objects.get(id=eventID)
	demoEvent = Event(demoEventModel.di.getNodes(), demoEventModel.di.getEdges())

	#Creates demoUsers and their associated profiles, then adds them to the demoEvent
	demoUsers = []

	for userNum in range(numUsers):
		demoUsers.append(user=User.objects.create_user("User#" + str(userNum), password='foobar'))
		demoEventModel.addUser(demoUsers[userNum]);
		demoEvent.add_user(demoUsers[userNum]);

	print("Graph dump:")
	print(demoEvent.export_users())
	print(demoEvent.export_edges_directed())
	print(demoEvent.export_edges_undirected())
	print("")