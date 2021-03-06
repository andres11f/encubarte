# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import Encubarte.backend.apps.profesor.views
from Encubarte.backend.apps.profesor.views import LogProfesor, ModificarInfoProfesor, MatricularEstudiante, listaCursosControl
from Encubarte.backend.apps.generales.views import CamPass

admin.autodiscover()

urlpatterns = patterns('Encubarte.backend.apps.profesor.views',

    #Links Profesores:
    url(r'^$', LogProfesor.as_view(), name='Profesor'),
    url(r'^listaCursos/$', listaCursosControl.as_view(), name='listaCursos'),
    #url(r'^listaCursos/$', Encubarte.backend.apps.profesor.views.listaCursosControl),
    url(r'^MatricularEstu/?$', MatricularEstudiante.as_view(), name='Matricular'),
    url(r'^ModificarInfo/?$', ModificarInfoProfesor.as_view(), name='Modificar'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^frontend/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )