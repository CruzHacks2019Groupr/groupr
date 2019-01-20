from project.models import Event
def reccomendNext(userID):
	e = Event()										#loads event Data type
	x = e.getUsers.index(userID)					#loads user index by searching for userID's position
	y = e.getUserOn(x)								#gets int at user index representing the next user to swipe on
	
	if y is userID:									#checks to make sure the user doesn't swipe on themselves
		e.setUserOn(x,y+1)							#increment the userID and reloads it
		y = e.getUserOn(x)

	if y>=len(e.getUsers):							#checks to see if the position of the user is valid
		return -1
	else: 
		e.setUserOn(x,y+1)							#increments the value for the future
		return e.getUsers(y)