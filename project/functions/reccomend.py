from project.models import Graph
from project.models import Event
from .dbHandler import *

def reccomendNext(e,userID):
	event = EventHandler(e)
	user = UserHandler(userID)

	# profile is a dict containing all private user info for the given event
	profile = user.getCustomInfo(event)

	#check if the user has the reccomend list. It should be generated during joinEvent probably.
	if "reccomendList" not in profile:
		generateList(e, userID)

	rec = profile["reccomendList"]
	
	#using None instead of -1. Fite me.
	if rec == []:
		return None
	else:
		#if reccomending the current user
		if rec[0] == user.id:
			popUser(event, user)
			return reccomendNext(e, userID)
		else:
			return rec[0]


#delete the first user from the ReccomendNext list
def popUser(e, userID):
	event = EventHandler(e)
	user = UserHandler(userID)
	profile = user.getCustomInfo(event)
	if "reccomendList" in profile:
		rec = profile["reccomendList"]
		if rec != []:
			temp = rec.pop(0)
			profile["reccomendList"] = rec
			user.setCustomInfo(event, profile)
			return temp


#generates/resets list of swipes
def generateList(e, userID):
	event = EventHandler(e)
	user = UserHandler(userID)
	profile = user.getCustomInfo(event)
	profile["reccomendList"] = event.getUserIds()
	user.setCustomInfo(event, profile)
	#for debugging
	return profile["reccomendList"]

def getList(e, userID):
	event = EventHandler(e)
	user = UserHandler(userID)
	profile = user.getCustomInfo(event)
	if "reccomendList" in profile:
		rec = profile["reccomendList"]
		return rec
	return []



"""

OLD HACKATHON CODE

def reccomendNext(e,userID):
	x = e.getUsers().index(userID)					#loads user index by searching for userID's position
	UserList = e.getUsersOn()
	y = UserList[x]

	if y == -1:
		return -1
													#gets int at user index representing the next user to swipe on
	if x == y:										#checks to make sure the user doesn't swipe on themselves
		y+=1
		if y>=len(e.getUsers()):					#checks to see if the position of the user is valid
			return -1
		e.setUserOn(x,y)							#increment the userID and reloads it
		y = e.getUsersOn().index(x)
	if y>=len(e.getUsers()):						#checks to see if the position of the user is valid
		e.setUserOn(x, -1)
		return -1
	else: 
		e.setUserOn(x,y+1)							#increments the value for the future
		return e.getUsers()[x]

"""