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
from Encubarte.backend.apps.generales.models import Horario, Curso, Grupo
from Encubarte.backend.apps.generales.parametros import parametros
from Encubarte.backend.apps.generales.forms import UserForm
from Encubarte.backend.apps.profesor.forms import ProfesorForm
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.template.defaulttags import register
import re, math, os, ast
import pdb
from datetime import timedelta, datetime, date
from django import template
import itertools

from django.core import serializers

class LogProfesor(base.View):
    def get(self, request, *args, **kwargs):
        return render_to_response('Profesor/LogProfesor.html', locals(), context_instance = RequestContext(request))

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
            return render_to_response('Generales/registroEstudiante.html', locals(), context_instance = RequestContext(request))
    
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
        cursoMatricular = curso_grupo[0] #nombre a matricular en string
        grupoCurso = curso_grupo[1] #grupo del curso a matricular
        cursoID = Curso.objects.get(nombre=cursoMatricular, numeroGrupo=grupoCurso) #IdCurso a partir del nombre del curso
        horarioNuevo = Horario.objects.filter(idCurso = cursoID)
        try:
            estudianteaMatricular = User.objects.get(username=request.POST['numeroDocumento'])
        except:
            errorEstudiante = True
            return render_to_response('Profesor/MatricularEstudiante.html',  locals(), context_instance = RequestContext(request))


        try:
            estudiante = Estudiante.objects.get(user = estudianteaMatricular)
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
            CursoDiferente = True
            HorarioLibre = True


        if CursoDiferente and HorarioLibre:
            MatriculaSuccess = True
            grupo = Grupo(idEstudiante= estudiante , idCurso= cursoID)
            grupo.save()
            return render_to_response('Profesor/MatricularEstudiante.html',  locals(), context_instance = RequestContext(request))
        elif not CursoDiferente:
                CursandoCurso = True
                return render_to_response('Profesor/MatricularEstudiante.html',  locals(), context_instance = RequestContext(request))
        else:
            HoraOcupada = True
            return render_to_response('Profesor/MatricularEstudiante.html',  locals(), context_instance = RequestContext(request))

class listaCursosControl(base.View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_staff:
            idProfesor = Profesor.objects.get(user = request.user)
            cursos = Curso.objects.filter(idProfesor = idProfesor)
            print("--------------------CURSOS----------------")
            print(cursos)
            return render_to_response('Profesor/listaCursos.html',locals(), context_instance = RequestContext(request))
        else:
            return HttpResponseRedirect('/404')

    def post(self, request, *args, **kwargs):
        if request.user.is_authenticated() and request.user.is_staff:
            idProfesor = Profesor.objects.get(user = request.user)
            cursos = Curso.objects.filter(idProfesor = idProfesor)
            idCurso = request.POST["id"]
            curso = Curso.objects.get(id=idCurso)
            grupo = Grupo.objects.filter(idCurso=curso)
            visualizarEstudiantes = True
            return render_to_response('Profesor/listaCursos.html',locals(), context_instance = RequestContext(request))

        else:
            return HttpResponseRedirect('/404')

#__________________________________________________________________________________________________________________________________________________#
#___________________________________________________________OTRAS FUNCIONES________________________________________________________________________#
#__________________________________________________________________________________________________________________________________________________#

@register.filter
def get_item(dictionary, key):
    return dictionary.get((key.split(",")[0], key.split(",")[1]))


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