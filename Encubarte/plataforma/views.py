# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib.auth import login, authenticate, logout
from django.views.generic import base
from Encubarte.plataforma.models import Estudiante, DatosFamiliaMayor, DatosFamiliaMenor, Profesor, Horario, Curso, Grupo
from Encubarte.plataforma.parametros import parametros
from Encubarte.plataforma.forms import EstudianteForm, ProfesorForm, UserForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.template.defaulttags import register
import re, math, os, ast
import pdb
from datetime import timedelta, datetime, date
from django import template
import itertools

from django.core import serializers

#__________________________________________________________________________________________________________________________________________________#
#________________________________________________VISTAS GENERALES__________________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#

def inicioControl(request, registerSuccess=False):
	conectado=False
	misionInicio= "blabla"
	visionInicio= "blublu"
	quienesSomosInicio= "bleble"
	if request.user.is_authenticated():
		conectado=True
		estudiante= not request.user.is_staff
		nombre=request.user.first_name + " " + request.user.last_name
		if estudiante:
			return render_to_response('Estudiante/LogEstudiante.html',locals(), context_instance = RequestContext(request))
		else:
			return render_to_response('inicio.html',locals(), context_instance = RequestContext(request))
	else:
		return render_to_response ('inicio.html',locals(), context_instance = RequestContext(request))

def loginControl(request):
	try:
		username = request.POST['username']
		password = request.POST['password']
		if '@' in username:
			correo = username
			username = User.objects.get(email=correo).username

		usuario = authenticate(username=username, password=password)
		if usuario is not None and usuario.is_active:
			login(request, usuario)
			usuario = request.user
			conectado= True
			return HttpResponseRedirect('/')
	except:
		return HttpResponseRedirect('/')
	loginFailed = True
	misionInicio= "blue"
	visionInicio= "red"
	quienesSomosInicio= "yellow"
	return render_to_response('inicio.html', locals(), context_instance = RequestContext(request))

def logoutControl(request):
    logout(request)
    return HttpResponseRedirect('/')

def notFoundControl(request):
	return render_to_response('404.html',locals(),context_instance = RequestContext(request))

def fechaCorrecta(fecha):
	try:
		datetime.strptime(fecha, '%Y-%m-%d')
		return True
	except:
		return False

class CamPass(base.View):
	def get(self, request, *args, **kwargs):
		return render_to_response('CambiarContraseña.html', locals(), context_instance = RequestContext(request))

	def post(self, request, *args, **kwargs):

		PastPassword = request.POST['PastPassword']
		NewPassword = request.POST['NewPassword']
		NewPassword2 = request.POST['NewPassword2']
		if request.user.check_password(PastPassword):
			if 	NewPassword == NewPassword2:
				request.user.set_password(NewPassword)
				request.user.save()
				operationSuccess = True
				return render_to_response('inicio.html', locals(), context_instance = RequestContext(request))
			else:
				ChangedFailed = True
				return render_to_response('CambiarContraseña.html', locals(), context_instance = RequestContext(request))
				#return HttpResponseRedirect("LogEstudiante/CambiarContraseña")
		else:
			PassFailed = True
			return render_to_response('CambiarContraseña.html', locals(), context_instance = RequestContext(request))
			#return HttpResponseRedirect("LogEstudiante/CambiarContraseña")


	#	return render_to_response('Estudiante\CambiarContraseña.html', locals(), context_instance = RequestContext(request))


#__________________________________________________________________________________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#

#__________________________________________________________________________________________________________________________________________________#
#___________________________________________________________VISTAS DE ADMINISTRADOR________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#

