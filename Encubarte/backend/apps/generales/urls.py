# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
import Encubarte.backend.apps.generales
from Encubarte.backend.apps.generales.views import RegistroEstudiante2, RegistroEstudianteMenor, RegistroEstudianteMayor

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/', include(admin.site.urls)),

    #Links publicos:
    url(r'^$', Encubarte.backend.apps.generales.views.inicioControl),
    url(r'^registroEstudiante/$', RegistroEstudiante2.as_view(), name='registrar'),
    url(r'^registroEstudianteMenor/$', RegistroEstudianteMenor.as_view(), name='registrarMenor'),
    url(r'^registroEstudianteMayor/$', RegistroEstudianteMayor.as_view(), name='registrarMayor'),
    url(r'^login/$', Encubarte.backend.apps.generales.views.loginControl),
    url(r'^modulos/', include('Encubarte.backend.apps.modulos.urls')),
    url(r'^LogEstudiante/', include('Encubarte.backend.apps.estudiante.urls')),
    url(r'^LogProfesor/', include('Encubarte.backend.apps.profesor.urls')),
    url(r'^LogAdministrador/', include('Encubarte.backend.apps.administrador.urls')),
    

    #links para usuarios conectados:
    url(r'^logout/$', Encubarte.backend.apps.generales.views.logoutControl),
    url(r'^404/$', Encubarte.backend.apps.generales.views.notFoundControl),
)

if settings.DEBUG:
    urlpatterns += patterns('',
        (r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    )