# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museoApp', '0005_content_user_publicacion'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='content_user',
            name='publicacion',
        ),
    ]
