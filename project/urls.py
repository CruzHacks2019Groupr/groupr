from django.urls import path
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    url(r'^accounts/profile/$', views.redir, name='redir'),
    url(r'^login/$', auth_views.LoginView.as_view(), name='login'),
    url(r'^logout/$', views.logout_view, name='logout'),
    url(r'^signup/$', views.signup, name='signup'),
    url(r'^chat/$', views.chat, name='chat'),
    url(r'^event/$', views.event, name='event'),
    url(r'^ajax/chat/$', views.broadcast),


    #API
    url(r'^testFunc/$', views.testFunc, name='testFunc'),
    url(r'^accept/$', views.accept, name='accept'),
    url(r'^decline/$', views.decline, name='decline'),
    url(r'^getNextMatch/$', views.getNextMatch, name='getNextMatch'),
    url(r'^loadData/$', views.loadData, name='loadData'),
    

    # ex: /notes/5/
    #path('<int:note_id>/', views.detail, name='detail'),
    #path('get_notes/', views.get_notes, name='get_notes'),
    #path('post_note/', views.post_note, name='post_note'),
]