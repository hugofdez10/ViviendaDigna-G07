from django import forms
from django.contrib.auth.models import User
from django.utils.translation import gettext_lazy as _

from .models import Ciudad, Preferencias, SolicitudInformacion


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
        label=_('Ciudad'),
        empty_label=_('Todas las ciudades'),
        required=False,
    )
    precio_maximo = forms.DecimalField(
        label=_('Precio máximo mensual (€)'),
        min_value=0,
        max_digits=8,
        decimal_places=2,
        required=False,
    )


class SolicitudInformacionForm(forms.ModelForm):
    class Meta:
        model = SolicitudInformacion
        fields = ['mensaje']
        labels = {'mensaje': _('¿Qué te gustaría saber sobre esta oferta?')}
        widgets = {'mensaje': forms.Textarea(attrs={'rows': 5})}
