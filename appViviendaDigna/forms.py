from django import forms
from django.contrib.auth.models import User

from .models import Preferencias


class DatosUsuarioForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email']

        labels = {
            'first_name': 'Nombre',
            'last_name': 'Apellidos',
            'email': 'Correo electrónico',
        }


class PreferenciasForm(forms.ModelForm):
    class Meta:
        model = Preferencias
        fields = ['ciudades', 'precio_maximo']

        labels = {
            'ciudades': 'Ciudades que te interesan',
            'precio_maximo': 'Precio máximo mensual (€)',
        }

        widgets = {
            'ciudades': forms.CheckboxSelectMultiple(),
        }