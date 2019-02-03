from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.template import loader
from django.utils import timezone
import requests, random, string, re
from django.core import serializers
import json
from pusher import Pusher
from django.http import QueryDict
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

from .functions.reccomend import reccomendNext
from .functions.dbHandler import EventHandler, UserHandler, GroupHandler
from .forms import EventForm

from .functions.matcher import *


pusher = Pusher(app_id=u'694776', key=u'4105ec1d8d985dcf27bf', secret=u'1cf25393f1f636e8dc3e' ,cluster=u'us2')

@login_required(login_url='/landing/')
def index(request):
    print(request.user)
    if request.user is None:
        return redirect('landing')
    return render(request, 'project/index.html')

def landing(request):
    if request.user.is_authenticated:
        return redirect('index');  
    return render(request, 'project/landing.html')

def redir(request):
	return redirect('index');    

def detail(request, question_id):
	return HttpResponse("You're looking at question %s." % question_id)

@login_required(login_url='/login/')
def chat(request):
	channel = Search.getUserGroupInEvent(request.user.id, 1)
	return render(request, "project/chat.html", {'channel': channel})

@csrf_exempt
def broadcast(request):
	pusher.trigger(u'a_channel', u'an_event', {u'name': request.user.username, u'message': request.POST['message']})
	return HttpResponse("done");

def signup(request):
	if request.method == 'POST':
		form = UserCreationForm(request.POST)
		if form.is_valid():
			form.save()
			username = form.cleaned_data.get('username')
			raw_password = form.cleaned_data.get('password1')
			user = authenticate(username=username, password=raw_password)
			login(request, user)
			return redirect('index')
	else:
		form = UserCreationForm()
	return render(request, 'registration/signup.html', {'form': form})

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
	else:
		form = EventForm()
	return render(request, 'project/event.html', {'form':form})

def logout_view(request):
	logout(request)
	response_data = {}
	response_data['success'] = True
	return redirect('index')	#all of these functions are returning this JSONresponse because
								#it makes it easy to confirm delivery on the client-side





#API

def testFunc(request):
	current_user = request.user
	print ("Current User ID: ", current_user.id)
	print("testFunc")
	demoScript.demo()

	response_data = {}
	response_data['success'] = True
	return (JsonResponse(response_data))

@login_required(login_url='/login/')
def addEvent(request):
	response_data = {}
	info = request.POST.dict()
	print(info)
	user = UserHandler(request.user.id)
	user.joinEvent(info.get('code'))
	return redirect('index')


@login_required(login_url='/login/')
def accept(request):
	print("accept")

	response_data = {}
	info = request.GET.dict()

	"""
	eventID = int(info.get('eventID'))
	mainUser = request.user.id
	acceptedUser = int(info.get('otherID'))

	
	targetEventModel = Event.objects.get(id=eventID)
	targetEvent = EventClass(targetEventModel.di.getNodes(), targetEventModel.di.getEdges())

	targetEvent.add_edge(mainUser, acceptedUser) 
	print("Group size" + str(targetEventModel.group_size))
	groupUsers = findPerfectGroup(targetEvent, mainUser, targetEventModel.group_size)

	#print("Group Users" + groupUsers)
	group = -1;

	if groupUsers != None:
		print("WE FOUND A GROUP")
		group = buildGroup(targetEventModel.id, groupUsers)
 
	print("reccomend next: " +str(reccomendNext(targetEventModel, mainUser)))
	
	response_data['group'] = group
	"""
	response_data['success'] = True
	return (JsonResponse(response_data))

@login_required(login_url='/login/')
def decline(request):
	print("decline")
	
	response_data = {}
	info = request.GET.dict()
	"""
	eventID = int(info.get('eventID'))
	mainUser = request.user.id

	targetEventModel = Event.objects.get(id=eventID)
	targetEvent = EventClass(targetEventModel.di.getNodes(), targetEventModel.di.getEdges())

	print("reccomend next: " +str(reccomendNext(targetEventModel, mainUser)))
	"""

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
		g = user.getGroups(event = e)
		if(g != []):
			temp['group'] = g[0].id
		json_events.append(temp)

	my_events = user.getEventsOwner()
	for e in my_events:
		isIn = False
		for E in json_events:
			if(e.id == E.get('ID') and user.id == e.owner):
				isIn = True
		if not isIn:	
			print(e)
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

@login_required(login_url='/login/')
def getNextMatch(request):
	print("getNextMatch")
	response_data = {}
	requestDict = request.GET.dict()
	event = EventHandler(requestDict.get('eventID'))
	user = UserHandler(request.user.id)
	suggestedUser = UserHandler(reccomendNext(event,user))
	if suggestedUser.exists:
		response_data['suggested_usr_name'] = suggestedUser.getName()
		response_data['suggested_usr_id'] = suggestedUser.id
	else:
		response_data['suggested_usr_name'] = ""
		response_data['suggested_usr_id'] = ""


	"""
	event = int(eventBody.get('eventID'))

	if (event != -1):
		usrs = Event.objects.get(id=event).getUsers()
		me = -1
		for i in range(len(usrs)):
			if usrs[i] == request.user.id:
				me = i
		usrsOn = Event.objects.get(id=event).getUsersOn()
		if me != -1 and usrsOn[me] != -1:
			Usr = User.objects.get(id=usrs[usrsOn[me]-1]) #might be wrong
			response_data['suggested_usr_name'] = Usr.username
			response_data['suggested_usr_id'] = Usr.id
		else:
			response_data['suggested_usr_name'] = "No More Users"
			response_data['suggested_usr_id'] = -1
	else:
		response_data['suggested_usr_name'] = "No More Users"
		response_data['suggested_usr_id'] = -1
	"""
	
	return (JsonResponse(response_data))
