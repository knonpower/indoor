from django.urls import path
from .views import home, indoor, configuracion, servicio, eliminar

app_name = "appindoor1"

urlpatterns = [
    path('', home, name="home"),
    path('indoor/', indoor, name="indoor"),
    path('configuracion/', configuracion, name="configuracion"),
    path('servicio/', servicio, name="servicio"),
    path('eliminar/<id>/', eliminar, name="eliminar"),
]