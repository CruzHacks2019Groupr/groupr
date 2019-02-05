from django.shortcuts import render, redirect
from .functions.reccomend import *
from .functions.dbHandler import EventHandler, UserHandler, GroupHandler
from django.contrib.auth.models import User
from .functions.matcher import *
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import QueryDict
from .forms import EventForm
from .functions import dbTest
from .functions import dbHandler


def testFunc1(request):
	print("testFunc1")

	dbTest.generateLukeTestCase(request.user.id)
	response_data = {}
	response_data['success'] = True
	return (JsonResponse(response_data))

def testFunc2(request):
	print("testFunc2")
	dbHandler.dropAllTables()

	response_data = {}
	response_data['success'] = True
	return (JsonResponse(response_data))


@login_required(login_url='/login/')
def event(request):
	if request.method == 'POST':
		form = EventForm(request.POST)
		if form.is_valid():
			e = form.save(commit=False)
			e.creator = request.user.id
			
			ev = EventHandler.createEvent(e.name, e.description, e.group_size, e.creator)

			print(ev)

			return redirect('index')
	return redirect('index')

@login_required(login_url='/login/')
def addEvent(request):
	response_data = {}
	info = request.POST.dict()
	print(info)
	user = UserHandler(request.user.id)
	user.joinEvent(info.get('code'))
	return redirect('index')

#this is a helper function
def getGroup(event, user):
	user = UserHandler(user)
	group = user.getGroups(event)
	if group is not None:
		groupObj = {}
		groupObj['id'] = group.id
		groupObj['hash'] = group.hash
		groupObj['users'] = [u.id for u in group.getUsers()]
		return groupObj
	return None

@login_required(login_url='/login/')
def accept(request):

	response_data = {}
	info = request.GET.dict()

	event = EventHandler(info.get('eventID'))
	user = UserHandler(request.user.id)
	acceptedUser = reccomendNext(event, user)
	popUser(event, user)

	event.addEdge(user.id, acceptedUser)
	pG = findPerfectGroup(event, user)

	if(pG != None):
		response_data['group'] = getGroup(event,user)

	response_data['success'] = True
	return (JsonResponse(response_data))

@login_required(login_url='/login/')
def decline(request):
	
	response_data = {}
	info = request.GET.dict()

	popUser(info.get('eventID'), request.user.id)

	response_data['success'] = True
	return (JsonResponse(response_data))

@login_required(login_url='/login/')
def loadData(request):
	response_data = {}
	response_data['success'] = True

	user = UserHandler(request.user.id)
	events = user.getEvents()
	json_events = []

	for e in events:
		temp = {}
		temp['ID'] = e.id
		temp['name'] = e.name
		temp['isIn'] = True
		temp['addCode'] = e.addCode
		temp['description'] = e.description
		if(e.owner == user.id):
			temp['isOwner'] = True
		else:
			temp['isOwner'] = False
		g = getGroup(e, user)
		if g is not None:
			temp['group'] = g
		json_events.append(temp)

	my_events = user.getEventsOwner()
	for e in my_events:
		isIn = False
		for E in json_events:
			if(e.id == E.get('ID') and user.id == e.owner):
				isIn = True
		if not isIn:	
			temp = {}
			temp['ID'] = e.id
			temp['name'] = e.name
			temp['addCode'] = e.addCode
			temp['isIn'] = False
			temp['isOwner'] = True
			temp['description'] = e.description
			json_events.append(temp)

	response_data['events'] = json_events
	return (JsonResponse(response_data))


def getNextMatch(request):
	response_data = {}
	info = request.GET.dict()

	suggestedUser = reccomendNext(info.get('eventID'), request.user.id)

	if(suggestedUser != None):
		response_data['suggested_usr_id'] = UserHandler(suggestedUser).id
		response_data['suggested_usr_name'] = UserHandler(suggestedUser).getName()
	else:
		response_data['suggested_usr_id'] = -1
		response_data['suggested_usr_name'] = ''
	
	response_data['success'] = True
	return (JsonResponse(response_data))
