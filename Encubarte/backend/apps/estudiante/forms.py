# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from Encubarte.backend.apps.estudiante.models import Estudiante, DatosFamiliaMayor, DatosFamiliaMenor
from django.contrib.auth.models import User

class EstudianteForm(forms.ModelForm):
	class Meta:
		model = Estudiante
		exclude = ['user']

	def __str__(self):
		return self.user.username+" "+self.user.first_name+" "+self.user.last_name

class DatosMayorForm(forms.ModelForm):
	class Meta:
		model = DatosFamiliaMayor
		exclude = ['idEstudiante']


class DatosMenorForm(forms.ModelForm):
	class Meta:
		model = DatosFamiliaMenor
		exclude = ['idEstudiante']
