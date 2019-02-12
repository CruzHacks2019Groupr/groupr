from django.forms import ModelForm
from django import forms
from .models import Event, Profile

class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ['name', 'group_size', 'description']

class ProfileForm(forms.Form):
	name = forms.CharField()
	bio = forms.CharField()
	pic = forms.ImageField(required=False)
	contactInfo = forms.CharField()
