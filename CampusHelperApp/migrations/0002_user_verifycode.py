# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('CampusHelperApp', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='user',
            name='verifyCode',
            field=models.CharField(max_length=5, null=True, blank=True),
            preserve_default=True,
        ),
    ]
