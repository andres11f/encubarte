## -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib.auth import login, authenticate, logout
from django.views.generic import base
from Encubarte.backend.apps.estudiante.models import Estudiante, DatosFamiliaMayor, DatosFamiliaMenor
from Encubarte.backend.apps.administrador.models import Solicitudes, Correcciones
#from Encubarte.backend.apps.profesor.models import Profesor
from Encubarte.backend.apps.generales.models import Roles
from Encubarte.backend.apps.generales.parametros import parametros
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

class inicioControl(base.View):
    def get(self, request, *args, **kwargs):
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
                return render_to_response('Generales/inicio.html',locals(), context_instance = RequestContext(request))
        else:
            return render_to_response ('Generales/inicio.html',locals(), context_instance = RequestContext(request))


class loginControl(base.View):
     def post(self, request, *args, **kwargs):
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
                conectado = True
                #return HttpResponseRedirect("/modulos/")
                return render_to_response('Modulos/modulos.html', locals(), context_instance = RequestContext(request))
        except:
            return HttpResponseRedirect('/')
        loginFailed = True
        misionInicio= "blue"
        visionInicio= "red"
        quienesSomosInicio= "yellow"
        return render_to_response('Generales/inicio.html', locals(), context_instance = RequestContext(request))

class logoutControl(base.View):
    def get(self, request, *args, **kwargs):
        logout(request)
        return HttpResponseRedirect('/')

class notFoundControl(base.View):
    def get(self, request, *args, **kwargs):
        return render_to_response('Generales/404.html',locals(),context_instance = RequestContext(request))


class CamPass(base.View):
    def get(self, request, *args, **kwargs):
        return render_to_response('Generales/CambiarContrasena.html', locals(), context_instance = RequestContext(request))

    def post(self, request, *args, **kwargs):

        PastPassword = request.POST['PastPassword']
        NewPassword = request.POST['NewPassword']
        NewPassword2 = request.POST['NewPassword2']
        if request.user.check_password(PastPassword):
            if  NewPassword == NewPassword2:
                request.user.set_password(NewPassword)
                request.user.save()
                operationSuccess = True
                return render_to_response('Generales/inicio.html', locals(), context_instance = RequestContext(request))
            else:
                ChangedFailed = True
                return render_to_response('Generales/CambiarContrasena.html', locals(), context_instance = RequestContext(request))
                #return HttpResponseRedirect("LogEstudiante/CambiarContrasena")
        else:
            PassFailed = True
            return render_to_response('Generales/CambiarContrasena.html', locals(), context_instance = RequestContext(request))
            #return HttpResponseRedirect("LogEstudiante/CambiarContrasena")


    #   return render_to_response('Estudiante\CambiarContrasena.html', locals(), context_instance = RequestContext(request))


