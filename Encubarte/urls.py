# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import Encubarte.plataforma.views
from Encubarte.plataforma.views import matriculaControl, LogEstudiante, horarioControl, inicioControl, CamPass, ModificarInfoEstudiante, ModificarInfoProfesor, MatricularEstudiante, RegistroEstudiante

admin.autodiscover()

urlpatterns = patterns('Encubarte.plataforma.views',
    url(r'^admin/', include(admin.site.urls)),
    
    #Links publicos:
    url(r'^$', Encubarte.plataforma.views.inicioControl),
    url(r'^registroEstudiante/$', RegistroEstudiante.as_view(), name='registrar'),
    url(r'^login/$', Encubarte.plataforma.views.loginControl),

    #links para usuarios conectados:
    url(r'^logout/$', Encubarte.plataforma.views.logoutControl),
    url(r'^404/$', Encubarte.plataforma.views.notFoundControl),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )
