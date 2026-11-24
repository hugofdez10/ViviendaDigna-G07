from django.conf import settings
from django.conf.urls.i18n import i18n_patterns
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path
from django.utils.translation import get_language_from_path, override
from django.views.i18n import set_language
from appViviendaDigna import views


def cambiar_idioma(request):
    destino = request.POST.get('next', request.GET.get('next', ''))
    idioma_origen = get_language_from_path(destino) or request.LANGUAGE_CODE
    # La ruta del selector es neutra. Resuelve «next» en su idioma de origen.
    with override(idioma_origen):
        return set_language(request)


urlpatterns = [
    path('admin/', admin.site.urls),
    path('i18n/setlang/', cambiar_idioma, name='set_language'),
]

urlpatterns += i18n_patterns(
    path('', views.InicioView.as_view(), name='inicio'),
    path('appViviendaDigna/', include('appViviendaDigna.urls')),
    prefix_default_language=False,
)

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
