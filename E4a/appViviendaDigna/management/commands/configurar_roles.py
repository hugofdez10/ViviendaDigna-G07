from secrets import token_urlsafe

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group, Permission
from django.core.management.base import BaseCommand
from django.db import transaction


class Command(BaseCommand):
    help = 'Configura los grupos de administración del catálogo de Vivienda Digna.'

    def add_arguments(self, parser):
        parser.add_argument(
            '--usuarios-demo',
            action='store_true',
            help='Crea dos cuentas de demostración locales con contraseñas aleatorias.',
        )

    @transaction.atomic
    def handle(self, *args, **options):
        lectura = ['view_ciudad', 'view_servicio', 'view_oferta']
        roles = [
            ('Consulta del catálogo', 'e4_consulta', lectura),
            ('Editor de ofertas', 'e4_editor', lectura + ['add_oferta', 'change_oferta']),
        ]
        for nombre, usuario_demo, permisos in roles:
            grupo, _ = Group.objects.get_or_create(name=nombre)
            grupo.permissions.set(Permission.objects.filter(
                content_type__app_label='appViviendaDigna',
                codename__in=permisos,
            ))
            if options['usuarios_demo']:
                self.crear_usuario_demo(grupo, usuario_demo)
        self.stdout.write(self.style.SUCCESS('Grupos de administración configurados.'))

    def crear_usuario_demo(self, grupo, nombre):
        usuarios = get_user_model().objects
        if usuarios.filter(username=nombre).exists():
            self.stdout.write(f'{nombre} ya existe.')
            return
        contrasena = token_urlsafe(12)
        usuario = usuarios.create_user(username=nombre, password=contrasena, is_staff=True)
        usuario.groups.add(grupo)
        self.stdout.write(f'{nombre}: {contrasena}')
