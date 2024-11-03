from django.conf import settings
from django.conf.urls.static import static
from django.urls import path, include
from store import views
from django.contrib import admin  # Asegúrate de importar admin aquí


urlpatterns = [
    path('admin/', admin.site.urls),  # Ahora admin está correctamente definido
    path('', views.base, name='home'),
    path('store/', include('store.urls')),
]
# Configuración para servir archivos de medios en desarrollo
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
