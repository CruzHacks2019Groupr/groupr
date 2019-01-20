from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.utils import timezone
import requests, random, string
from django.core import serializers
import json
from .functions import swipr
from pusher import Pusher

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
    return render(request, "project/chat.html");

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





#API

#used for generating random names
def randomword(length):
   letters = string.ascii_lowercase
   return ''.join(random.choice(letters) for i in range(length))

def logout_view(request):
    logout(request)
    response_data = {}
    response_data['success'] = True
    return (JsonResponse(response_data))	#all of these functions are returning this JSONresponse because
    										#it makes it easy to confirm delivery on the client-side

def testFunc(request):
    current_user = request.user
    print ("Current User ID: ", current_user.id)
    print("testFunc")


    response_data = {}
    response_data['success'] = True
    return (JsonResponse(response_data))

def accept(request):
    print("accept")
    swipr.makeConnection(request.user.id, 4)
    response_data = {}
    response_data['success'] = True
    return (JsonResponse(response_data))

def decline(request):
    print("decline")
    response_data = {}
    response_data['success'] = True
    return (JsonResponse(response_data))

def getNextMatch(request):
    print("getNextMatch")
    response_data = {}
    #impliment real code here
    response_data['suggested_usr_name'] = randomword(5) + " " + randomword(8)

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
