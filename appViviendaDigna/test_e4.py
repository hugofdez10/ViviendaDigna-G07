from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Ciudad, Oferta


class FuncionalidadesE4Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        usuarios = get_user_model().objects
        cls.usuario = usuarios.create_user('estudiante_e4')
        cls.ciudad = Ciudad.objects.create(nombre='Bilbao', descripcion='Ciudad de prueba')
        cls.oferta = Oferta.objects.create(
            titulo='Habitación de prueba', descripcion='Prueba', ciudad=cls.ciudad,
            precio_mensual=350,
        )

    def setUp(self):
        self.client.force_login(self.usuario)

    def test_filtro_get_y_fragmento_ajax_comparten_resultados(self):
        rutas = ('listado_ofertas', 'resultados_ofertas')
        for nombre in rutas:
            with self.subTest(ruta=nombre):
                ruta = reverse(nombre)
                respuesta = self.client.get(ruta, {'ciudad': self.ciudad.pk, 'precio_maximo': '350'})
                self.assertContains(respuesta, f'href="{reverse("detalle_ciudad", args=[self.ciudad.pk])}"')
                self.assertContains(respuesta, self.oferta.titulo)
                sin_ofertas = self.client.get(ruta, {'precio_maximo': '0'})
                self.assertNotContains(sin_ofertas, self.oferta.titulo)
                invalida = self.client.get(ruta, {'precio_maximo': '-1'})
                self.assertContains(invalida, 'Revisa los filtros')
        self.assertNotContains(self.client.get(reverse('resultados_ofertas')), '<!DOCTYPE html>')
