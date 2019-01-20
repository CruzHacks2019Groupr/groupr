from django.contrib.auth.models import User

def demoScript(mainUserId, eventID, numUsers):
	#Gets references to mainUser and demoEvent
	mainUserModel = User.objects.get(id=mainUserId)
	demoEventModel = EventModel.objects.get(id=eventID)

	#Creates demoUsers and their associated profiles
	demoUsers = []

	for userNum in range(numUsers):
		demoUsers.append(user=User.objects.create_user("User#" + str(userNum), password='foobar'))
		demoEventModel.addUser();