from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.template import loader
from django.utils import timezone
import requests
from django.core import serializers
import json
from .functions import test
from pusher import Pusher


pusher = Pusher(app_id=u'694776', key=u'4105ec1d8d985dcf27bf', secret=u'1cf25393f1f636e8dc3e' ,cluster=u'us2')

def index(request):
    test.printSomeShit()
    return render(request, 'project/index.html')
    

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

#@login_required(login_url='/admin/login/')
def chat(request):
    return render(request, "project/chat.html");

@csrf_exempt
def broadcast(request):
    pusher.trigger(u'a_channel', u'an_event', {u'name': request.user.username, u'message': request.POST['message']})
    return HttpResponse("done");
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
