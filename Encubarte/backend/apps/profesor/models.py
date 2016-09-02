# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User



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

