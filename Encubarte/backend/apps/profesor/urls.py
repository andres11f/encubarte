# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import Encubarte.backend.apps.profesor.views
from Encubarte.backend.apps.profesor.views import LogProfesor, ModificarInfoProfesor, MatricularEstudiante
from Encubarte.backend.apps.generales.views import CamPass

admin.autodiscover()

urlpatterns = patterns('Encubarte.backend.apps.profesor.views',

    #Links Profesores:
    url(r'^/?$', LogProfesor.as_view(), name='Estudiante'),
    url(r'^listaCursos/$', Encubarte.backend.apps.profesor.views.listaCursosControl),
    url(r'^MatricularEstu/?$', MatricularEstudiante.as_view(), name='Matricular'),
    url(r'^ModificarInfo/?$', ModificarInfoProfesor.as_view(), name='Modificar'),
    url(r'^CambiarContrasena/?$', CamPass.as_view(), name='Cambiar'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )