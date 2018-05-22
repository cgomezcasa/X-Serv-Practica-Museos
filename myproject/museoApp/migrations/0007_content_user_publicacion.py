# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('museoApp', '0006_remove_content_user_publicacion'),
    ]

    operations = [
        migrations.AddField(
            model_name='content_user',
            name='publicacion',
            field=models.DateTimeField(default='2000-01-01 00:00', auto_now=True),
            preserve_default=False,
        ),
    ]
