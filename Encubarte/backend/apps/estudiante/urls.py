# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import Encubarte.backend.apps.estudiante
from Encubarte.backend.apps.estudiante.views import LogEstudiante, matriculaControl, horarioControl, ModificarInfoEstudiante
from Encubarte.backend.apps.generales.views import CamPass

admin.autodiscover()

urlpatterns = patterns('Encubarte.backend.apps.estudiante.views',
    
    #links estudiantes:
    url(r'^$', LogEstudiante.as_view(), name='Estudiante'),
    url(r'^CambiarContrasena/', CamPass.as_view(), name='Cambiar'),
    url(r'^ModificarInfo/', ModificarInfoEstudiante.as_view(), name='Modificar'),
    url(r'^VerHorario/', horarioControl.as_view(), name='Horario'),
    url(r'^MatricularCurso/', matriculaControl.as_view(), name='Matricular'),

)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^frontend/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )