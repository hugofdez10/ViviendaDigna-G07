from django import forms
from django.contrib.auth.models import User

from .models import Ciudad, Preferencias


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


class FiltroOfertasForm(forms.Form):
    ciudad = forms.ModelChoiceField(
        queryset=Ciudad.objects.order_by('nombre'),
        label='Ciudad',
        empty_label='Todas las ciudades',
        required=False,
    )
    precio_maximo = forms.DecimalField(
        label='Precio máximo mensual (€)',
        min_value=0,
        max_digits=8,
        decimal_places=2,
        required=False,
    )
