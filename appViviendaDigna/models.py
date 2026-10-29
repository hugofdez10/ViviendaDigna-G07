from django.db import models
from django.conf import settings
from django.core.validators import MinValueValidator

class Ciudad(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Servicio(models.Model):
    nombre = models.CharField(max_length=50)
    descripcion = models.TextField()

    def __str__(self):
        return self.nombre


class Oferta(models.Model):
    titulo = models.CharField(max_length=100)
    descripcion = models.TextField()
    precio_mensual = models.DecimalField(max_digits=8, decimal_places=2)
    ciudad = models.ForeignKey(Ciudad, on_delete=models.CASCADE)
    servicios = models.ManyToManyField(Servicio)
    imagen = models.ImageField(upload_to='ofertas/', blank=True, null=True)

    def __str__(self):
        return self.titulo

class Preferencias(models.Model):
    usuario = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE
    )

    ciudades = models.ManyToManyField(
        Ciudad,
        blank=True
    )

    precio_maximo = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
        validators=[MinValueValidator(0)]
    )

    def __str__(self):
        return f"Preferencias de {self.usuario.username}"