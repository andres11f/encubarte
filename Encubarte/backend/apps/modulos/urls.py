# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
#import Encubarte.backend.apps.generales
from Encubarte.backend.apps.modulos.views import EscogerModulo

admin.autodiscover()

urlpatterns = patterns('Encubarte.backend.apps.modulos.views',

    #url(r'^LogEstudiante/?', include('Encubarte.backend.apps.estudiante.urls')),
    #url(r'^LogProfesor/?', include('Encubarte.backend.apps.profesor.urls')),
    #url(r'^LogAdministrador/?', include('Encubarte.backend.apps.administrador.urls')),
    url(r'^/?$', EscogerModulo.as_view(), name='escogerModulo'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )