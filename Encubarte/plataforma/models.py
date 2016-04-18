from django.db import models
from django.contrib.auth.models import User

class Registro(models.Model):
	#Objeto user contiene: numeroDocumento como username, correoElectronico como email, contraseña como password
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

	#def url(self,filename):
	#	return "fotos/carros/%s/%s/%s/%s"%(self.marca, self.referencia, self.placa , filename)
	#foto = models.FileField(upload_to=url)

	def __str__(self):
		return self.user.username+" "+self.user.first_name+" "+self.user.last_name

class DatosFamiliaMayor(models.Model):
	id = models.AutoField(primary_key=True)
	idRegistro = models.OneToOneField(Registro)
	nombreContacto = models.CharField(max_length=50)
	telefonoContacto = models.IntegerField()
	desempeño = models.CharField(max_length=50)
	lugar = models.CharField(max_length=50)

	class Meta:
		verbose_name_plural=u'Datos Familias Mayor'

class DatosFamiliaMenor(models.Model):
	id = models.AutoField(primary_key=True)
	idRegistro = models.OneToOneField(Registro)
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

class Curso(models.Model):
	id = models.AutoField(primary_key=True)
	nombre = models.CharField(max_length=50)

	def __str__(self):
		return self.nombre

class Profesor(models.Model):
	id = models.AutoField(primary_key=True)
	idCurso = models.ForeignKey(Curso)
	nombre = models.CharField(max_length=50)
	edad = models.IntegerField()
	genero = models.CharField(max_length=50)

	def __str__(self):
		return self.nombre

	class Meta:
		verbose_name_plural=u'Profesores'

class Horario(models.Model):
	id = models.AutoField(primary_key=True)
	idCurso = models.ForeignKey(Curso)
	dia = models.CharField(max_length=20)
	hora = models.TimeField()
	
	def __str__(self):
		return self.dia + " " + self.horario.strftime("%H:%M")

class Grupo(models.Model):
	id = models.AutoField(primary_key=True)
	idRegistro = models.ForeignKey(Registro)
	idCurso = models.ForeignKey(Curso)

	def __str__(self):
		return "Registro: " + self.idRegistro.user.username + " Curso: " + self.idCurso.nombre