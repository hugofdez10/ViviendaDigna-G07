from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.db import transaction
from django.shortcuts import redirect
from django.urls import reverse
from django.utils.decorators import method_decorator
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, FormView, ListView, RedirectView, TemplateView

from .forms import DatosUsuarioForm, FiltroOfertasForm, PreferenciasForm
from .models import Ciudad, Oferta, Preferencias, Servicio


class ListadoOfertasView(LoginRequiredMixin, ListView):
    model = Oferta
    template_name = 'ofertas.html'
    context_object_name = 'ofertas'

    def get_queryset(self):
        self.filtros = FiltroOfertasForm(self.request.GET or None)
        ofertas = super().get_queryset().select_related('ciudad')
        if not self.filtros.is_valid():
            return ofertas

        ciudad = self.filtros.cleaned_data['ciudad']
        precio_maximo = self.filtros.cleaned_data['precio_maximo']
        if ciudad:
            ofertas = ofertas.filter(ciudad=ciudad)
        if precio_maximo is not None:
            ofertas = ofertas.filter(precio_mensual__lte=precio_maximo)
        return ofertas

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['filtros'] = self.filtros
        return contexto


class ResultadosOfertasView(ListadoOfertasView):
    template_name = 'ofertas_resultados.html'


class DetalleOfertaView(LoginRequiredMixin, DetailView):
    queryset = Oferta.objects.select_related('ciudad').prefetch_related('servicios')
    template_name = 'detalle_oferta.html'
    pk_url_kwarg = 'oferta_id'


class ListadoCiudadesView(LoginRequiredMixin, ListView):
    model = Ciudad
    template_name = 'ciudades.html'
    context_object_name = 'ciudades'


class DetalleCiudadView(LoginRequiredMixin, DetailView):
    model = Ciudad
    template_name = 'detalle_ciudad.html'
    pk_url_kwarg = 'ciudad_id'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['ofertas'] = self.object.oferta_set.all()
        return contexto


class ListadoServiciosView(LoginRequiredMixin, ListView):
    model = Servicio
    template_name = 'servicios.html'
    context_object_name = 'servicios'


class DetalleServicioView(LoginRequiredMixin, DetailView):
    model = Servicio
    template_name = 'detalle_servicio.html'
    pk_url_kwarg = 'servicio_id'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        contexto['ofertas'] = self.object.oferta_set.all()
        return contexto


class InicioView(LoginRequiredMixin, TemplateView):
    template_name = 'inicio.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        preferencias, _ = Preferencias.objects.get_or_create(usuario=self.request.user)
        ciudades = preferencias.ciudades.all()
        if not ciudades.exists():
            ciudades = Ciudad.objects.all()

        ofertas_destacadas = []
        for ciudad in ciudades:
            ofertas = ciudad.oferta_set.all()
            if preferencias.precio_maximo is not None:
                ofertas = ofertas.filter(precio_mensual__lte=preferencias.precio_maximo)
            oferta = ofertas.order_by('precio_mensual', 'id').first()
            if oferta:
                ofertas_destacadas.append(oferta)

        contexto['ofertas_destacadas'] = ofertas_destacadas
        return contexto


class PortadaAntiguaView(RedirectView):
    pattern_name = 'inicio'


class IniciarSesionView(LoginView):
    template_name = 'iniciar_sesion.html'

    def get_default_redirect_url(self):
        return reverse('inicio')


class CrearCuentaView(FormView):
    form_class = UserCreationForm
    template_name = 'crear_cuenta.html'

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            return redirect('perfil')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        with transaction.atomic():
            usuario = form.save()
            Preferencias.objects.create(usuario=usuario)
        login(self.request, usuario)
        return redirect('perfil')


@method_decorator(require_POST, name='dispatch')
class CerrarSesionView(LoginRequiredMixin, LogoutView):
    next_page = 'iniciar_sesion'


class PerfilView(LoginRequiredMixin, TemplateView):
    template_name = 'perfil.html'

    def get_context_data(self, **kwargs):
        contexto = super().get_context_data(**kwargs)
        preferencias, _ = Preferencias.objects.get_or_create(usuario=self.request.user)
        datos = self.request.POST if self.request.method == 'POST' else None
        contexto['datos_form'] = DatosUsuarioForm(datos, instance=self.request.user)
        contexto['preferencias_form'] = PreferenciasForm(datos, instance=preferencias)
        return contexto

    def post(self, request, **kwargs):
        contexto = self.get_context_data(**kwargs)
        datos_form = contexto['datos_form']
        preferencias_form = contexto['preferencias_form']
        datos_validos = datos_form.is_valid()
        preferencias_validas = preferencias_form.is_valid()
        if datos_validos and preferencias_validas:
            with transaction.atomic():
                datos_form.save()
                preferencias_form.save()
            return redirect('perfil')
        return self.render_to_response(contexto)