def registroProfesorControl(request):
	if request.user.is_authenticated() and request.user.is_superuser:
		generos = parametros["generos"]
		tiposDocumento = parametros["tiposDocumento"]
		profesores = Profesor.objects.all()

		if request.method == 'POST':
			#Toma de datos
			numeroDocumento = request.POST["numeroDocumento"]
			correoElectronico = request.POST["correoElectronico"]
			contrasena = request.POST["contrasena"]
			contrasena2 = request.POST["contrasena2"]
			nombres = request.POST["nombres"]
			apellidos = request.POST["apellidos"]
			fechaNacimiento = request.POST['fechaNacimiento']
			tipoDocumento = request.POST["tipoDocumento"]
			genero = request.POST['genero']
	
			#Validaciones
			errorNumeroDocumento = (User.objects.filter(username=numeroDocumento) or  not re.match("^([0-9]{8,20})$",numeroDocumento))
			errorCorreoElectronico = (User.objects.filter(email=correoElectronico) or not re.match(r"^[A-Za-z0-9\._-]+@[A-Za-z0-9]+\.[a-zA-Z]+$", correoElectronico))
			errorContrasena = (request.POST["contrasena"]!=request.POST["contrasena2"])
			errorFechaNacimiento = not fechaCorrecta(fechaNacimiento)
			errorTipoDocumento = (tipoDocumento  not in (parametros["tiposDocumento"]))
			errorGenero = (genero not in (parametros["generos"]))
	
			if (errorNumeroDocumento or errorCorreoElectronico or errorContrasena or errorFechaNacimiento or errorTipoDocumento or errorGenero):
				return render_to_response('Administrador/registroProfesor.html', locals(), context_instance = RequestContext(request))
	
			#Guardar usuario
			usuario = User.objects.create_user(username=numeroDocumento, email=correoElectronico, password=contrasena)
			usuario.first_name = nombres
			usuario.last_name = apellidos
			usuario.is_staff = True
			usuario.save()
	
			#Guardar profesor
			profesor = Profesor(user = usuario, fechaNacimiento = fechaNacimiento, tipoDocumento = tipoDocumento, genero = genero)
			profesor.save();
	
			return inicioControl(request,registerSuccess=True)
		else:
			if(request.GET.get('eliminarProfesor')):
				user = User.objects.get(username = request.GET.get('username'))
				profesorAEliminar = Profesor.objects.get(user = user)
				profesorAEliminar.delete()
			return render_to_response('Administrador/registroProfesor.html', locals(), context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/404')

def registroCursoControl(request):
	if request.user.is_authenticated() and request.user.is_superuser:
		numerosGrupos = parametros["numerosGrupos"]
		profesores = Profesor.objects.all()
		cursos = Curso.objects.all()
		
		if request.method == 'POST':
			nombreCurso = request.POST["nombreCurso"]
			usernameProfesor = request.POST["profesor"]
			numeroGrupo = request.POST["numeroGrupo"]

			esCerrado = False
			if "esCursoCerrado" in request.POST.keys(): esCerrado = True

			#validaciones
			try:
				user = User.objects.get(username = usernameProfesor)
				profesor = Profesor.objects.get(user = user)
			except Profesor.DoesNotExist or User.DoesNotExist:
				profesor = None

			errorProfesor = profesor is None
			errorNumeroGrupo = (int(numeroGrupo) not in parametros["numerosGrupos"])

			try:
				tmp = Curso.objects.get(nombre = nombreCurso, idProfesor = profesor, numeroGrupo = numeroGrupo)
			except Curso.DoesNotExist:
				tmp = None
			errorCursoYaExiste = tmp is not None

			if (errorProfesor or errorNumeroGrupo or errorCursoYaExiste):
				return render_to_response('Administrador/registroCurso.html', locals(), context_instance = RequestContext(request))

			#guardo objeto en base de datos
			curso = Curso(nombre = nombreCurso, idProfesor = profesor, numeroGrupo = numeroGrupo, esCerrado = esCerrado)#Profesor.objects.get(nombre = profesor))
			curso.save()
			operationSuccess = True
			return render_to_response('Administrador/registroCurso.html', locals(), context_instance = RequestContext(request))
		else:
			if(request.GET.get('eliminarCurso')):				
				cursoAEliminar = Curso.objects.get(id = request.GET.get('id'))
				cursoAEliminar.delete()
			return render_to_response('Administrador/registroCurso.html', locals(), context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/404')

def registroHorarioControl(request):
	if request.user.is_authenticated() and request.user.is_superuser:
		cursos = Curso.objects.all()
		dias = parametros["diasSemana"]
		horas = parametros["horas"]
		horarios = Horario.objects.all().order_by('idCurso')

		if request.method == 'POST':
			idCurso = request.POST["idCurso"]
			dia = request.POST["dia"]
			horaInicio = request.POST["horaInicio"]
			horaFinal = request.POST["horaFin"]

			#validaciones
			try:
				curso = Curso.objects.get(id = idCurso)
			except Curso.DoesNotExist:
				curso = None

			errorCurso = curso is None
			errorDia = dia not in parametros["diasSemana"]
			errorHora = (horaInicio not in parametros["horas"] or horaFinal not in parametros["horas"])
			horaInicioFormato = datetime.strptime(horaInicio, '%H:%M').time()
			horaFinFormato = datetime.strptime(horaFinal, '%H:%M').time()
			errorHoraFin = horaFinFormato < horaInicioFormato

			if (errorCurso or errorDia or errorHora or errorHoraFin):
				return render_to_response('Administrador/registroHorario.html', locals(), context_instance = RequestContext(request))

			#guardo objeto
			horario = Horario(idCurso = curso, dia = dia, horaInicio = horaInicioFormato, horaFin = horaFinFormato)
			horario.save()
			operationSuccess = True
			return render_to_response('Administrador/registroHorario.html', locals(), context_instance = RequestContext(request))
		else:
			if(request.GET.get('eliminarHorario')):				
				horarioAEliminar = Horario.objects.get(id = request.GET.get('id'))
				horarioAEliminar.delete()
			return render_to_response('Administrador/registroHorario.html', locals(), context_instance = RequestContext(request))
	else:
		return HttpResponseRedirect('/404')


#__________________________________________________________________________________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#

#__________________________________________________________________________________________________________________________________________________#
#______________________________________________________________VISTAS DE PROFESOR__________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#

class ModificarInfoProfesor(base.View):
	def get(self, request, *args, **kwargs):
		user = User.objects.get(username = request.user.username)
		profesor = Profesor.objects.get(user = user)
		generos = parametros["generos"]
		tiposDocumento = parametros["tiposDocumento"]
		if request.user.is_authenticated():
			form = ProfesorForm(instance=profesor)
			formUser = UserForm(instance=user)
			return render_to_response('Profesor\ModificarInfo.html', locals(), context_instance = RequestContext(request))
		

	def post(self, request, *args, **kwargs):
		user = User.objects.get(username = request.user.username)
		profesor = Profesor.objects.get(user = user)

		user.first_name = request.POST["first_name"]
		user.last_name = request.POST["last_name"]		
		profesor.tipoDocumento = request.POST["tipoDocumento"]
		profesor.fechaNacimiento = request.POST['fechaNacimiento']
		profesor.genero = request.POST['genero']
		
		#Validaciones
		errorTipoDocumento = (profesor.tipoDocumento  not in (parametros["tiposDocumento"]))
		errorFechaNacimiento = not fechaCorrecta(profesor.fechaNacimiento)
		errorGenero = (profesor.genero not in (parametros["generos"]))

		if (errorTipoDocumento or errorFechaNacimiento or errorGenero):
			return render_to_response('registroEstudiante.html', locals(), context_instance = RequestContext(request))
	
        #Guardar usuario
		user.save()
		profesor.save()

		operationSuccess = True
		return render_to_response('Estudiante\LogEstudiante.html', locals(), context_instance = RequestContext(request))



class MatricularEstudiante(base.View):
	def get(self, request, *args, **kwargs):
		profesor = Profesor.objects.get(user = request.user)
		cursos = Curso.objects.filter(idProfesor = profesor)
		return render_to_response('Profesor/MatricularEstudiante.html',  locals(), context_instance = RequestContext(request)) 

	def post(self, request, *args, **kwargs):
		profesor = Profesor.objects.get(user = request.user)
		cursos = Curso.objects.filter(idProfesor = profesor)
		curso_grupo = request.POST['horario'].split(" Grupo ")
		print ("==========================> NoNO <================================")
		cursoMatricular = curso_grupo[0] #nombre a matricular en string
		grupoCurso = curso_grupo[1] #grupo del curso a matricular
		cursoID = Curso.objects.get(nombre=cursoMatricular, numeroGrupo=grupoCurso) #IdCurso a partir del nombre del curso
		horarioNuevo = Horario.objects.filter(idCurso = cursoID)
		print(cursoMatricular)
		print (grupoCurso)
		print(cursoID)
		print (horarioNuevo)
		estudianteaMatricular = User.objects.get(username=request.POST['numeroDocumento'])
		#codigoEstudiante = request.GET['numeroDocumento']

		try:
			print ("==========================> Cerveza <================================")
			estudiante = Estudiante.objects.get(user = estudianteaMatricular)
			gruposEstudiante = Grupo.objects.filter(idEstudiante = estudiante)
			print(estudiante)
			print (gruposEstudiante)
		except estudiante.DoesNotExist:
			estudiante = None

		errorEstudiante = estudiante is None

		if errorEstudiante:
			return render_to_response('Profesor/MatricularEstudiante.html', locals(), context_instance = RequestContext(request))

		HorarioEmpty = True

		for grupoE in gruposEstudiante:
			HorarioEmpty = False
			horariosGrupo = Horario.objects.filter(idCurso = grupoE.idCurso)
			print(grupoE.idCurso)
			print(horariosGrupo)
			print(HorarioEmpty)

		CursoDiferente = False
		HorarioLibre = False

		print ("==========================> PERRO <================================")
		print(HorarioEmpty)

		if not HorarioEmpty:
			for horario in horarioNuevo:
				print ("==========================> HOLA <================================")
				hora_ini = horario.horaInicio
				hora_final = horario.horaFin
				for h in horariosGrupo:
					hora_IC = h.horaInicio # hora inicio cursos matriculados
					hora_FC = h.horaFin #hora fin cursos matriculados
					if h.idCurso != horario.idCurso:
						CursoDiferente = True
						Libre = Hora_Libre(hora_IC, hora_FC, hora_ini, hora_final)
						if h.dia == horario.dia:
							if Libre:
								HorarioLibre = True
							else:
								HorarioLibre = False
								break
						else:
							HorarioLibre = True
					else:
						CursoDiferente = False
						break
		else:
			print ("==========================> CABALLO <================================")
			CursoDiferente = True
			HorarioLibre = True


		if CursoDiferente and HorarioLibre:
			MatriculaSuccess = True
			print ("==========================> EXITO <================================")
			grupo = Grupo(idEstudiante= estudiante , idCurso= cursoID)
			grupo.save()
			return render_to_response('Profesor/MatricularEstudiante.html',  locals(), context_instance = RequestContext(request))
		elif not CursoDiferente:
				print ("==========================> CURSANDOCURSO <================================")
				CursandoCurso = True
				return render_to_response('Profesor/MatricularEstudiante.html',  locals(), context_instance = RequestContext(request))
		else:
			print ("==========================> HORAOCUPADA <================================")
			HoraOcupada = True
			return render_to_response('Profesor/MatricularEstudiante.html',  locals(), context_instance = RequestContext(request))


def listaCursosControl(request):
	if request.user.is_authenticated() and request.user.is_staff:
		idProfesor = Profesor.objects.get(user = request.user)
		cursos = Curso.objects.filter(idProfesor = idProfesor)
		print("--------------------CURSOS----------------")
		print(cursos)
		return render_to_response('Profesor/listaCursos.html',locals(), context_instance = RequestContext(request))

#__________________________________________________________________________________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#

#__________________________________________________________________________________________________________________________________________________#
#___________________________________________________________VISTAS DE ESTUDIANTE___________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#

def registroEstudianteControl(request):
	if not request.user.is_authenticated():
		generos = parametros["generos"]
		tiposDocumento = parametros["tiposDocumento"]
		zonas = parametros["zonas"]
		if request.method == 'POST':
			#Toma de datos
			numeroDocumento = request.POST["numeroDocumento"]
			tipoDocumento = request.POST["tipoDocumento"]
			contrasena = request.POST["contrasena"]
			contrasena2 = request.POST["contrasena2"]
			correoElectronico = request.POST["correoElectronico"]
			nombres = request.POST["nombres"]
			apellidos = request.POST["apellidos"]
			fechaNacimiento = request.POST['fechaNacimiento']
			genero = request.POST['genero']
			direccion = request.POST['direccion']
			barrio = request.POST['barrio']
			telefonoFijo = request.POST['telefonoFijo']
			telefonoCelular = request.POST['telefonoCelular']
			seguridadSocial = request.POST['seguridadSocial']
			documento = request.FILES["documento"]

			#Inicializo datos opcionales
			zona = ""
			comuna = ""
			grupoEtnico = ""
			condicion = ""
			enviarInfoAlCorreo = False

			#Tomo los datos opcionales que el usuario haya ingresado
			if request.POST['zona']: zona = request.POST['zona']
			if request.POST['comuna']: comuna = request.POST['comuna']
			if request.POST['grupoEtnico']: grupoEtnico = request.POST['grupoEtnico']
			if request.POST['condicion']: condicion = request.POST['condicion']
			if "enviarInfoAlCorreo" in request.POST.keys(): enviarInfoAlCorreo = True

			#Validaciones
			errorNumeroDocumento = (User.objects.filter(username=numeroDocumento) or  not re.match("^([0-9]{8,20})$",numeroDocumento))
			errorTipoDocumento = (tipoDocumento  not in (parametros["tiposDocumento"]))
			errorContrasena = (request.POST["contrasena"]!=request.POST["contrasena2"])
			errorCorreoElectronico = (User.objects.filter(email=correoElectronico) or not re.match(r"^[A-Za-z0-9\._-]+@[A-Za-z0-9]+\.[a-zA-Z]+$", correoElectronico))
			errorFechaNacimiento = not fechaCorrecta(fechaNacimiento)
			errorGenero = (genero not in (parametros["generos"]))
			errorTelefonos = (not re.match("^([0-9]{7,12})$",telefonoFijo) or not re.match("^([0-9]{7,12})$",telefonoCelular))
			errorDocumento = not documento

			if (errorContrasena or errorNumeroDocumento or errorTipoDocumento or errorCorreoElectronico or errorFechaNacimiento or errorGenero or errorTelefonos or errorDocumento):
				return render_to_response('registroEstudiante.html', locals(), context_instance = RequestContext(request))

			#Guardar usuario
			usuario = User.objects.create_user(username=numeroDocumento, email=correoElectronico, password=contrasena)
			usuario.first_name = nombres
			usuario.last_name = apellidos
			usuario.save()

			#Guardo estudiante
			estudiante = Estudiante(user = usuario, tipoDocumento = tipoDocumento, fechaNacimiento = fechaNacimiento, genero = genero, direccion = direccion, barrio = barrio, zona = zona, comuna = comuna, telefonoFijo = telefonoFijo, telefonoCelular = telefonoCelular, grupoEtnico = grupoEtnico, condicion = condicion, seguridadSocial = seguridadSocial, enviarInfoAlCorreo = enviarInfoAlCorreo, documento = documento)
			estudiante.save()

			return inicioControl(request, registerSuccess=True)
		else:
			return render_to_response('registroEstudiante.html', locals(), context_instance = RequestContext(request))
	else:
		conectado = True
		nombreUsuario = request.user.username
		return render_to_response('registroEstudiante.html', locals(), context_instance = RequestContext(request))

def horarioUsuario(User):
	horas = parametros["horas"]
	diasSemana = parametros["diasSemana"]
	
	horario = dict()

	for d in diasSemana:
		for h in horas:
			horario[(d, h)] = ''

	try:
		estudiante = Estudiante.objects.get(user = User)
		gruposEstudiante = Grupo.objects.filter(idEstudiante = estudiante)
	except:
		return {}

	for grupoE in gruposEstudiante:
		horariosGrupo = Horario.objects.filter(idCurso = grupoE.idCurso)

		for h in horariosGrupo:
			horaInicio = h.horaInicio
			horaFin = h.horaFin
			horaTmp = horaInicio

			while horaTmp < horaFin:
				if horaTmp.strftime("%H:%M") in horas and h.dia in diasSemana:
					horario[(h.dia, horaTmp.strftime("%H:%M"))] = h.idCurso.nombre
				horaTmp = (datetime.combine(date.today(), horaTmp) + timedelta(hours=1)).time()

	return horario	
	"""
	for d in diasSemana:
		for h in horas:
			try:
				tmpHorario = Horario.objects.get(dia = d, hora = h)
			except Horario.DoesNotExist:
				tmpHorario = None

			if tmpHorario is None:
				horario[h].append('')
			else:
				if gruposEstudiante.filter(idCurso = tmpHorario.idCurso):
					horario[h].append(tmpHorario.idCurso.nombre)
				else:
					horario[h].append('')
	"""
	#por cada grupo del estudiante
		#obtengo el id del curso
			#obtengo los horarios asociados a ese curso
				#por cada horario obtengo el horario de inicio a final
					#por cada hora entre la hora de inicio y final
						#horario[hora] = idcurso.nombre

class matriculaControl(base.View):
	def get(self, request, *args, **kwargs):
		if(request.GET.get('VerHorario')):
			cursos = Curso.objects.filter(esCerrado=False)
			curso_grupo = request.GET['horario'].split(" Grupo ")
			print ("==========================> NoNO <================================")
			cursoMatricular = curso_grupo[0] #nombre a matricular en string
			grupoCurso = curso_grupo[1] #grupo del curso a matricular
			print(cursoMatricular)
			print(grupoCurso)
			cursoID = Curso.objects.get(nombre=cursoMatricular, numeroGrupo=grupoCurso) #IdCurso a partir del nombre del curso
			horarioVer = Horario.objects.filter(idCurso = cursoID)
			print(horarioVer)
			MostrarHorario = True
			return render_to_response('Estudiante\MatricularCurso.html',  locals(), context_instance = RequestContext(request)) 
		else:
			MostrarHorario = False
			cursos = Curso.objects.filter(esCerrado=False)
			horarios = Horario.objects.all()
			return render_to_response('Estudiante\MatricularCurso.html',  locals(), context_instance = RequestContext(request)) 

	def post(self, request, *args, **kwargs):
		cursos = Curso.objects.filter(esCerrado=False)
		horarios = Horario.objects.all()
		cursoMatricular = request.POST['idCurso'] #nombre a matricular en string
		grupoCurso = request.POST['idGrupo'] #grupo del curso a matricular
		cursoID = Curso.objects.get(nombre=cursoMatricular, numeroGrupo=grupoCurso) #IdCurso a partir del nombre del curso y numero de grupo
		horarioNuevo = Horario.objects.filter(idCurso = cursoID)
		print(horarioNuevo)
		#dia = horarioNuevo.dia

		try:
			print ("==========================> NoNO <================================")
			user = User.objects.get(username = request.user.username)
			print(user)
			estudiante = Estudiante.objects.get(user = user)
			print(estudiante)
			gruposEstudiante = Grupo.objects.filter(idEstudiante = estudiante)
			print (gruposEstudiante)
		except:
			return {}

		HorarioEmpty = True

		for grupoE in gruposEstudiante:
			HorarioEmpty = False
			horariosGrupo = Horario.objects.filter(idCurso = grupoE.idCurso)
			print ("==========================> LUNA <================================")
			print(grupoE.idCurso)
			print(horariosGrupo)
			print(HorarioEmpty)
			

		CursoDiferente = False
		HorarioLibre = False
		print ("==========================> PERRO <================================")
		print(HorarioEmpty)

		if not HorarioEmpty:
			for horario in horarioNuevo:
				print ("==========================> HOLA <================================")
				hora_ini = horario.horaInicio
				hora_final = horario.horaFin
				for h in horariosGrupo:
					hora_IC = h.horaInicio # hora inicio cursos matriculados
					hora_FC = h.horaFin #hora fin cursos matriculados
					if h.idCurso != horario.idCurso:
						CursoDiferente = True
						Libre = Hora_Libre(hora_IC, hora_FC, hora_ini, hora_final)
						if h.dia == horario.dia:
							if Libre:
								HorarioLibre = True
							else:
								HorarioLibre = False
								break
						else:
							HorarioLibre = True
					else:
						CursoDiferente = False
						break
		else:
			print ("==========================> CABALLO <================================")
			CursoDiferente = True
			HorarioLibre = True

		if CursoDiferente and HorarioLibre:
			MatriculaSuccess = True
			grupo = Grupo(idEstudiante= estudiante , idCurso= cursoID)
			grupo.save()
			return render_to_response('Estudiante\MatricularCurso.html',  locals(), context_instance = RequestContext(request))
		elif not CursoDiferente:
				CursandoCurso = True
				return render_to_response('Estudiante\MatricularCurso.html',  locals(), context_instance = RequestContext(request))
		else:
			HoraOcupada = True
			return render_to_response('Estudiante\MatricularCurso.html',  locals(), context_instance = RequestContext(request))

class horarioControl(base.View):
	def get(self, request, *args, **kwargs):
		diasSemana = parametros["diasSemana"]
		horas = parametros["horas"]
		user = User.objects.get(username = request.user.username)

		try:
			estudiante = Estudiante.objects.get(user = user)
			gruposEstudiante= Grupo.objects.filter(idEstudiante = estudiante)
		except:
			return {}

		for grupo in gruposEstudiante:
			horarios = Horario.objects.filter(idCurso = grupo.idCurso)

		horario = horarioUsuario(request.user)
		print ("==========================> CABALLO <================================")
		print(gruposEstudiante)
		return render_to_response('Estudiante\VerHorario.html', locals(), context_instance = RequestContext(request))

class LogEstudiante(base.View):
	def get(self, request, *args, **kwargs):
		return render_to_response('Estudiante\LogEstudiante.html', locals(), context_instance = RequestContext(request))

class ModificarInfoEstudiante(base.View):
	def get(self, request, *args, **kwargs):
		user = User.objects.get(username = request.user.username)
		estudiante = Estudiante.objects.get(user = user)
		generos = parametros["generos"]
		tiposDocumento = parametros["tiposDocumento"]
		if request.user.is_authenticated():
			form = EstudianteForm(instance=estudiante)
			formUser = UserForm(instance=user)
			return render_to_response('Estudiante\ModificarInfo.html', locals(), context_instance = RequestContext(request))


	def post(self, request, *args, **kwargs):
		user = User.objects.get(username = request.user.username)
		estudiante = Estudiante.objects.get(user = user)

		user.first_name = request.POST["first_name"]
		user.last_name = request.POST["last_name"]
		estudiante.tipoDocumento = request.POST["tipoDocumento"]
		estudiante.fechaNacimiento = request.POST['fechaNacimiento']
		estudiante.genero = request.POST['genero']
		estudiante.direccion = request.POST['direccion']
		estudiante.barrio = request.POST['barrio']
		estudiante.telefonoFijo = request.POST['telefonoFijo']
		estudiante.telefonoCelular = request.POST['telefonoCelular']
		estudiante.seguridadSocial = request.POST['seguridadSocial']
		estudiante.zona = request.POST['zona']
		estudiante.comuna = request.POST['comuna']
		estudiante.grupoEtnico = request.POST['grupoEtnico']
		estudiante.condicion = request.POST['condicion']
		if "enviarInfoAlCorreo" in request.POST.keys(): enviarInfoAlCorreo = True

		#Validaciones
		errorTipoDocumento = (estudiante.tipoDocumento  not in (parametros["tiposDocumento"]))
		errorFechaNacimiento = not fechaCorrecta(estudiante.fechaNacimiento)
		errorGenero = (estudiante.genero not in (parametros["generos"]))
		errorTelefonos = (not re.match("^([0-9]{7,12})$",estudiante.telefonoFijo) or not re.match("^([0-9]{7,12})$",estudiante.telefonoCelular))

		if (errorTipoDocumento or errorFechaNacimiento or errorGenero or errorTelefonos):
			return render_to_response('registroEstudiante.html', locals(), context_instance = RequestContext(request))
	
        #Guardar usuario
		user.save()
		estudiante.save()

		operationSuccess = True
		return render_to_response('Estudiante\LogEstudiante.html', locals(), context_instance = RequestContext(request))

#__________________________________________________________________________________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#


#__________________________________________________________________________________________________________________________________________________#
#___________________________________________________________OTRAS FUNCIONES________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#

@register.filter
def get_item(dictionary, key):
	return dictionary.get((key.split(",")[0], key.split(",")[1]))


def __format__(self, format_spec):
    return format(str(self), format_spec)


def Hora_Libre(curso_ini, curso_fin, hora_ini, hora_fin):
	if curso_ini >= hora_ini and curso_fin <= hora_fin:
		libre = False
	elif hora_ini >= curso_ini and hora_fin <= curso_fin:
		libre = False
	elif curso_ini >= hora_ini and curso_ini <= hora_fin:
		libre = False
	elif hora_ini >= curso_ini and hora_ini <= curso_fin:
		libre = False
	elif hora_ini == curso_ini and hora_ini == curso_fin:
		libre = False
	else:
		libre = True

	return libre


class CycleNode(template.Node):
    def __init__(self, cyclevars):
        self.cyclevars = template.Variable(cyclevars)

    def render(self, context):
        names = self.cyclevars.resolve(context)
        if self not in context.render_context:
            context.render_context[self] = itertools.cycle(names)
        cycle_iter = context.render_context[self]
        return next(cycle_iter)

@register.tag
def cycle_list(parser, token):
    try:
        tag_name, arg = token.contents.split(None, 1)
    except ValueError:
        raise template.TemplateSyntaxError(
            "%r tag requires an argument" % token.contents.split()[0]
        )
    node = CycleNode(arg)
    return node