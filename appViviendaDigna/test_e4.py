from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse

from .models import Ciudad, Oferta, SolicitudInformacion


class FuncionalidadesE4Tests(TestCase):
    @classmethod
    def setUpTestData(cls):
        usuarios = get_user_model().objects
        cls.usuario = usuarios.create_user('estudiante_e4')
        cls.otro_usuario = usuarios.create_user('otro_estudiante')
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

    def test_solicitud_se_asocia_a_la_oferta_y_solo_la_lee_su_titular(self):
        ruta = reverse('solicitar_informacion', args=[self.oferta.pk])
        self.assertEqual(self.client.post(ruta, {'mensaje': '   '}).status_code, 200)
        self.assertFalse(SolicitudInformacion.objects.exists())

        respuesta = self.client.post(ruta, {'mensaje': '¿Está disponible en enero?'})
        solicitud = SolicitudInformacion.objects.get()
        self.assertEqual(solicitud.usuario, self.usuario)
        self.assertEqual(solicitud.oferta, self.oferta)
        confirmacion = reverse('solicitud_confirmada', args=[solicitud.pk])
        self.assertRedirects(respuesta, confirmacion)
        self.assertContains(self.client.get(confirmacion), 'Solicitud guardada')

        self.client.force_login(self.otro_usuario)
        self.assertEqual(self.client.get(confirmacion).status_code, 404)

    def test_selector_de_idioma_conserva_ruta_y_filtros(self):
        ruta = reverse('listado_ofertas') + '?precio_maximo=350'
        respuesta = self.client.post(reverse('set_language'), {'language': 'en', 'next': ruta})
        self.assertRedirects(respuesta, '/en' + ruta)
        ingles = self.client.get('/en' + ruta)
        self.assertContains(ingles, 'lang="en"')
        self.assertContains(ingles, 'Accommodation listings')
        self.assertContains(ingles, '/en/appViviendaDigna/ofertas/resultados/')
        self.assertContains(self.client.get('/'), 'lang="es"')
