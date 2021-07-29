from django.contrib import admin
from .models import Indoor, Plan

# Register your models here.

class IndoorAdmin(admin.ModelAdmin):
    list_display = ['nombre']

class PlanAdmin(admin.ModelAdmin):
    list_display = ['indoor', 'nombre', 'hora_encendido', 'hora_apagado']

admin.site.register(Indoor, IndoorAdmin)
admin.site.register(Plan, PlanAdmin)