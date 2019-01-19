from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    # ex: /notes/5/
    #path('<int:note_id>/', views.detail, name='detail'),
    #path('get_notes/', views.get_notes, name='get_notes'),
    #path('post_note/', views.post_note, name='post_note'),
]