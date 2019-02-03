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

	event = info.get('!!!EVENT!!!')
	user = info.get('!!!USER!!!')
	acceptedUser = info.get('!!!OTHER USER!!!')

	popUser(event, user)
	event.addEdge(user, acceptedUser)

	if(findPerfectGroup(event, user) == None):
		response_data['groupFormed'] = False
	else:
		response_data['groupFormed'] = True

	response_data['success'] = True
	return (JsonResponse(response_data))

@login_required(login_url='/login/')
def decline(request):
	print("decline")
	
	response_data = {}
	info = request.GET.dict()

	popUser(info.get('!!!EVENT!!!'), info.get('!!!USER!!!'))

	response_data['success'] = True
	return (JsonResponse(response_data))

@login_required(login_url='/login/')
def loadData(request):
	print("Load Data")
	response_data = {}
	response_data['success'] = True

	user = UserHandler(request.user.id)
	events = user.getEvents()
	json_events = []
	for e in events:
		temp = {}
		temp['ID'] = e.id
		temp['name'] = e.name
		temp['group'] = user.getGroups(event = e.id)
		json_events.append(temp)

	my_events = user.getEventsOwner()
	my_json_events = []
	for e in my_events:
		temp = {}
		temp['ID'] = e.id
		temp['name'] = e.name
		temp['addCode'] = e.addCode
		temp['description'] = e.description
		my_json_events.append(temp)



	curr_type = False #False is ev, true is my_ev
	curr = -1
	if(len(json_events) != 0):
		curr = 0
	elif(len(my_json_events) != 0):
		curr = 0
		curr_type = True

	#response_data['events'] = 
	response_data['my_events'] =  my_json_events
	response_data['events'] = json_events
	response_data['curr_event'] = curr
	response_data['curr_type'] = curr_type
	return (JsonResponse(response_data))

@login_required(login_url='/login/')
def getNextMatch(request):
	print("getNextMatch")
	response_data = {}
	requestDict = request.GET.dict()

	response_data['nextUser'] = reccomendNext(info.get('!!!EVENT!!!'), info.get('!!!USER!!!'))
	
	response_data['success'] = True
	return (JsonResponse(response_data))
