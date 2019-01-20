from project.models import Graph
from project.models import Event

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