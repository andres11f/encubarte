# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import Encubarte.backend.apps.administrador.views
from Encubarte.backend.apps.administrador.views import LogAdministrador, VerSolicitudes
from Encubarte.backend.apps.generales.views import CamPass

admin.autodiscover()

urlpatterns = patterns('Encubarte.backend.apps.administrador.views',

    url(r'^admin/', include(admin.site.urls)),
    
    #links administrador:
    url(r'^/?$', LogAdministrador.as_view(), name='inicio'),
    url(r'^registroProfesor/', Encubarte.backend.apps.administrador.views.registroProfesorControl),
    url(r'^registroCurso/', Encubarte.backend.apps.administrador.views.registroCursoControl),
    url(r'^registroHorario/', Encubarte.backend.apps.administrador.views.registroHorarioControl),
    url(r'^verSolicitudes/', VerSolicitudes.as_view(), name='verSolicitudes'),
    #url(r'^revisarSolicitud/', revisarSolicitud.as_view(), name='revisarSolicitudes')

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^frontend/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )