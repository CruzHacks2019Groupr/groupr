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
from .functions import demoScript
from .functions.matcher import *
from .functions.Event import Event as EventClass
from pusher import Pusher
from .forms import EventForm
from .models import Graph
from .models import Event
from .searchUser import Search
from . import BuildGroup
from django.http import QueryDict
from .functions.reccomend import reccomendNext

from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm


pusher = Pusher(app_id=u'694776', key=u'4105ec1d8d985dcf27bf', secret=u'1cf25393f1f636e8dc3e' ,cluster=u'us2')

def index(request):
    return render(request, 'project/index.html')

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
            a = Graph()
            b = Graph()
            a.save()
            b.save()
            e.di = a
            e.undi = b
            e.save()
            return redirect('index')
    else:
        form = EventForm()
    return render(request, 'project/event.html', {'form':form})





#API

#used for generating random names
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def logout_view(request):
    logout(request)
    response_data = {}
    response_data['success'] = True
    return redirect('index')	#all of these functions are returning this JSONresponse because
    										#it makes it easy to confirm delivery on the client-side

def testFunc(request):
    current_user = request.user
    print ("Current User ID: ", current_user.id)
    print("testFunc")
    demoScript.demo()

    response_data = {}
    response_data['success'] = True
    return (JsonResponse(response_data))

@login_required(login_url='/login/')
def accept(request):
    print("accept")

    response_data = {}
    info = request.GET.dict()

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


    response_data['success'] = True
    response_data['group'] = group
    return (JsonResponse(response_data))

@login_required(login_url='/login/')
def decline(request):
    print("decline")
    response_data = {}
    info = request.GET.dict()
    eventID = int(info.get('eventID'))
    mainUser = request.user.id

    targetEventModel = Event.objects.get(id=eventID)
    targetEvent = EventClass(targetEventModel.di.getNodes(), targetEventModel.di.getEdges())

    print("reccomend next: " +str(reccomendNext(targetEventModel, mainUser)))

    response_data['success'] = True
    return (JsonResponse(response_data))

@login_required(login_url='/login/')
def loadData(request):
    print("Load Data")
    response_data = {}
    response_data['success'] = True

    evID = Search.getUserEvents(request.user.id)
    evName = []
    for i in evID:
        evName.append(Event.objects.get(id=i).name)

    my_evID = Search.getUserCreatedEvents(request.user.id)
    my_evName = []
    for i in my_evID:
        my_evName.append(Event.objects.get(id=i).name)

    curr_type = False #False is ev, true is my_ev
    curr = -1
    if(len(evID) != 0):
        curr = 0
    elif(len(my_evID) != 0):
        curr = 0
        curr_type = True

    response_data['event_ids'] = evID
    response_data['event_names'] = evName
    response_data['my_event_ids'] = my_evID
    response_data['my_event_names'] = my_evName
    response_data['curr_event'] = curr
    response_data['curr_type'] = curr_type
    response_data['Group'] = None
    return (JsonResponse(response_data))

@login_required(login_url='/login/')
def getNextMatch(request):
    print("getNextMatch")
    response_data = {}
    eventBody = request.GET.dict()
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
    
    return (JsonResponse(response_data))

"""
Demo:
def post_note(request):
	noteTitle = request.GET['title']
	noteBody = request.GET['body']
	n = note(note_title=noteTitle, note_text=noteBody, pub_date=timezone.now())
	print(n)
	n.save()
	return(JsonResponse({"success", 1}))

def get_notes(request):
	print(request.GET['start_idx'])
	resultset = note.objects.all()
	results = [ob.as_json() for ob in resultset]
	return(JsonResponse(json.dumps(results),safe=False))
"""
