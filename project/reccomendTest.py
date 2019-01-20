from .models import Graph
from .models import Event
from .functions.reccomend import *

def reccomend_test():

	_di = Graph()
	_undi = Graph()
	e = Event(name = "NAME",  group_size = 2,  di = _di, undi = _undi, creator = "userid")
	e.addUser("Poop")
	e.addUser("Jenkins")
	print(e.getUsers())
	print(e.getUsersOn())
	print(reccomendNext(e,"Poop"))