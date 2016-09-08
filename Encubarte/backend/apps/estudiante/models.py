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

	def __str__(self):
		return self.user.username+" - "+self.user.first_name+" "+self.user.last_name


	class Meta:
		verbose_name_plural=u'Estudiante'

class DatosFamiliaMayor(models.Model):
	id = models.AutoField(primary_key=True)
	idEstudiante = models.OneToOneField(Estudiante)
	nombreContacto = models.CharField(max_length=50)
	telefonoContacto = models.IntegerField()
	desempeno = models.CharField(max_length=50)
	lugar = models.CharField(max_length=50)

	def urlCedula(self, filename):
		return "documentos/%s/%s"%(self.idEstudiante.user.username, "cedula.jpg")
	cedula = models.FileField(upload_to=urlCedula)
	
	def urlFoto(self, filename):
		return "documentos/%s/%s"%(self.idEstudiante.user.username, "foto.jpg")
	foto = models.FileField(upload_to=urlFoto)

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

	def urlDocumento(self,filename):
		return "documentos/%s/%s"%(self.idEstudiante.user.username, "documento")
	documento = models.FileField(upload_to=urlDocumento)
	def urlCedula(self,filename):
		return "documentos/%s/%s"%(self.idEstudiante.user.username, "cedula")
	cedula = models.FileField(upload_to=urlCedula)
	def urlFoto(self,filename):
		return "documentos/%s/%s"%(self.idEstudiante.user.username, "foto")
	foto = models.FileField(upload_to=urlFoto)

	class Meta:
		verbose_name_plural=u'Datos Familias Menor'

