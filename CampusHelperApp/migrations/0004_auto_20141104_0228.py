# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CampusHelperApp', '0003_merge'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='value',
            field=models.PositiveSmallIntegerField(default=0),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.TextField(default=b'other'),
            preserve_default=True,
        ),
    ]
