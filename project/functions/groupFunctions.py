#takes handlers
def disbandGroup(group, event):
	print("disbandGroup")
	users = group.getUsers()

	for user in users:
		event._addUserToGraph(user.id)
		#reset all swipes and delete the nodes
		profile = user.getCustomInfo(event)
		reccomendList = profile['reccomendList']
		for otherUser in users:
			if otherUser.id != user.id:
				if(otherUser.id not in reccomendList):
					#add users to the front of the list
					reccomendList.insert(0 , otherUser.id)
				event.removeEdge(user.id,otherUser.id)
		profile['reccomendList'] = reccomendList
		user.setCustomInfo(event,profile)
	group.delete()

#takes handlers
def leaveGroup(group, event, user):
	print("leaveGroup")
	users = group.getUsers()

	event._addUserToGraph(user.id)
	#reset all swipes and delete the nodes
	profile = user.getCustomInfo(event)
	reccomendList = profile['reccomendList']

	for otherUser in users:
		if otherUser.id != user.id:
			if(otherUser.id not in reccomendList):
				#add users to the front of the list
				reccomendList.insert(0 , otherUser.id)
			event.removeEdge(user.id,otherUser.id)
	profile['reccomendList'] = reccomendList
	user.setCustomInfo(event,profile)
	group.group.users.remove(user._getEventProfile(event))