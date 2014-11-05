# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CampusHelperApp', '0004_remove_task_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='category',
            field=models.TextField(default='default'),
            preserve_default=False,
        ),
    ]
