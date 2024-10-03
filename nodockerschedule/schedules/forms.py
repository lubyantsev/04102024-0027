from django import forms
from .models import Schedule, Event

class ScheduleForm(forms.ModelForm):
    class Meta:
        model = Schedule
        fields = ['password']

class PasswordForm(forms.Form):
    password = forms.CharField(widget=forms.PasswordInput)

class EventForm(forms.ModelForm):
    class Meta:
        model = Event
        fields = ['when', 'where', 'who']

