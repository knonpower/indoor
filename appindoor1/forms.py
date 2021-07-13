from django import forms
from .models import Indoor, Plan

class IndoorForm(forms.ModelForm):
    
    class Meta:
        model = Indoor
        fields = '__all__'

class PlanForm(forms.ModelForm):

    class Meta:
        model = Plan
        fields = '__all__'
