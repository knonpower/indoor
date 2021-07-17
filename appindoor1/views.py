from django.shortcuts import render, redirect, get_object_or_404
from .models import Indoor, Plan
from .forms import IndoorForm, PlanForm
from django.contrib import messages

# Create your views here.


def home(request):

    return render(request, 'appindoor1/home.html')

def indoor(request):
    if request.method == "GET":
        indoor = Indoor.objects.all().order_by("id")
        context = {'lista_indoor':indoor}
        print("El GET de indoor:", context)
        return render(request, 'appindoor1/indoor.html', context)
    elif request.method == "POST":
        print("El POST contiene", request.POST)
        Indoor.objects.create(
            nombre=request.POST['nombre_indoor']
        )
        
        return redirect('appindoor1:indoor')

def configuracion(request):

    return render(request, 'appindoor1/configuracion.html')

def servicio(request):

    return render(request, 'appindoor1/servicio.html')


def eliminar(request, id):
    indoor = get_object_or_404(Indoor, id=id )
    indoor.delete()
    #messages.success(request, "Elemento eliminado")
    return redirect('appindoor1:indoor')