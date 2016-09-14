# -*- coding: utf-8 -*-
from django.db import models
from django.contrib.auth.models import User
from Encubarte.backend.apps.estudiante.models import Estudiante

class Solicitudes(models.Model):
	id = models.AutoField(primary_key=True)
	IDestudiante = models.ForeignKey(Estudiante)
	estado = models.CharField(max_length=20)
	Correcciones = models.BooleanField()

	class Meta:
		verbose_name_plural=u'Solicitudes'

class Correcciones(models.Model):
	id = models.AutoField(primary_key=True)
	IDestudiante = models.ForeignKey(Estudiante)
	campo = models.CharField(max_length=20)

	class Meta:
		verbose_name_plural=u'Correcciones'

