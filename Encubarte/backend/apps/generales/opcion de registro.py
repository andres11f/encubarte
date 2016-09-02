class RegistroEstudiante(base.View):
    def get(self, request, *args, **kwargs):
        if not request.user.is_authenticated():
            generos = parametros['generos']
            tiposDocumento = parametros['tiposDocumento']
            zonas = parametros['zonas']
            return render_to_response('Generales/registroEstudiante.html', locals(), context_instance = RequestContext(request))

        else:
            conectado = True
            nombreUsuario = request.user.username
            return render_to_response('Generales/registroEstudiante.html', locals(), context_instance = RequestContext(request))

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

        if (errorContrasena or errorNumeroDocumento or errorTipoDocumento or errorCorreoElectronico or errorFechaNacimiento or errorGenero or errorTelefonos):
            return render_to_response('Generales/registroEstudiante.html', locals(), context_instance = RequestContext(request))

        #Guardar usuario
        print User.objects.all().count()

        usuario = User.objects.create_user(id=User.objects.all().count() + 1, username=numeroDocumento, email=correoElectronico, password=contrasena)
        usuario.first_name = nombres
        usuario.last_name = apellidos
        usuario.save()
        
        #Guardo estudiante
        estudiante = Estudiante(user = usuario, tipoDocumento = tipoDocumento, fechaNacimiento = fechaNacimiento, genero = genero, direccion = direccion, barrio = barrio, zona = zona, comuna = comuna, 
            telefonoFijo = telefonoFijo, telefonoCelular = telefonoCelular, grupoEtnico = grupoEtnico, condicion = condicion, seguridadSocial = seguridadSocial, enviarInfoAlCorreo = enviarInfoAlCorreo)
        estudiante.save()
