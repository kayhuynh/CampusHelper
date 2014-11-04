# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CampusHelperApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='summary',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='user',
            name='cookieID',
            field=models.BigIntegerField(unique=True),
            preserve_default=True,
        ),
    ]
