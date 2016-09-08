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
from Encubarte.backend.apps.generales.models import Horario, Curso, Grupo
from Encubarte.backend.apps.generales.parametros import parametros
from Encubarte.backend.apps.generales.forms import UserForm
from Encubarte.backend.apps.estudiante.forms import EstudianteForm, DatosMayorForm, DatosMenorForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.template.defaulttags import register
import re, math, os, ast
import pdb
from datetime import timedelta, datetime, date
from django import template
import itertools

class LogEstudiante(base.View):
    def get(self, request, *args, **kwargs):
        return render_to_response('Estudiante/LogEstudiante.html', locals(), context_instance = RequestContext(request))

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
            return render_to_response('Estudiante/MatricularCurso.html',  locals(), context_instance = RequestContext(request)) 
        else:
            MostrarHorario = False
            cursos = Curso.objects.filter(esCerrado=False)
            horarios = Horario.objects.all()
            #comentario
            return render_to_response('Estudiante/MatricularCurso.html',  locals(), context_instance = RequestContext(request)) 

    def post(self, request, *args, **kwargs):
        cursos = Curso.objects.filter(esCerrado=False)
        horarios = Horario.objects.all()
        cursoMatricular = request.POST['idCurso'] #nombre a matricular en string
        grupoCurso = request.POST['idGrupo'] #grupo del curso a matricular
        cursoID = Curso.objects.get(nombre=cursoMatricular, numeroGrupo=grupoCurso) #IdCurso a partir del nombre del curso y numero de grupo
        horarioNuevo = Horario.objects.filter(idCurso = cursoID)
        HorarioEmpty = False

        try:
            user = User.objects.get(username = request.user.username)
            estudiante = Estudiante.objects.get(user = user)
            gruposEstudiante = Grupo.objects.filter(idEstudiante = estudiante)
            horariosGrupo = Horario.objects.filter(idCurso__in=gruposEstudiante.values('idCurso'))
        except horariosGrupo.DoesNotExist:
            HorarioEmpty = True

        CursoDiferente = False
        HorarioLibre = False

        if not HorarioEmpty:
            for horario in horarioNuevo:
                hora_ini = horario.horaInicio
                hora_final = horario.horaFin
                for h in horariosGrupo:
                    print(horariosGrupo)
                    hora_IC = h.horaInicio # hora inicio cursos matriculados
                    hora_FC = h.horaFin #hora fin cursos matriculados
                    if h.idCurso != horario.idCurso:
                        CursoDiferente = True
                        Libre = Hora_Libre(hora_IC, hora_FC, hora_ini, hora_final)
                        print(h.idCurso)
                        print(horario.idCurso)
                        print(h.dia)
                        print(horario.dia)
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
            CursoDiferente = True
            HorarioLibre = True

        if CursoDiferente and HorarioLibre:
            MatriculaSuccess = True
            grupo = Grupo(idEstudiante= estudiante , idCurso= cursoID)
            grupo.save()
            return render_to_response('Estudiante/MatricularCurso.html',  locals(), context_instance = RequestContext(request))
        elif not CursoDiferente:
                CursandoCurso = True
                return render_to_response('Estudiante/MatricularCurso.html',  locals(), context_instance = RequestContext(request))
        else:
            HoraOcupada = True
            return render_to_response('Estudiante/MatricularCurso.html',  locals(), context_instance = RequestContext(request))

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
        return render_to_response('Estudiante/VerHorario.html', locals(), context_instance = RequestContext(request))

class ModificarInfoEstudiante(base.View):
    def get(self, request, *args, **kwargs):
        user = User.objects.get(username = request.user.username)
        estudiante = Estudiante.objects.get(user = user)
        Tipo = estudiante.tipoDocumento
        generos = parametros["generos"]
        tiposDocumento = parametros["tiposDocumento"]
        zonas = parametros['zonas']
        if Tipo == "Cedula":
            DatosMayor = DatosFamiliaMayor.objects.get(idEstudiante = estudiante)
            if request.user.is_authenticated():
                form = EstudianteForm(instance=estudiante)
                formUser = UserForm(instance=user)
                formExtra = DatosMayorForm(instance=DatosMayor)
                return render_to_response('Estudiante/ModificarInfo.html', locals(), context_instance = RequestContext(request))
        else:
            DatosMenor = DatosFamiliaMenor.objects.get(idEstudiante = estudiante)
            if request.user.is_authenticated():
                form = EstudianteForm(instance=estudiante)
                formUser = UserForm(instance=user)
                formExtra = DatosMenorForm(instance=DatosMenor)
                return render_to_response('Estudiante/ModificarInfo.html', locals(), context_instance = RequestContext(request))

        


    def post(self, request, *args, **kwargs):
        generos = parametros["generos"]
        tiposDocumento = parametros["tiposDocumento"]
        zonas = parametros['zonas']
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

        Tipo = estudiante.tipoDocumento
        if Tipo == "Cedula":
            DatosMayor = DatosFamiliaMayor.objects.get(idEstudiante = estudiante)
            DatosMayor.nombreContacto = request.POST['nombreContacto']
            DatosMayor.telefonoContacto = request.POST['telefonoContacto']
            DatosMayor.desempeno = request.POST['desempeno']
            DatosMayor.lugar = request.POST['lugar']
            DatosMayor.cedula = request.POST['cedula']
            DatosMayor.foto =request.POST['foto']
            errorTelefonosFamilia = not re.match("^([0-9]{7,12})$",DatosMayor.telefonoContacto)

            if (errorTipoDocumento or errorFechaNacimiento or errorGenero or errorTelefonos or errorTelefonosFamilia):
                return render_to_response('Estudiante/LogEstudiante.html', locals(), context_instance = RequestContext(request))

            #Guardar usuario
            user.save()
            estudiante.save()
            DatosMayor.save()

            operationSuccess = True
            return render_to_response('Estudiante/LogEstudiante.html', locals(), context_instance = RequestContext(request))

        else:
            DatosMenor = DatosFamiliaMenor.objects.get(idEstudiante = estudiante)
            DatosMenor.nombrePadre = request.POST['nombrePadre']
            DatosMenor.nombreMadre = request.POST['nombreMadre']
            DatosMenor.telefonoPadre = request.POST['telefonoPadre']
            DatosMenor.telefonoMadre = request.POST['telefonoMadre']
            DatosMenor.institucionEducativa = request.POST['institucionEducativa']
            DatosMenor.grupo = request.POST['grupo']
            DatosMenor.jornada = request.POST['jornada']
            DatosMenor.nombreAcudiente = request.POST['nombreAcudiente']
            DatosMenor.cedulaAcudiente = request.POST['cedulaAcudiente']
            DatosMenor.documento = request.POST['documento']
            DatosMenor.cedula = request.POST['cedula']
            DatosMenor.foto = request.POST['foto']
            errorTelefonosFamilia = (not re.match("^([0-9]{7,12})$",DatosMenor.telefonoPadre) or not re.match("^([0-9]{7,12})$",DatosMenor.telefonoMadre))

            if (errorTipoDocumento or errorFechaNacimiento or errorGenero or errorTelefonos or errorTelefonosFamilia):
                return render_to_response('Estudiante/LogEstudiante.html', locals(), context_instance = RequestContext(request))
            
            #Guardar usuario
            user.save()
            estudiante.save()
            DatosMenor.save()

            operationSuccess = True
            return render_to_response('Estudiante/LogEstudiante.html', locals(), context_instance = RequestContext(request))

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