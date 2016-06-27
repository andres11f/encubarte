# -*- coding: utf-8 -*-
from Encubarte.plataforma.parametros import parametros

def nombreOrganizacion(request):
    nombreOrganizacion=parametros["nombreOrganizacion"]
    return {
        'nombreOrganizacion': nombreOrganizacion,
    }