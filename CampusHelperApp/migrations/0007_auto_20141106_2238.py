# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('CampusHelperApp', '0006_merge'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='acceptor',
            field=models.ForeignKey(related_name='tasksAccepted', on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='CampusHelperApp.User', null=True),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='category',
            field=models.TextField(),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='task',
            name='value',
            field=models.PositiveSmallIntegerField(),
            preserve_default=True,
        ),
    ]
