from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login, logout
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.db import transaction
from .models import Oferta, Ciudad, Servicio, Preferencias
from .forms import DatosUsuarioForm, PreferenciasForm

@login_required
def listado_ofertas(request):
    ofertas = Oferta.objects.all()
    context = {'ofertas': ofertas}
    return render(request, 'ofertas.html', context)


@login_required
def detalle_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    context = {'oferta': oferta}
    return render(request, 'detalle_oferta.html', context)


@login_required
def listado_ciudades(request):
    ciudades = Ciudad.objects.all()
    context = {'ciudades': ciudades}
    return render(request, 'ciudades.html', context)


@login_required
def detalle_ciudad(request, ciudad_id):
    ciudad = get_object_or_404(Ciudad, pk=ciudad_id)
    ofertas = ciudad.oferta_set.all()

    context = {
        'ciudad': ciudad,
        'ofertas': ofertas,
    }

    return render(request, 'detalle_ciudad.html', context)


@login_required
def listado_servicios(request):
    servicios = Servicio.objects.all()
    context = {'servicios': servicios}
    return render(request, 'servicios.html', context)


@login_required
def detalle_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    ofertas = servicio.oferta_set.all()

    context = {
        'servicio': servicio,
        'ofertas': ofertas,
    }

    return render(request, 'detalle_servicio.html', context)


@login_required
def inicio(request):
    preferencias, _ = Preferencias.objects.get_or_create(usuario=request.user)
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

    return render(request, 'inicio.html', {'ofertas_destacadas': ofertas_destacadas})


def iniciar_sesion(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)

        if form.is_valid():
            usuario = form.get_user()
            login(request, usuario)
            return redirect('inicio')
    else:
        form = AuthenticationForm(request)

    context = {'form': form}
    return render(request, 'iniciar_sesion.html', context)

def crear_cuenta(request):
    if request.user.is_authenticated:
        return redirect('perfil')

    if request.method == 'POST':
        form = UserCreationForm(request.POST)

        if form.is_valid():
            with transaction.atomic():
                usuario = form.save()
                Preferencias.objects.create(usuario=usuario)

            login(request, usuario)
            return redirect('perfil')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'crear_cuenta.html', context)

@require_POST
@login_required
def cerrar_sesion(request):
    logout(request)
    return redirect('iniciar_sesion')

@login_required
def perfil(request):
    preferencias, creado = Preferencias.objects.get_or_create(
        usuario=request.user
    )

    if request.method == 'POST':
        datos_form = DatosUsuarioForm(
            request.POST,
            instance=request.user
        )

        preferencias_form = PreferenciasForm(
            request.POST,
            instance=preferencias
        )

        datos_validos = datos_form.is_valid()
        preferencias_validas = preferencias_form.is_valid()

        if datos_validos and preferencias_validas:
            with transaction.atomic():
                datos_form.save()
                preferencias_form.save()

            return redirect('perfil')
    else:
        datos_form = DatosUsuarioForm(instance=request.user)
        preferencias_form = PreferenciasForm(instance=preferencias)

    context = {
        'datos_form': datos_form,
        'preferencias_form': preferencias_form,
    }

    return render(request, 'perfil.html', context)