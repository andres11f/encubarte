# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib.auth import login, authenticate, logout
from django.views.generic import base
from Encubarte.plataforma.models import Estudiante, DatosFamiliaMayor, DatosFamiliaMenor, Profesor, Horario, Curso, Grupo
from Encubarte.plataforma.parametros import parametros
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.template.defaulttags import register
import re, math, os, ast
import pdb
from datetime import timedelta, datetime, date
from django import template
import itertools

from django.core import serializers

def inicioControl(request, registerSuccess=False):
	conectado=False
	nombre=request.user.username
	misionInicio= "blabla"
	visionInicio= "blublu"
	quienesSomosInicio= "bleble"
	if request.user.is_authenticated():
		conectado=True
		estudiante= not request.user.is_staff
		nombre=request.user.first_name
		if estudiante:
			return render_to_response('Estudiante/LogEstudiante.html',locals(), context_instance = RequestContext(request))
		else:
			return render_to_response('inicio.html',locals(), context_instance = RequestContext(request))
	else:
		return render_to_response ('inicio.html',locals(), context_instance = RequestContext(request))

def registroEstudianteControl(request):
	if not request.user.is_authenticated():
		generos = parametros["generos"]
		tiposDocumento = parametros["tiposDocumento"]
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

			return inicioControl(request,registerSuccess=True)
		else:
			return render_to_response('registroEstudiante.html', locals(), context_instance = RequestContext(request))
	else:
		conectado = True
		nombreUsuario = request.user.username
		return render_to_response('registroEstudiante.html', locals(), context_instance = RequestContext(request))

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
		nombresCursos = parametros["nombresCursos"]
		profesores = Profesor.objects.all()
		cursos = Curso.objects.all()

		if request.method == 'POST':
			nombreCurso = request.POST["nombreCurso"]
			idProfesor = request.POST["profesor"]

			#validaciones
			try:
				user = User.objects.get(username = idProfesor.split()[0])
				profesor = Profesor.objects.get(user = user)
			except Profesor.DoesNotExist or User.DoesNotExist:
				profesor = None

			errorNombreCurso = nombreCurso not in parametros["nombresCursos"]
			errorProfesor = profesor is None

			try:
				tmp = Curso.objects.get(nombre = nombreCurso, idProfesor = profesor)
			except Curso.DoesNotExist:
				tmp = None
			errorCursoYaExiste = tmp is not None

			if (errorNombreCurso or errorProfesor or errorCursoYaExiste):
				return render_to_response('Administrador/registroCurso.html', locals(), context_instance = RequestContext(request))

			#guardo objeto en base de datos
			curso = Curso(nombre = nombreCurso, idProfesor = profesor)#Profesor.objects.get(nombre = profesor))
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

def listaCursosControl(request):
	if request.user.is_authenticated() and request.user.is_staff:
		idProfesor = Profesor.objects.get(user = request.user)
		cursos = Curso.objects.filter(idProfesor = idProfesor)
		print("--------------------CURSOS----------------")
		print(cursos)
		return render_to_response('Profesor/listaCursos.html',locals(), context_instance = RequestContext(request))

def notFoundControl(request):
	return render_to_response('404.html',locals(),context_instance = RequestContext(request))

def fechaCorrecta(fecha):
	try:
		datetime.strptime(fecha, '%Y-%m-%d')
		return True
	except:
		return False

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
		curso = Curso.objects.all()
		return render_to_response('Estudiante\MatricularCurso.html', {"cursos":curso})

class horarioControl(base.View):
	def get(self, request, *args, **kwargs):
		diasSemana = parametros["diasSemana"]
		horas = parametros["horas"]
		horario = horarioUsuario(request.user)
		return render_to_response('Estudiante\VerHorario.html', locals(), context_instance = RequestContext(request))

class LogEstudiante(base.View):
	def get(self, request, *args, **kwargs):
		return render_to_response('Estudiante\LogEstudiante.html', locals(), context_instance = RequestContext(request))

class CamPassEstudiante(base.View):
	def get(self, request, *args, **kwargs):
		return render_to_response('Estudiante\CambiarContraseña.html', locals(), context_instance = RequestContext(request))

	def post(self, request, *args, **kwargs):
		return render_to_response('Estudiante\CambiarContraseña.html', locals(), context_instance = RequestContext(request))

class ModificarInformacion(base.View):
	def get(self, request, *args, **kwargs):
		return render_to_response('Estudiante\ModificarInfo.html', locals(), context_instance = RequestContext(request))

	def post(self, request, *args, **kwargs):
		return render_to_response('Estudiante\ModificarInfo.html', locals(), context_instance = RequestContext(request))

@register.filter
def get_item(dictionary, key):
	return dictionary.get((key.split(",")[0], key.split(",")[1]))

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