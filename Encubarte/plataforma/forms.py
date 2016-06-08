from django import forms
from django.forms import ModelForm
from Encubarte.plataforma.models import Estudiante, Horario, Profesor
from django.contrib.auth.models import User
from crispy_forms.helper import FormHelper

class EstudianteForm(forms.ModelForm):
	class Meta:
		model = Estudiante
		exclude = ['user']

	#def url(self,filename):
	#	return "fotos/carros/%s/%s/%s/%s"%(self.marca, self.referencia, self.placa , filename)
	
	#foto = forms.FileField(upload_to=url)

	def __str__(self):
		return self.user.username+" "+self.user.first_name+" "+self.user.last_name

class ProfesorForm(forms.ModelForm):
	class Meta:
		model = Profesor
		exclude = ['username']

class UserForm(forms.ModelForm):
	class Meta:
		model = User
		fields = ['first_name', 'last_name']