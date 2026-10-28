from django.shortcuts import render, get_object_or_404
from .models import Ciudad, Servicio, Oferta

def listado_ofertas(request):
    ofertas = Oferta.objects.all()
    context = {'ofertas': ofertas}
    return render(request, 'ofertas.html', context)

def detalle_oferta(request, oferta_id):
    oferta = get_object_or_404(Oferta, pk=oferta_id)
    context = {'oferta': oferta}
    return render(request, 'detalle_oferta.html', context)

def listado_ciudades(request):
    ciudades = Ciudad.objects.all()
    context = {'ciudades': ciudades}
    return render(request, 'ciudades.html', context)

def detalle_ciudad(request, ciudad_id):
    ciudad = get_object_or_404(Ciudad, pk=ciudad_id)
    ofertas = ciudad.oferta_set.all()

    context = {
        'ciudad': ciudad,
        'ofertas': ofertas,
    }

    return render(request, 'detalle_ciudad.html', context)

def listado_servicios(request):
    servicios = Servicio.objects.all()
    context = {'servicios': servicios}
    return render(request, 'servicios.html', context)

def detalle_servicio(request, servicio_id):
    servicio = get_object_or_404(Servicio, pk=servicio_id)
    ofertas = servicio.oferta_set.all()

    context = {
        'servicio': servicio,
        'ofertas': ofertas,
    }

    return render(request, 'detalle_servicio.html', context)

def inicio(request):
    return render(request, 'inicio.html')
