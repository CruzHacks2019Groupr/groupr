from django.forms import ModelForm
from .models import Event, Profile

class EventForm(ModelForm):
	class Meta:
		model = Event
		fields = ['name', 'group_size', 'description']

class ProfileForm(ModelForm):
	class Meta:
		model = Profile
		fields = ['name', 'bio', 'pic']