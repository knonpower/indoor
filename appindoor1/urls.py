from django.urls import path
from . import views

app_name = "appindoor1"

urlpatterns = [
    path('home/', views.home, name='home'),
    path('indoor/', views.indoor, name='indoor'),
    path('configuracion/', views.configuracion, name='configuracion'),
    path('servicio/', views.servicio, name='servicio'),
]