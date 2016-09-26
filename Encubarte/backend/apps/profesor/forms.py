# -*- coding: utf-8 -*-
from django import forms
from django.forms import ModelForm
from Encubarte.backend.apps.profesor.models import Profesor
from django.contrib.auth.models import User


class ProfesorForm(forms.ModelForm):
	class Meta:
		model = Profesor
		exclude = ['user']

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name']