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
from django.contrib.auth.models import User
from django.core.paginator import Paginator,EmptyPage,InvalidPage
from django.template.defaulttags import register
from Encubarte.backend.apps.generales.models import Roles
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
            user = User.objects.get(username= nombreUsuario)
            rol = Roles.objects.get(IDuser= user)
            if rol.Estudiante == False and rol.Profesor == False and rol.Administrador == False:
                sinRol = True
                return HttpResponseRedirect("/LogEstudiante/")
            else:
                return render_to_response('Modulos/modulos.html', locals(), context_instance = RequestContext(request))

    def post(self, request, *args, **kwargs):
        codigo= request.POST['codigo_modulo']
    	user = request.POST['codigo_usuario']
        usuario = User.objects.get(username=user)
        rol = Roles.objects.get(IDuser=usuario)
        if codigo == "Estudiante":
            rol.LoginComo = "Estudiante"
            print "AAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA"
            print rol.LoginComo
            rol.save()
            return HttpResponseRedirect("/LogEstudiante/")
    	elif codigo == "Profesor":
            rol.LoginComo = "Profesor"
            rol.save()
            return HttpResponseRedirect("/LogProfesor/")
    	elif codigo == "Administrador":
            rol.LoginComo = "Administrador"
            rol.save()
            return HttpResponseRedirect("/LogAdministrador/")
