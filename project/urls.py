from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views
from . import api

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^landing/$', views.landing, name='landing'),
    
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^ajax/chat/$', views.broadcast),


    #API
    url(r'^testFunc1/$', api.testFunc1, name='testFunc1'),
    url(r'^testFunc2/$', api.testFunc2, name='testFunc2'),
    url(r'^forceGroups/$', api.forceGroups, name='forceGroups'),
    url(r'^accept/$', api.accept, name='accept'),
    url(r'^decline/$', api.decline, name='decline'),
    url(r'^getNextMatch/$', api.getNextMatch, name='getNextMatch'),
    url(r'^loadData/$', api.loadData, name='loadData'),
    url(r'^event/$', api.event, name='event'),
    url(r'^addevent/$', api.addEvent, name='addevent'),
    url(r'^updateProfile/$', api.updateProfile, name='event'),
    url(r'^rejectGroup/$', api.rejectGroup, name='event'),
    
]