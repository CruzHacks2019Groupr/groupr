import random

from .dbHandler import UserHandler
from .dbHandler import EventHandler
from .dbHandler import GroupHandler

__MAXRAND__ = 100000
__NUMUSERS__ = 20

def generateLukeTestCase(userId):
	userList = []
	userList.append(userId)

	for userNum in range(1, __NUMUSERS__):
		userList.append(createUser())

	testEvent = createEvent("TestEvent", "A test event", userList, 3)

	for userIdIter in range(1, len(userList)):
		testEvent.addEdge(userList[userIdIter], userList[0])

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

	for userIter in range(len(userList)):
		if userIter != 0:
			event.addUser(userList[userIter])

	return eventId

def createGroup():
	pass