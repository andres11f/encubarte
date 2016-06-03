# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-06-03 01:07
from __future__ import unicode_literals

import Encubarte.plataforma.models
from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0007_alter_validators_add_error_messages'),
    ]

    operations = [
        migrations.CreateModel(
            name='Curso',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombre', models.CharField(max_length=50)),
                ('nroGrupo', models.IntegerField()),
                ('esCerrado', models.BooleanField()),
            ],
        ),
        migrations.CreateModel(
            name='DatosFamiliaMayor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombreContacto', models.CharField(max_length=50)),
                ('telefonoContacto', models.IntegerField()),
                ('desempeño', models.CharField(max_length=50)),
                ('lugar', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Datos Familias Mayor',
            },
        ),
        migrations.CreateModel(
            name='DatosFamiliaMenor',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('nombrePadre', models.CharField(max_length=50)),
                ('nombreMadre', models.CharField(max_length=50)),
                ('telefonoPadre', models.IntegerField()),
                ('telefonoMadre', models.IntegerField()),
                ('institucionEducativa', models.CharField(max_length=50)),
                ('grupo', models.CharField(max_length=50)),
                ('jornada', models.CharField(max_length=50)),
                ('nombreAcudiente', models.CharField(max_length=50)),
                ('cedulaAcudiente', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Datos Familias Menor',
            },
        ),
        migrations.CreateModel(
            name='Estudiante',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('tipoDocumento', models.CharField(max_length=10)),
                ('fechaNacimiento', models.DateField()),
                ('genero', models.CharField(max_length=1)),
                ('direccion', models.CharField(max_length=50)),
                ('barrio', models.CharField(max_length=50)),
                ('zona', models.CharField(max_length=50)),
                ('comuna', models.CharField(max_length=50)),
                ('telefonoFijo', models.IntegerField()),
                ('telefonoCelular', models.IntegerField()),
                ('grupoEtnico', models.CharField(max_length=50)),
                ('condicion', models.CharField(max_length=50)),
                ('seguridadSocial', models.CharField(max_length=50)),
                ('enviarInfoAlCorreo', models.BooleanField()),
                ('documento', models.FileField(upload_to=Encubarte.plataforma.models.Estudiante.url)),
            ],
        ),
        migrations.CreateModel(
            name='Grupo',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('idCurso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.Curso')),
                ('idEstudiante', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.Estudiante')),
            ],
        ),
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('dia', models.CharField(max_length=20)),
                ('horaInicio', models.TimeField()),
                ('horaFin', models.TimeField()),
                ('idCurso', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.Curso')),
            ],
        ),
        migrations.CreateModel(
            name='Profesor',
            fields=[
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to=settings.AUTH_USER_MODEL)),
                ('fechaNacimiento', models.DateField()),
                ('tipoDocumento', models.CharField(max_length=10)),
                ('genero', models.CharField(max_length=50)),
            ],
            options={
                'verbose_name_plural': 'Profesores',
            },
        ),
        migrations.AddField(
            model_name='datosfamiliamenor',
            name='idEstudiante',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='plataforma.Estudiante'),
        ),
        migrations.AddField(
            model_name='datosfamiliamayor',
            name='idEstudiante',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='plataforma.Estudiante'),
        ),
        migrations.AddField(
            model_name='curso',
            name='idProfesor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='plataforma.Profesor'),
        ),
    ]
