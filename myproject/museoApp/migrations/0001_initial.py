# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Comentario',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('comentario', models.TextField()),
                ('publicacion', models.DateTimeField()),
            ],
        ),
        migrations.CreateModel(
            name='Configuracion',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('fuente', models.CharField(max_length=32)),
                ('color', models.CharField(max_length=32)),
                ('titulo', models.CharField(max_length=128)),
                ('usuario', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Content_User',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('usuario', models.CharField(max_length=32)),
            ],
        ),
        migrations.CreateModel(
            name='Museo',
            fields=[
                ('id', models.AutoField(serialize=False, primary_key=True, auto_created=True, verbose_name='ID')),
                ('idMuseo', models.IntegerField()),
                ('nombre', models.CharField(max_length=128)),
                ('descripcion', models.TextField()),
                ('horario', models.TextField()),
                ('transporte', models.TextField()),
                ('accesibilidad', models.BinaryField()),
                ('url', models.URLField()),
                ('distrito', models.CharField(max_length=32)),
                ('email', models.EmailField(max_length=64)),
            ],
        ),
        migrations.AddField(
            model_name='content_user',
            name='museo',
            field=models.ForeignKey(to='museoApp.Museo'),
        ),
        migrations.AddField(
            model_name='comentario',
            name='museo',
            field=models.ForeignKey(to='museoApp.Museo'),
        ),
    ]
