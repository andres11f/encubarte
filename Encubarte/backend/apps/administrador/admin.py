# -*- coding: utf-8 -*-
from django.contrib import admin
#from Encubarte.plataforma.models import Estudiante, DatosFamiliaMayor, DatosFamiliaMenor, Profesor, Horario, Curso, Grupo
from Encubarte.backend.apps.estudiante.models import Estudiante, DatosFamiliaMayor, DatosFamiliaMenor
from Encubarte.backend.apps.profesor.models import Profesor
from Encubarte.backend.apps.administrador.models import Solicitudes, Correcciones
from Encubarte.backend.apps.generales.models import Horario, Curso, Grupo, Roles

#class AdminMateria(admin.ModelAdmin):
#	list_filter = ('nombre',)
#	ordering = ('-nombre',)
#	search_fields = ('nombre', 'tematica', 'semestre',)

admin.site.register(Estudiante)
admin.site.register(DatosFamiliaMayor)
admin.site.register(DatosFamiliaMenor)
admin.site.register(Profesor)
admin.site.register(Horario)
admin.site.register(Curso)
admin.site.register(Grupo)
admin.site.register(Roles)
admin.site.register(Solicitudes)
admin.site.register(Correcciones)

