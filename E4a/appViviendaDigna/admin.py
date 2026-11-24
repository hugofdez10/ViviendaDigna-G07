from django.contrib import admin

from .models import Ciudad, Oferta, Preferencias, Servicio, SolicitudInformacion

admin.site.site_header = 'Administración de Vivienda Digna'
admin.site.site_title = 'Vivienda Digna'
admin.site.index_title = 'Catálogo y solicitudes'


@admin.register(Ciudad, Servicio)
class EntidadCatalogoAdmin(admin.ModelAdmin):
    list_display = ('nombre', 'descripcion')
    search_fields = ('nombre',)
    ordering = ('nombre',)


@admin.register(Oferta)
class OfertaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'ciudad', 'precio_mensual')
    list_filter = ('ciudad', 'servicios')
    list_select_related = ('ciudad',)
    search_fields = ('titulo', 'ciudad__nombre')
    filter_horizontal = ('servicios',)
    fieldsets = (
        ('Datos del anuncio', {'fields': ('titulo', 'descripcion', 'imagen')}),
        ('Alojamiento y servicios', {'fields': ('ciudad', 'precio_mensual', 'servicios')}),
    )


@admin.register(Preferencias)
class PreferenciasAdmin(admin.ModelAdmin):
    list_display = ('usuario', 'precio_maximo')
    search_fields = ('usuario__username',)
    filter_horizontal = ('ciudades',)


@admin.register(SolicitudInformacion)
class SolicitudInformacionAdmin(admin.ModelAdmin):
    list_display = ('oferta', 'usuario', 'fecha')
    list_filter = ('fecha',)
    search_fields = ('oferta__titulo', 'usuario__username')
    readonly_fields = ('fecha',)
