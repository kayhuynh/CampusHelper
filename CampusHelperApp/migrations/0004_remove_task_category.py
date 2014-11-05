# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CampusHelperApp', '0003_merge'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='category',
        ),
    ]
