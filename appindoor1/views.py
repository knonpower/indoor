from django.shortcuts import render
from .models import Indoor, Plan
from .forms import IndoorForm, PlanForm


# Create your views here.


def home(request):

    return render(request, 'appindoor1/home.html')

def indoor(request):
    if request.method == 'POST':
        print("El POST contiene", request.POST)
        Indoor.objects.create(
            nombre=request.POST['nombre_indoor']
        )
    return render(request, 'appindoor1/indoor.html')

def configuracion(request):

    return render(request, 'appindoor1/configuracion.html')

def servicio(request):

   
    return render(request, 'appindoor1/servicio.html')