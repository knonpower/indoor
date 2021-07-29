from django.urls import path
from .views import dashboard, indoor, crea_indoor, configuracion, servicio, eliminar, modificar, plan
app_name = "appindoor1"

urlpatterns = [
    path('', dashboard, name="dashboard"),
    path('indoor/', indoor, name="indoor"),
    path('crea_indoor/', crea_indoor, name="crea_indoor"),
    path('configuracion/', configuracion, name="configuracion"),
    path('servicio/', servicio, name="servicio"),
    path('eliminar/<pk>/', eliminar, name="eliminar"),
    path('modificar/<pk>/', modificar, name="modificar"),
    path('plan/<pk>/', plan, name="plan"),
]