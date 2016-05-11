from django.contrib import admin
from Encubarte.plataforma.models import Estudiante, DatosFamiliaMayor, DatosFamiliaMenor, Profesor, Horario, Curso, Grupo

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