from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.views.decorators.csrf import csrf_exempt
from django.core import serializers
from pusher import Pusher
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import UserCreationForm

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

def logout_view(request):
	logout(request)
	response_data = {}
	response_data['success'] = True
	return redirect('index')	#all of these functions are returning this JSONresponse because
								#it makes it easy to confirm delivery on the client-side