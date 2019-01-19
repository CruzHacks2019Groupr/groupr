from django.shortcuts import render
from django.http import HttpResponse, JsonResponse
from django.template import loader
from django.utils import timezone
import requests
from django.core import serializers
import json
from .functions import test

def index(request):
    test.printSomeShit()
    return render(request, 'project/index.html')
    

def detail(request, question_id):
    return HttpResponse("You're looking at question %s." % question_id)

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
