import random

from .dbHandler import UserHandler
from .dbHandler import EventHandler
from .dbHandler import GroupHandler
from .dbHandler import dropMostTables

__MAXRAND__ = 100000
__NUMUSERS__ = 5

def generateLukeTestCase(userId):
	dropMostTables(userId)

	userList = []
	userList.append(userId)

	for userNum in range(1, __NUMUSERS__):
		userList.append(createUser())

	testEvent = createEvent("TestEvent", "A test event", userList, 3)

	#eventhandler won't create duplicate edges
	for user1 in userList:
		for user2 in userList:
			if user1 != userId:
				testEvent.addEdge(user1,user2, silent=True)
			if user2 != userId:
				testEvent.addEdge(user2,user1, silent=True)

	print("Users")

	for user in userList:
		print(UserHandler(user))

	print(testEvent)

	print(testEvent.di.getEdges())

def createUser():
	userNum = random.randint(1, __MAXRAND__)
	print(str(userNum))
	return UserHandler.createUser(("User" + str(userNum)), "00000000").id

def createEvent(name, desc, userList, groupSize):
	eventId = EventHandler.createEvent(name, desc, groupSize, userList[0])

	event = EventHandler(eventId)

	for user in userList:
		event.addUser(user)

	return eventId

def createGroup():
	pass