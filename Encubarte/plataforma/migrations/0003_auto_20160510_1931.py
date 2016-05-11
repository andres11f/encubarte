# -*- coding: utf-8 -*-
# Generated by Django 1.9 on 2016-05-11 00:31
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('plataforma', '0002_auto_20160510_1311'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profesorcurso',
            name='idCurso',
        ),
        migrations.RemoveField(
            model_name='profesorcurso',
            name='idProfesor',
        ),
        migrations.AddField(
            model_name='curso',
            name='idProfesor',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='plataforma.Profesor'),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='ProfesorCurso',
        ),
    ]
