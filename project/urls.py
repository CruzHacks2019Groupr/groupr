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
    url(r'^ajax/chat/$', views.broadcast),
    # ex: /notes/5/
    #path('<int:note_id>/', views.detail, name='detail'),
    #path('get_notes/', views.get_notes, name='get_notes'),
    #path('post_note/', views.post_note, name='post_note'),
]