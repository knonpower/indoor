from django import forms
from django.forms import ModelForm
from .models import Indoor, Plan

class IndoorForm(ModelForm):
    
    class Meta:
        model = Indoor
        fields = '__all__'

class PlanForm(ModelForm):

    class Meta:
        model = Plan
        fields = '__all__'
