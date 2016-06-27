# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User

class Estudiante(models.Model):
	#Objeto user contiene: numeroDocumento como username, correoElectronico como email, contrasena como password
	#nombres como first_name, apellidos como last_name
	user = models.OneToOneField(User, primary_key=True)
	tipoDocumento = models.CharField(max_length=10)
	fechaNacimiento = models.DateField()
	genero = models.CharField(max_length=1)
	direccion = models.CharField(max_length=50)
	barrio = models.CharField(max_length=50)
	zona = models.CharField(max_length=50)
	comuna = models.CharField(max_length=50)
	telefonoFijo = models.IntegerField()
	telefonoCelular = models.IntegerField()
	grupoEtnico = models.CharField(max_length=50)
	condicion = models.CharField(max_length=50)
	seguridadSocial = models.CharField(max_length=50)
	enviarInfoAlCorreo = models.BooleanField()

	def url(self,filename):
		return "documentos/%s/%s"%(self.user.username, filename)
	documento = models.FileField(upload_to=url)

	def __str__(self):
		return self.user.username+" "+self.user.first_name+" "+self.user.last_name

class DatosFamiliaMayor(models.Model):
	id = models.AutoField(primary_key=True)
	idEstudiante = models.OneToOneField(Estudiante)
	nombreContacto = models.CharField(max_length=50)
	telefonoContacto = models.IntegerField()
	desempeno = models.CharField(max_length=50)
	lugar = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural=u'Datos Familias Mayor'

class DatosFamiliaMenor(models.Model):
	id = models.AutoField(primary_key=True)
	idEstudiante = models.OneToOneField(Estudiante)
	nombrePadre = models.CharField(max_length=50)
	nombreMadre = models.CharField(max_length=50)
	telefonoPadre = models.IntegerField()
	telefonoMadre = models.IntegerField()
	institucionEducativa = models.CharField(max_length=50)
	grupo = models.CharField(max_length=50)
	jornada = models.CharField(max_length=50)
	nombreAcudiente = models.CharField(max_length=50)
	cedulaAcudiente = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural=u'Datos Familias Menor'

class Profesor(models.Model):
	#Objeto user contiene: numeroDocumento como username, correoElectronico como email, contrasena como password
	#nombres como first_name, apellidos como last_name
	user = models.OneToOneField(User, primary_key=True)
	fechaNacimiento = models.DateField()
	tipoDocumento = models.CharField(max_length=10)
	genero = models.CharField(max_length=50)

	def __str__(self):
		#no cambiar esto o se vera afectado el comportamiento de registroCursoControl
		return self.user.username+" - "+self.user.first_name+" "+self.user.last_name

	class Meta:
		verbose_name_plural=u'Profesores'

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