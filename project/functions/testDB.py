from project.functions.dbHandler import *
from django.contrib.auth.models import User

for userNum in range(10):
	User.objects.create_user("User#" + str(userNum), password='foobar')


u1 = UserHandler(1)
u2 = UserHandler(2)
u3 = UserHandler(3)

event = EventHandler.createEvent("My Event", 5, 5)
u1.joinEvent(event.addCode)
u2.joinEvent(event.addCode)
u3.joinEvent(event.addCode)
GroupHandler.createGroup([u1,u2,u3], event)