from .models import Event, Groups

class Search():
	def getUserEvents(userID):
		events = Event.objects.all()
		myEvents = []
		for x in events:
			usrs = x.getUsers()
			for i in usrs:
				if(i == userID):
					myEvents.append(x.id)
		return myEvents

	def getUserCreatedEvents(userID):
		events = Event.objects.all()
		for x in events:
			usr = x.creator
			if(usr == userID):
				return x.id
		return None

	def getUserGroups(userID):
		groups = Groups.objects.All()
		myGroups = []
		for x in groups:
			for i in x.getUsers():
				if(i == userID):
					myEvents.append(x.id)
		return myGroups

	def getUserGroupInEvent(userID, eventID):
		myGroups = getUserGroups(userID)
		for x in myGroups:
			people = x.getUsers()
			for i in people:
				if(i == userID):
					return x.id