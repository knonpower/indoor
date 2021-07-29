from django.shortcuts import render, redirect, get_object_or_404
from .models import Indoor, Plan
from .forms import IndoorForm, PlanForm
from django.contrib import messages

# Create your views here.


def dashboard(request):

    return render(request, 'appindoor1/dashboard.html')

def indoor(request):
    if request.method == "GET":
        indoor = Indoor.objects.all().order_by("id")
        context = {'lista_indoor':indoor, 'form':IndoorForm()}
        print("El GET de indoor:", context)
        return render(request, 'appindoor1/indoor.html', context)
    elif request.method == "POST":
        print("El Post: ", request.POST) 
        formulario = IndoorForm(request.POST)
        print("este es el formulario:", formulario)
        if formulario.is_valid():
            print("entro al if")
            formulario.save()        
            return redirect('appindoor1:indoor')

    #Indoor.objects.create(
    #    nombre=request.POST['nombre_indoor']
    #)
        
    #return redirect('appindoor1:indoor')
def crea_indoor(request):
    if request.method == 'GET':
        indoor = Indoor.objects.all().order_by("id")
        context = {'lista_indoor':indoor, 'form':IndoorForm()}
        print("El GET de indoor:", context)
        return render(request, 'appindoor1/crea_indoor.html', context)
    elif request.method == 'POST':
        print("El Post: ", request.POST) 
        formulario = IndoorForm(request.POST)
        print("este es el formulario:", formulario)
        if formulario.is_valid():
            print("entro al if")
            formulario.save()        
            return redirect('appindoor1:crea_indoor')
            
    return render(request, 'appindoor1/crea_indoor.html')

def configuracion(request):

    return render(request, 'appindoor1/configuracion.html')

def servicio(request):

    return render(request, 'appindoor1/servicio.html')


def eliminar(request, pk):
    #indoor = get_object_or_404(Indoor, id=id )
    indoor = Indoor.objects.get(pk=pk)
    indoor.delete()
    #messages.success(request, "Elemento eliminado")
    return redirect('appindoor1:crea_indoor')

def modificar(request, pk):
    indoor = Indoor.objects.get(pk=pk)
    context = {
        'form':IndoorForm(instance=indoor)
    }
    if request.method == "POST":
        formulario = IndoorForm(data=request.POST, instance=indoor)
        if formulario.is_valid():
            formulario.save()
            context['form'] = formulario
            print("el context tiene:", context)
    return render(request, 'appindoor1/modificar.html', context)

def plan(request, pk):
    plan = Plan.objects.all()
    print("Este es el Plan:", plan)
    context = {
        'form':PlanForm(), 'lista_plan':plan
    }
    return render(request, 'appindoor1/plan.html', context)