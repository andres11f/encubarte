# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from Encubarte.backend.apps.estudiante.models import Estudiante
from Encubarte.backend.apps.profesor.models import Profesor


class Curso(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=50)
	idProfesor = models.ForeignKey(Profesor)
	numeroGrupo = models.IntegerField()
	esCerrado = models.BooleanField()
	
	def __str__(self):
		return self.nombre + " Grupo " + str(self.numeroGrupo) + " - " + self.idProfesor.user.first_name + " " + self.idProfesor.user.last_name 

class Horario(models.Model):
	id = models.AutoField(primary_key=True)
	idCurso = models.ForeignKey(Curso)
	dia = models.CharField(max_length=20)
	horaInicio = models.TimeField()
	horaFin = models.TimeField()
	
	def __str__(self):
		return self.idCurso.nombre + " - " + self.idCurso.idProfesor.user.first_name + " " + self.idCurso.idProfesor.user.last_name + ": " + self.dia + " " + self.horaInicio.strftime("%H:%M") + " - " + self.horaFin.strftime("%H:%M")

class Grupo(models.Model):
	id = models.AutoField(primary_key=True)
	idEstudiante = models.ForeignKey(Estudiante)
	idCurso = models.ForeignKey(Curso)

	def __str__(self):
		return "Estudiante: " + self.idEstudiante.user.username + " Curso: " + self.idCurso.nombre + " - " + self.idCurso.idProfesor.user.first_name + " " + self.idCurso.idProfesor.user.last_name

class Roles (models.Model):
	id = models.AutoField(primary_key=True)
	IDuser = models.ForeignKey(User)
	Estudiante = models.BooleanField()
	Profesor = models.BooleanField()
	Administrador = models.BooleanField()

	class Meta:
		verbose_name_plural=u'Roles'