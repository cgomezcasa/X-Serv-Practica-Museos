# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museoApp', '0003_auto_20180518_1449'),
    ]

    operations = [
        migrations.AddField(
            model_name='museo',
            name='barrio',
            field=models.CharField(max_length=32, default='-'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='direccion',
            field=models.CharField(max_length=32, default='-'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='museo',
            name='telefono',
            field=models.CharField(max_length=32, default='-'),
            preserve_default=False,
        ),
    ]
