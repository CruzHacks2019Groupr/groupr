from django.contrib.auth.models import User
from .Event import Event
from ..models import Event as EventModel
import random

#Demo script for presentation. Create the event, join it with your user then run script with parameters to populate with dummy users
def demo():
	__MAINUSERID__ = 1
	__DEMOEVENTID__ = 1
	__TOTALUSERS__ = 5

	#Gets references to mainUser and demoEvent
	mainUserModel = User.objects.get(id=__MAINUSERID__)
	demoEventModel = EventModel.objects.get(id=__DEMOEVENTID__)
	demoEvent = Event(demoEventModel.di.getNodes(), demoEventModel.di.getEdges())

	#Creates demoUsers and their associated profiles, then adds them to the demoEvent
	demoUsers = []

	demoEventModel.addUser(__MAINUSERID__);
	demoEvent.add_user(__MAINUSERID__);


	for userNum in range(__TOTALUSERS__):
		demoUsers.append(User.objects.create_user("User#" + str(userNum), password='foobar'))
		demoEventModel.addUser(demoUsers[userNum].id);
		demoEvent.add_user(demoUsers[userNum].id);

	for user1 in demoUsers:
		for user2 in demoUsers:
			if user1.id != user2.id and user1.id != __MAINUSERID__ and user2.id != __MAINUSERID__:
				demoEvent.add_edge(user1.id, user2.id)

	print("Graph dump:")
	print(demoEvent.export_users())
	print(demoEvent.export_edges_directed())
	print(demoEvent.export_edges_undirected())
	print("")

	demoEventModel.di.setNodes(demoEvent.export_users());
	demoEventModel.di.setEdges(demoEvent.export_edges_directed());

	demoEventModel.di.save();
	demoEventModel.save();