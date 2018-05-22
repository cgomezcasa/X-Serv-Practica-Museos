# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museoApp', '0008_auto_20180522_2042'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='publicacion',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
        migrations.AlterField(
            model_name='content_user',
            name='publicacion',
            field=models.DateTimeField(null=True, auto_now=True),
        ),
    ]
