from decimal import Decimal
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from .models import Ciudad, Oferta, Preferencias, Servicio


class FlujoViviendaTests(TestCase):
    @classmethod
    def setUpTestData(cls):
        cls.user = get_user_model().objects.create_user(username='estudiante', password='ClavePruebas483!')
        cls.a = Ciudad.objects.create(nombre='Ciudad A', descripcion='Ejemplo')
        cls.b = Ciudad.objects.create(nombre='Ciudad B', descripcion='Ejemplo')
        cls.servicio = Servicio.objects.create(nombre='Wifi', descripcion='Internet')
        cls.barata = Oferta.objects.create(titulo='A económica', descripcion='Ejemplo', precio_mensual='400', ciudad=cls.a)
        cls.empate = Oferta.objects.create(titulo='A empate', descripcion='Ejemplo', precio_mensual='400', ciudad=cls.a)
        cls.cara = Oferta.objects.create(titulo='A cara', descripcion='Ejemplo', precio_mensual='900', ciudad=cls.a)
        cls.otra = Oferta.objects.create(titulo='B económica', descripcion='Ejemplo', precio_mensual='600', ciudad=cls.b)
        cls.barata.servicios.add(cls.servicio)

    def setUp(self):
        self.client.force_login(self.user)

    def seleccion(self):
        return list(self.client.get(reverse('inicio')).context['ofertas_destacadas'])

    def test_sin_preferencias_crea_perfil_y_muestra_todas_las_ciudades(self):
        self.assertEqual(self.seleccion(), [self.barata, self.otra])
        self.assertTrue(Preferencias.objects.filter(usuario=self.user).exists())

    def test_ciudad_seleccionada(self):
        pref = Preferencias.objects.create(usuario=self.user)
        pref.ciudades.add(self.b)
        self.assertEqual(self.seleccion(), [self.otra])

    def test_presupuesto_inclusivo_y_desempate_por_id(self):
        Preferencias.objects.create(usuario=self.user, precio_maximo=Decimal('400'))
        self.assertEqual(self.seleccion(), [self.barata])

    def test_presupuesto_cero_no_se_ignora(self):
        Preferencias.objects.create(usuario=self.user, precio_maximo=0)
        self.assertEqual(self.seleccion(), [])

    def test_ciudad_y_presupuesto_se_combinan(self):
        pref = Preferencias.objects.create(usuario=self.user, precio_maximo=500)
        pref.ciudades.add(self.b)
        self.assertEqual(self.seleccion(), [])

    def test_sin_resultados_muestra_mensaje(self):
        Preferencias.objects.create(usuario=self.user, precio_maximo=1)
        self.assertContains(self.client.get(reverse('inicio')), 'No hay ofertas que coincidan')

    def test_catalogo_y_detalles(self):
        rutas = [('inicio', []), ('listado_ofertas', []), ('listado_ciudades', []), ('listado_servicios', []), ('perfil', []), ('detalle_oferta', [self.barata.pk]), ('detalle_ciudad', [self.a.pk]), ('detalle_servicio', [self.servicio.pk])]
        for nombre, args in rutas:
            with self.subTest(nombre=nombre):
                self.assertEqual(self.client.get(reverse(nombre, args=args)).status_code, 200)

    def test_rutas_privadas_redirigen_a_login(self):
        self.client.logout()
        for nombre in ['inicio', 'listado_ofertas', 'listado_ciudades', 'listado_servicios', 'perfil']:
            with self.subTest(nombre=nombre):
                respuesta = self.client.get(reverse(nombre))
                self.assertEqual(respuesta.status_code, 302)
                self.assertIn(reverse('iniciar_sesion'), respuesta.url)

    def test_perfil_guarda_datos_y_preferencias(self):
        respuesta = self.client.post(reverse('perfil'), {'first_name': 'Ana', 'last_name': 'Ejemplo', 'email': 'ana@example.com', 'ciudades': [self.a.pk], 'precio_maximo': '450.00'})
        self.assertRedirects(respuesta, reverse('perfil'))
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, 'Ana')
        pref = Preferencias.objects.get(usuario=self.user)
        self.assertEqual(pref.precio_maximo, Decimal('450'))
        self.assertEqual(list(pref.ciudades.all()), [self.a])

    def test_presupuesto_negativo_no_guarda_datos_personales(self):
        respuesta = self.client.post(reverse('perfil'), {'first_name': 'No guardar', 'last_name': '', 'email': '', 'precio_maximo': '-1'})
        self.assertEqual(respuesta.status_code, 200)
        self.assertIn('precio_maximo', respuesta.context['preferencias_form'].errors)
        self.user.refresh_from_db()
        self.assertEqual(self.user.first_name, '')

    def test_registro_crea_preferencias(self):
        self.client.logout()
        respuesta = self.client.post(reverse('crear_cuenta'), {'username': 'nuevo', 'password1': 'ClaveNueva849!abc', 'password2': 'ClaveNueva849!abc'})
        self.assertRedirects(respuesta, reverse('perfil'))
        self.assertTrue(Preferencias.objects.filter(usuario__username='nuevo').exists())

    def test_login_y_logout_solo_por_post(self):
        self.client.logout()
        self.assertRedirects(self.client.post(reverse('iniciar_sesion'), {'username': 'estudiante', 'password': 'ClavePruebas483!'}), reverse('inicio'))
        self.assertEqual(self.client.get(reverse('cerrar_sesion')).status_code, 405)
        self.assertRedirects(self.client.post(reverse('cerrar_sesion')), reverse('iniciar_sesion'))

    def test_oferta_inexistente_devuelve_404(self):
        self.assertEqual(self.client.get(reverse('detalle_oferta', args=[99999])).status_code, 404)
