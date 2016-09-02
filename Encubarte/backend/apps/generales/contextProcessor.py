# -*- coding: utf-8 -*-
from Encubarte.backend.apps.generales.parametros import parametros

def nombreOrganizacion(request):
    nombreOrganizacion=parametros["nombreOrganizacion"]
    return {
        'nombreOrganizacion': nombreOrganizacion,
    }