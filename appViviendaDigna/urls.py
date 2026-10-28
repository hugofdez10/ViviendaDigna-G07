from django.urls import path
from . import views

urlpatterns = [
    path('', views.inicio, name='inicio'),
    path('ofertas/', views.listado_ofertas, name='listado_ofertas'),
    path('ofertas/<int:oferta_id>/', views.detalle_oferta, name='detalle_oferta'),
    path('ciudades/', views.listado_ciudades, name='listado_ciudades'),
    path('ciudades/<int:ciudad_id>/', views.detalle_ciudad, name='detalle_ciudad'),
    path('servicios/', views.listado_servicios, name='listado_servicios'),
    path('servicios/<int:servicio_id>/', views.detalle_servicio, name='detalle_servicio'),
    path('iniciar-sesion/', views.iniciar_sesion, name='iniciar_sesion'),
    path('crear-cuenta/', views.crear_cuenta, name='crear_cuenta'),
    path('cerrar-sesion/', views.cerrar_sesion, name='cerrar_sesion'),
]