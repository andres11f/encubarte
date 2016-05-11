from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import Encubarte.plataforma.views

admin.autodiscover()

urlpatterns = patterns('Encubarte.plataforma.views',
    url(r'^admin/', include(admin.site.urls)),
    #Links publicos:
    url(r'^$', Encubarte.plataforma.views.inicioControl),
    url(r'^registroEstudiante/$', Encubarte.plataforma.views.registroEstudianteControl),
    url(r'^login/$', Encubarte.plataforma.views.loginControl),
    #links administrador:
    url(r'^registroProfesor/$', Encubarte.plataforma.views.registroProfesorControl),
    url(r'^registroCurso/$', Encubarte.plataforma.views.registroCursoControl),
    url(r'^registroHorario/$', Encubarte.plataforma.views.registroHorarioControl),

    #links para usuarios conectados:
    url(r'^logout/$', Encubarte.plataforma.views.logoutControl),
    url(r'^404/$', Encubarte.plataforma.views.notFoundControl),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )