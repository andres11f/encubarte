# -*- coding: utf-8 -*-
# Create your views here.
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.http import HttpResponseRedirect
from django.forms.models import model_to_dict
from django.contrib.auth import login, authenticate, logout
from django.views.generic import base
#from Encubarte.plataforma.models import Estudiante, DatosFamiliaMayor, DatosFamiliaMenor, Profesor, Horario, Curso, Grupo
#from Encubarte.plataforma.parametros import parametros
#from Encubarte.plataforma.forms import EstudianteForm, ProfesorForm, UserForm
from Encubarte.backend.apps.estudiante.models import Estudiante, DatosFamiliaMayor, DatosFamiliaMenor
from Encubarte.backend.apps.profesor.models import Profesor
from Encubarte.backend.apps.generales.models import Horario, Curso, Grupo
from Encubarte.backend.apps.generales.parametros import parametros
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.template.defaulttags import register
import re, math, os, ast
import pdb
from datetime import timedelta, datetime, date
from django import template
import itertools

class EscogerModulo(base.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            return render_to_response ('Generales/inicio.html',locals(), context_instance = RequestContext(request))
        else:
            conectado = True
            nombreUsuario = request.user.username
            return render_to_response('Modulos/modulos.html', locals(), context_instance = RequestContext(request))

    def post(self, request, *args, **kwargs):
        codigo= request.POST['codigo_modulo']
    	user = request.POST['codigo_usuario']
        if codigo == "estudiante":
    		return HttpResponseRedirect("/LogEstudiante/")
    	elif codigo == "profesor":
    		return HttpResponseRedirect("/LogProfesor/")
    	elif codigo == "administrador":
    		return HttpResponseRedirect("/LogAdministrador/")
