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
            name='publicacion',
            field=models.DateTimeField(default='-', auto_now=True),
            preserve_default=False,
        ),
    ]
