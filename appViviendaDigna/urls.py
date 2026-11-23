from django.urls import path
from . import views

urlpatterns = [
    path('', views.PortadaAntiguaView.as_view(), name='portada_antigua'),
    path('ofertas/', views.ListadoOfertasView.as_view(), name='listado_ofertas'),
    path('ofertas/resultados/', views.ResultadosOfertasView.as_view(), name='resultados_ofertas'),
    path('ofertas/<int:oferta_id>/', views.DetalleOfertaView.as_view(), name='detalle_oferta'),
    path(
        'ofertas/<int:oferta_id>/solicitar-informacion/',
        views.SolicitarInformacionView.as_view(),
        name='solicitar_informacion',
    ),
    path('solicitudes/<int:pk>/', views.SolicitudConfirmadaView.as_view(), name='solicitud_confirmada'),
    path('ciudades/', views.ListadoCiudadesView.as_view(), name='listado_ciudades'),
    path('ciudades/<int:ciudad_id>/', views.DetalleCiudadView.as_view(), name='detalle_ciudad'),
    path('servicios/', views.ListadoServiciosView.as_view(), name='listado_servicios'),
    path('servicios/<int:servicio_id>/', views.DetalleServicioView.as_view(), name='detalle_servicio'),
    path('iniciar-sesion/', views.IniciarSesionView.as_view(), name='iniciar_sesion'),
    path('crear-cuenta/', views.CrearCuentaView.as_view(), name='crear_cuenta'),
    path('cerrar-sesion/', views.CerrarSesionView.as_view(), name='cerrar_sesion'),
    path('perfil/', views.PerfilView.as_view(), name='perfil'),
]
