from django.conf.urls import include, url
from django.contrib import admin
from herramienta.views import upload_file, construir_entrenamiento_prueba_vista

urlpatterns = [
    # Examples:
    # url(r'^$', 'tesis.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^uploads/$', upload_file, name = "uploads"),
    url(r'^divisor/$', construir_entrenamiento_prueba_vista, name = "divisor"),
]