class RegistroEstudianteMayor(base.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            generos = parametros['generos']
            tiposDocumento = parametros['tiposDocumento']
            zonas = parametros['zonas']
            return render_to_response('Generales/registroEstudianteMayor.html', locals(), context_instance = RequestContext(request))
        else:
            conectado = True
            nombreUsuario = request.user.username
            return render_to_response('Generales/inicio.html', locals(), context_instance = RequestContext(request))

    def post(self, request, *args, **kwargs):
        generos = parametros['generos']
        tiposDocumento = parametros['tiposDocumento']
        zonas = parametros['zonas']

        #Toma de datos
        numeroDocumento = request.POST['numeroDocumento']
        tipoDocumento = request.POST['tipoDocumento']
        contrasena = request.POST['contrasena']
        contrasena2 = request.POST['contrasena2']
        correoElectronico = request.POST['correoElectronico']
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        fechaNacimiento = request.POST['fechaNacimiento']
        genero = request.POST['genero']
        direccion = request.POST['direccion']
        barrio = request.POST['barrio']
        telefonoFijo = request.POST['telefonoFijo']
        telefonoCelular = request.POST['telefonoCelular']
        seguridadSocial = request.POST['seguridadSocial']

        #Toma de datos particulares
        nombreAcudiente = request.POST['Acudiente']
        telefonoAcudiente = request.POST['telefonoAcudiente']
        foto = request.FILES['foto']
        #URLfoto = "documentos/%s/%s"%(request.user.username, "cedula")
        cedula = request.FILES['cedula']
        #URLcedula = "documentos/%s/%s"%(request.user.username, "foto")

        #Inicializo datos opcionales
        zona = ""
        comuna = ""
        grupoEtnico = ""
        condicion = ""
        enviarInfoAlCorreo = False

        #Inicializo Datos Opcionales particulares
        desempeno = ""
        lugar = ""

        #Tomo los datos opcionales
        if request.POST['zona']: zona = request.POST['zona']
        if request.POST['comuna']: comuna = request.POST['comuna']
        if request.POST['grupoEtnico']: grupoEtnico = request.POST['grupoEtnico']
        if request.POST['condicion']: condicion = request.POST['condicion']
        if "enviarInfoAlCorreo" in request.POST.keys(): enviarInfoAlCorreo = True

        #tomo datos opcionales particulares
        if request.POST['Labor']: desempeno = request.POST['Labor']
        if request.POST['Lugar']: lugar = request.POST['Lugar']

        #Validaciones
        errorNumeroDocumento = (User.objects.filter(username=numeroDocumento) or  not re.match("^([0-9]{8,20})$",numeroDocumento))
        errorTipoDocumento = (tipoDocumento  not in (parametros["tiposDocumento"]))
        errorContrasena = (request.POST["contrasena"]!=request.POST["contrasena2"])
        errorCorreoElectronico = (User.objects.filter(email=correoElectronico) or not re.match(r"^[A-Za-z0-9\._-]+@[A-Za-z0-9]+\.[a-zA-Z]+$", correoElectronico))
        errorFechaNacimiento = not fechaCorrecta(fechaNacimiento)
        errorGenero = (genero not in (parametros["generos"]))
        errorTelefonos = (not re.match("^([0-9]{7,12})$",telefonoFijo) or not re.match("^([0-9]{7,12})$",telefonoCelular) or not re.match("^([0-9]{7,12})$",telefonoAcudiente))

        if (errorContrasena or errorNumeroDocumento or errorTipoDocumento or errorCorreoElectronico or errorFechaNacimiento or errorGenero or errorTelefonos):
            return render_to_response('Generales/registroEstudianteMayor.html', locals(), context_instance = RequestContext(request))

        #Guardar usuario
        usuario = User.objects.create_user(id=User.objects.all().count() + 1, username=numeroDocumento, email=correoElectronico, password=contrasena)
        usuario.first_name = nombres
        usuario.last_name = apellidos
        
        #Guardo estudiante
        estudiante = Estudiante(user = usuario, tipoDocumento = tipoDocumento, fechaNacimiento = fechaNacimiento, genero = genero, direccion = direccion, barrio = barrio, zona = zona, comuna = comuna, 
            telefonoFijo = telefonoFijo, telefonoCelular = telefonoCelular, grupoEtnico = grupoEtnico, condicion = condicion, seguridadSocial = seguridadSocial, enviarInfoAlCorreo = enviarInfoAlCorreo)

        #Guardo datos particulares del Mayor
        datosMayor = DatosFamiliaMayor(id= User.objects.all().count() + 1, idEstudiante= estudiante, nombreContacto= nombreAcudiente, telefonoContacto= telefonoAcudiente,
            desempeno= desempeno, lugar= lugar, cedula= cedula, foto= foto)

        #Guardar Roles
        rol= Roles(id=User.objects.all().count() + 1, IDuser= usuario, Estudiante=False, Profesor=False, Administrador=False)

        #Guardar solicitud
        solicitud = Solicitudes(id=User.objects.all().count() + 1, IDestudiante= estudiante, estado= "Pendiente", Correcciones= False)

        usuario.save()
        rol.save()
        estudiante.save()  
        datosMayor.save()
        solicitud.save()

        return inicioControl(request, registerSuccess=True)

class RegistroEstudianteMenor(base.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            generos = parametros['generos']
            tiposDocumento = parametros['tiposDocumento']
            zonas = parametros['zonas']
            jornadas = parametros['jornada']
            return render_to_response('Generales/registroEstudianteMenor.html', locals(), context_instance = RequestContext(request))
        else:
            conectado = True
            nombreUsuario = request.user.username
            return render_to_response('Generales/registroEstudiante.html', locals(), context_instance = RequestContext(request))

    def post(self, request, *args, **kwargs):
        generos = parametros['generos']
        tiposDocumento = parametros['tiposDocumento']
        zonas = parametros['zonas']
        jornadas = parametros['jornada']

        #Toma de datos
        numeroDocumento = request.POST['numeroDocumento']
        tipoDocumento = request.POST['tipoDocumento']
        contrasena = request.POST['contrasena']
        contrasena2 = request.POST['contrasena2']
        correoElectronico = request.POST['correoElectronico']
        nombres = request.POST['nombres']
        apellidos = request.POST['apellidos']
        fechaNacimiento = request.POST['fechaNacimiento']
        genero = request.POST['genero']
        direccion = request.POST['direccion']
        barrio = request.POST['barrio']
        telefonoFijo = request.POST['telefonoFijo']
        telefonoCelular = request.POST['telefonoCelular']
        seguridadSocial = request.POST['seguridadSocial']

        #Toma de datos particulares
        nombreResponsable = request.POST['nombreAcudiente']
        cedulaAcudiente = request.POST['cedulaAcudiente']
        documento = request.FILES['documento']
        foto = request.FILES['foto']
        cedula = request.FILES['cedula']

        #Inicializo datos opcionales
        zona = ""
        comuna = ""
        grupoEtnico = ""
        condicion = ""
        enviarInfoAlCorreo = False

        #Inicializo datos opcionales Particulares
        nombrePadre = ""
        nombreMadre = ""
        telefonoPadre = ""
        telefonoMadre = ""
        Colegio = ""
        jornada = ""
        Grado = ""

         #tomo datos opcionales particulares
        if request.POST['nombrePadre']: nombrePadre = request.POST['nombrePadre']
        if request.POST['nombreMadre']: nombreMadre = request.POST['nombreMadre']
        if request.POST['telefonoPadre']: telefonoPadre = request.POST['telefonoPadre']
        if request.POST['telefonoMadre']: telefonoMadre = request.POST['telefonoMadre']
        if request.POST['Colegio']: Colegio = request.POST['Colegio']
        if request.POST['Jornada']: jornada = request.POST['Jornada']
        if request.POST['Grado']: Grado = request.POST['Grado']

        #Tomo los datos opcionales
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
        errorTelefonos = (not re.match("^([0-9]{7,12})$",telefonoFijo) or not re.match("^([0-9]{7,12})$",telefonoCelular) or not re.match("^([0-9]{7,12})$",telefonoPadre) or not re.match("^([0-9]{7,12})$",telefonoMadre))

        if (errorContrasena or errorNumeroDocumento or errorTipoDocumento or errorCorreoElectronico or errorFechaNacimiento or errorGenero or errorTelefonos):
            return render_to_response('Generales/registroEstudianteMenor.html', locals(), context_instance = RequestContext(request))

        #Guardar usuario
        usuario = User.objects.create_user(id=User.objects.all().count() + 1, username=numeroDocumento, email=correoElectronico, password=contrasena)
        usuario.first_name = nombres
        usuario.last_name = apellidos
        
        #Guardo estudiante
        estudiante = Estudiante(user = usuario, tipoDocumento = tipoDocumento, fechaNacimiento = fechaNacimiento, genero = genero, direccion = direccion, barrio = barrio, zona = zona, comuna = comuna, 
            telefonoFijo = telefonoFijo, telefonoCelular = telefonoCelular, grupoEtnico = grupoEtnico, condicion = condicion, seguridadSocial = seguridadSocial, enviarInfoAlCorreo = enviarInfoAlCorreo)

        #Guardo datos Particulares del menor
        datosMenor = DatosFamiliaMenor(idEstudiante = estudiante, nombrePadre= nombrePadre, nombreMadre= nombreMadre, telefonoPadre= telefonoPadre, telefonoMadre= telefonoMadre, institucionEducativa= Colegio, 
            grupo= Grado, jornada=jornada, nombreAcudiente=nombreResponsable, cedulaAcudiente= cedulaAcudiente, documento= documento, foto= foto, cedula= cedula)
        
        #Guardar solicitud
        solicitud = Solicitudes(id=User.objects.all().count() + 1, IDestudiante= estudiante, estado= "Pendiente", Correcciones= False)

        usuario.save()
        estudiante.save()
        datosMenor.save()
        solicitud.save()


        return inicioControl(request, registerSuccess=True)


class RegistroEstudiante2(base.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render_to_response('Generales/registroEstudiante.html', locals(), context_instance = RequestContext(request))
        else:
            conectado = True
            nombreUsuario = request.user.username
            return render_to_response('Generales/registroEstudiante.html', locals(), context_instance = RequestContext(request))

    def post(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            generos = parametros['generos']
            tiposDocumento = parametros['tiposDocumento']
            zonas = parametros['zonas']
            jornadas = parametros['jornada']
            edad = request.POST["codigo_edad"]
            if edad == "mayor":
                return render_to_response('Generales/registroEstudianteMayor.html', locals(), context_instance = RequestContext(request))
            else:
                return render_to_response('Generales/registroEstudianteMenor.html', locals(), context_instance = RequestContext(request))
        else:
            conectado = True
            nombreUsuario = request.user.username
            return render_to_response('Generales/registroEstudiante.html', locals(), context_instance = RequestContext(request))

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


def Hora_Libre(curso_ini, curso_fin, hora_ini, hora_fin):
    if hora_ini > curso_ini and hora_ini < curso_fin:
        libre = False
    elif hora_ini > curso_ini and hora_fin < curso_fin:
        libre = False
    elif hora_ini < curso_ini and hora_fin > curso_ini:
        libre = False
    elif hora_ini < curso_ini and hora_fin > curso_fin:
        libre = False
    elif hora_ini == curso_ini and hora_fin == curso_fin:
        libre = False
    else:
        libre = True

    return libre

def Edad(fechaNacimiento):
    Fecha_Actual = datetime.now()
    Fecha_Dia = Fecha_Actual.days
    Fecha_Mes = Fecha_Actual.month
    Fecha_Ano = Fecha_Actual.year
    Edad = fechaNacimiento.year - Fecha_Ano
    if fechaNacimiento.month == Fecha_Mes:
        if fechaNacimiento.days >= Fecha_Dia:
            Edad = Edad + 1
    elif fechaNacimiento.month > Fecha_Mes:
        Edad = Edad + 1

    return Edad


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