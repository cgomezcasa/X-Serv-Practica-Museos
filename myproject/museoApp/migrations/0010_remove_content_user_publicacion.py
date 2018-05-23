# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museoApp', '0009_auto_20180522_2046'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content_user',
            name='publicacion',
        ),
    ]
