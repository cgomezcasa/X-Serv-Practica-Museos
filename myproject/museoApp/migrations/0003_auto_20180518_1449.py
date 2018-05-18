# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museoApp', '0002_auto_20180517_1242'),
    ]

    operations = [
        migrations.AlterField(
            model_name='comentario',
            name='publicacion',
            field=models.DateTimeField(auto_now=True),
        ),
    ]
