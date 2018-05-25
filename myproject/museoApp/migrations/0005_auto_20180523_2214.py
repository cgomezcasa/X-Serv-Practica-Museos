# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museoApp', '0004_auto_20180518_1505'),
    ]

    operations = [
        migrations.AddField(
            model_name='content_user',
            name='fecha',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='comentario',
            name='publicacion',
            field=models.DateTimeField(null=True, auto_now_add=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='accesibilidad',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='barrio',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='descripcion',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='direccion',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='distrito',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='email',
            field=models.EmailField(max_length=64, null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='horario',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='idMuseo',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='telefono',
            field=models.CharField(max_length=32, null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='transporte',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='museo',
            name='url',
            field=models.URLField(null=True),
        ),
    ]
