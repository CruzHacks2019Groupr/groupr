import random

from .dbHandler import UserHandler
from .dbHandler import EventHandler
from .dbHandler import GroupHandler
from .dbHandler import dropMostTables

__MAXRAND__ = 100000
__NUMUSERS__ = 10

def generateLukeTestCase(userId):
	dropMostTables(userId)
	userList = []
	userList.append(UserHandler(userId))

	for userNum in range(0, __NUMUSERS__):
		userList.append(createUser(userNum))
	testEvent = createEvent("CMPS 183", "Web Delevopment Class", userList, 6)
	#eventhandler won't create duplicate edges
	print("building graph")
	for user1 in userList:
		for user2 in userList:
			if user1.id != userId:
				testEvent.addEdge(user1.id,user2.id, silent=True)
			
	print("Users")

	for user in userList:
		print(UserHandler(user))

	print(testEvent)

	print(testEvent.di.getEdges())

def createUser(userNum):

	#u = UserHandler.createUser(user_names[userNum], "00000000")
	#u.setBio(user_bios[userNum])
	#u.setPic("static/uploads/" + user_images[userNum])
	
	u = UserHandler.createUser("User" + str(userNum), "00000000")
	u.setBio("I am a robot. Help.")


	return u

def createEvent(name, desc, userList, groupSize):
	eventId = EventHandler.createEvent(name, desc, groupSize, userList[0].id)

	event = EventHandler(eventId)

	for user in userList:
		event.addUser(user)

	return eventId


user_names = ["John Smith", "Jack Sparrow", "Luke Skywalker", "Mary Poppins", "Jeff Lebowski", "Doc Brown"]
user_bios = ["Hi! I'm a full stack web developer and digital artist. For this project, I think that it would be cool to make a project that emails you when your Coffee is ready. I know how to use NodeJS, as well as the Adobe Suite.",
"Stay away from my rum, mate.", 
"I'm Luke Skywalker and I'm here to rescue you!",
"Don't you know that everybody's got a Fairyland of their own?",
"Stay away from my rug.",
"Why shouldn't you be happy?"]
user_images = [
"smith.jfif",
"sparrow.jfif",
"skywalker.jfif",
"poppins.webp",
"lebowski.webp",
"brown.jfif"]
user_emails = [
"jsmith@ucsc.edu",
"jack-sparrow@disney.com",
"luke_skywalker@cruzio.com",
"poppins@gmail.com",
"dont_touch_my_rug@gmail.com",
"docbrown@aol.net",
]