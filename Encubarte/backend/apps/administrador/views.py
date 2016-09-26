# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib.auth import login, authenticate, logout
from django.views.generic import base
from Encubarte.backend.apps.estudiante.models import Estudiante, DatosFamiliaMayor, DatosFamiliaMenor
from Encubarte.backend.apps.profesor.models import Profesor
from Encubarte.backend.apps.administrador.models import Solicitudes, Correcciones
from Encubarte.backend.apps.generales.models import Horario, Curso, Grupo, Roles
from Encubarte.backend.apps.generales.parametros import parametros
#from Encubarte.backend.apps.generales.forms import UserForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.template.defaulttags import register
import re, math, os, ast
import pdb
from datetime import timedelta, datetime, date
from django import template
import itertools

from django.core import serializers

class LogAdministrador(base.View):
    def get(self, request, *args, **kwargs):
        return render_to_response('Administrador/LogAdministrador.html', locals(), context_instance = RequestContext(request))


class registroProfesorControl(base.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_superuser:
            generos = parametros["generos"]
            tiposDocumento = parametros["tiposDocumento"]
            profesores = Profesor.objects.all()
            if(request.GET.get('eliminarProfesor')):
                user = User.objects.get(username = request.GET.get('username'))
                profesorAEliminar = Profesor.objects.get(user = user)
                profesorAEliminar.delete()
            return render_to_response('Administrador/registroProfesor.html', locals(), context_instance = RequestContext(request))
        else:
            return HttpResponseRedirect('/404')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_superuser:
            generos = parametros["generos"]
            tiposDocumento = parametros["tiposDocumento"]
            profesores = Profesor.objects.all()

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

            #Guardar Rol
            rol = Roles(id= Roles.objects.all().count() + 1, IDuser=usuario, Estudiante=False, Profesor=True, Administrador=False)
            rol.save()

            return inicioControl(request,registerSuccess=True)

        else:
            return HttpResponseRedirect('/404')


class registroCursoControl(base.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_superuser:
            numerosGrupos = parametros["numerosGrupos"]
            edad = parametros["edad"]
            profesores = Profesor.objects.all()
            cursos = Curso.objects.all()
            if(request.GET.get('eliminarCurso')):               
                cursoAEliminar = Curso.objects.get(id = request.GET.get('id'))
                cursoAEliminar.delete()
            return render_to_response('Administrador/registroCurso.html', locals(), context_instance = RequestContext(request))
        else:
            return HttpResponseRedirect('/404')  


    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_superuser:
            umerosGrupos = parametros["numerosGrupos"]
            edad = parametros["edad"]
            profesores = Profesor.objects.all()
            cursos = Curso.objects.all()
            nombreCurso = request.POST["nombreCurso"]
            userProfesor = request.POST["profesor"].split(" - ")
            usernameProfesor = userProfesor[0]
            numeroGrupo = request.POST["numeroGrupo"]
            edadMin = request.POST["edadMin"]
            edadMax = request.POST["edadMax"]

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
            return HttpResponseRedirect('/404')     


class registroHorarioControl(base.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_superuser:
            cursos = Curso.objects.all()
            dias = parametros["diasSemana"]
            horas = parametros["horas"]
            horarios = Horario.objects.all().order_by('idCurso')
            if(request.GET.get('eliminarHorario')):             
                horarioAEliminar = Horario.objects.get(id = request.GET.get('id'))
                horarioAEliminar.delete()
            return render_to_response('Administrador/registroHorario.html', locals(), context_instance = RequestContext(request))
        else:
            return HttpResponseRedirect('/404')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_superuser:
            cursos = Curso.objects.all()
            dias = parametros["diasSemana"]
            horas = parametros["horas"]
            horarios = Horario.objects.all().order_by('idCurso')
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


class VerSolicitudes(base.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_superuser:

            solicitudes = Solicitudes.objects.filter(estado="Pendiente")
            existenSolicitudes = solicitudes.count()

            if existenSolicitudes == 0:
                sinSolicitudes = True
                return render_to_response('Administrador/verSolicitudes.html', locals(), context_instance = RequestContext(request))
            else:
                return render_to_response('Administrador/verSolicitudes.html', locals(), context_instance = RequestContext(request))
        else:
            return HttpResponseRedirect('/404')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_superuser:
            revisarSolicitud = request.POST["revisarSolicitud"]
            if revisarSolicitud == "Revisar":
                Estudianteid = request.POST['id'].split(" - ")
                user = User.objects.get(username = Estudianteid[0])
                estudiante = Estudiante.objects.get(user = user)
                tipo = estudiante.tipoDocumento
                if tipo == "Cedula":
                    DatosMayor = DatosFamiliaMayor.objects.get(idEstudiante = estudiante)
                    return render_to_response('Administrador/revisarSolicitudMayor.html', locals(), context_instance = RequestContext(request))
                else:
                    DatosMenor = DatosFamiliaMenor.objects.get(idEstudiante = estudiante)
                    return render_to_response('Administrador/revisarSolicitudMenor.html', locals(), context_instance = RequestContext(request))

            elif revisarSolicitud == "Aprobar":
                cedula = request.POST["numeroDocumento"]
                user = User.objects.get(username = cedula)
                estudiante = Estudiante.objects.get(user = user)

                rol = Roles.objects.get(user = user)
                rol.Estudiante = True
                
                solicitudEstudiante = Solicitudes.objects.get(IDestudiante=estudiante)
                solicitudEstudiante.estado = "Aprobado"
                solicitudEstudiante.Correcciones = False

                rol.save()
                solicitudEstudiante.save()

                operationSuccess=True

                return render_to_response('Administrador/verSolicitudes.html', locals(), context_instance = RequestContext(request))

            elif revisarSolicitud == "Rechazar":
                numeroDocumento = request.POST["documentoHidden"]
                tipoDocumento = request.POST["tipodocumentoHidden"]
                user = User.objects.get(username = numeroDocumento)
                estudiante = Estudiante.objects.get(user = user)

                if "documentoCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Numero Documento")
                    corregir.save()
                if "tipoCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Numero Documento")
                    corregir.save()
                if "correoCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Correo Electronico")
                    corregir.save()
                if "nombresCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Nombres")
                    corregir.save()
                if "apellidosCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Apellidos")
                    corregir.save()
                if "nacimientoCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Fecha de Nacimiento")
                    corregir.save()
                if "generoCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Genero")
                    corregir.save()
                if "direccionCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Direccion")
                    corregir.save()
                if "barrioCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Barrio")
                    corregir.save()
                if "fijoCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Telefono Fijo")
                    corregir.save()
                if "celularCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Telefono Celular")
                    corregir.save()
                if "seguridadCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Seguridad Social")
                    corregir.save()
                if "zonaCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Zona")
                    corregir.save()
                if "comunaCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Comuna")
                    corregir.save()
                if "grupoCorreccion" in request.POST.keys():
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Grupo Etnico")
                    corregir.save()
                if "condicionCorreccion" in request.POST.keys(): 
                    corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Condicion")
                    corregir.save()                                       

                if tipoDocumento == "Cedula":
                    if "laborCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Labor")
                        corregir.save()
                    if "lugarCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Lugar Laboral")
                        corregir.save()
                    if "contactoCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Nombre Contacto")
                        corregir.save()
                    if "telefonoCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Telefono Contacto")
                        corregir.save()
                    if "cedulaCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Imagen Cedula")
                        corregir.save()
                    if "fotoCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Imagen Foto")
                        corregir.save()                        

                if tipoDocumento == "Tarjeta de Identidad" or tipoDocumento == "Registro Civil":
                    if "padreCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Nombre del Padre")
                        corregir.save()
                    if "telpaoCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Telenofo del Padre")
                        corregir.save()
                    if "madreCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Nombre de la Madre")
                        corregir.save()
                    if "telmaCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Telefono de la Madre")
                        corregir.save()
                    if "colegioCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Colegio")
                        corregir.save()
                    if "gradoCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Grado")
                        corregir.save()
                    if "jornadaCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Jornada")
                        corregir.save()
                    if "acudienteCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Nombre Acudiente")
                        corregir.save()
                    if "cedAcudCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Cedula Acudiente")
                        corregir.save()
                    if "cedulaCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Cedula Acudiente")
                        corregir.save()
                    if "fotoCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Imagen Foto")
                        corregir.save()
                    if "docmenoroCorreccion" in request.POST.keys():
                        corregir = Correcciones(id=Correcciones.objects.all().count() + 1, IDestudiante=estudiante, campo="Imagen Documento del Menor")
                        corregir.save()
                        
                solicitudEstudiante = Solicitudes.objects.get(IDestudiante=estudiante)
                solicitudEstudiante.estado = "Rechazado"
                solicitudEstudiante.Correcciones = True

                solicitudEstudiante.save()

                operationSuccess=True


                return render_to_response('Administrador/verSolicitudes.html', locals(), context_instance = RequestContext(request))

        else:
            return HttpResponseRedirect('/404')


#__________________________________________________________________________________________________________________________________________________#
#___________________________________________________________OTRAS FUNCIONES________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#

@register.filter
def get_item(dictionary, key):
    return dictionary.get((key.split(",")[0], key.split(",")[1]))

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


def __format__(self, format_spec):
    return format(str(self), format_spec)


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