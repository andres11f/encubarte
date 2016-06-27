# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import Encubarte.plataforma.views
from Encubarte.plataforma.views import matriculaControl, LogEstudiante, horarioControl, inicioControl, CamPass, ModificarInfoEstudiante, ModificarInfoProfesor, MatricularEstudiante

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

    #Links Profesores:
    url(r'^listaCursos/$', Encubarte.plataforma.views.listaCursosControl),
    url(r'^LogProfesor/MatricularEstu/?$', MatricularEstudiante.as_view(), name='Matricular'),
    url(r'^LogProfesor/ModificarInfo/?$', ModificarInfoProfesor.as_view(), name='Modificar'),
    url(r'^LogProfesor/CambiarContrasena/?$', CamPass.as_view(), name='Cambiar'),
    
    #links estudiantes:
    url(r'^LogEstudiante/CambiarContrasena/?$', CamPass.as_view(), name='Cambiar'),
    url(r'^LogEstudiante/ModificarInfo/?$', ModificarInfoEstudiante.as_view(), name='Modificar'),
    url(r'^LogEstudiante/VerHorario/?$', horarioControl.as_view(), name='Horario'),
    url(r'^LogEstudiante/MatricularCurso/?$', matriculaControl.as_view(), name='Matricular'),
    url(r'^LogEstudiante/?$', LogEstudiante.as_view(), name='Estudiante'),

    #links para usuarios conectados:
    url(r'^logout/$', Encubarte.plataforma.views.logoutControl),
    url(r'^404/$', Encubarte.plataforma.views.notFoundControl),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )