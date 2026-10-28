from django.contrib import admin
from .models import Ciudad, Servicio, Oferta

admin.site.register([Ciudad, Servicio, Oferta])
