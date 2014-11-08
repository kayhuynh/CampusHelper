# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Task',
            fields=[
                ('taskID', models.AutoField(serialize=False, primary_key=True)),
                ('title', models.TextField()),
                ('description', models.TextField()),
                ('timePosted', models.DateTimeField(auto_now_add=True)),
                ('state', models.SmallIntegerField(default=1)),
                ('summary', models.TextField()),
                ('value', models.PositiveSmallIntegerField()),
                ('category', models.TextField()),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.TextField(serialize=False, primary_key=True)),
                ('password', models.TextField()),
                ('email', models.EmailField(max_length=254)),
                ('description', models.TextField()),
                ('cookieID', models.BigIntegerField(unique=True)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='task',
            name='acceptor',
            field=models.ForeignKey(related_name='tasksAccepted', on_delete=django.db.models.deletion.PROTECT, default=None, blank=True, to='CampusHelperApp.User', null=True),
            preserve_default=True,
        ),
        migrations.AddField(
            model_name='task',
            name='creator',
            field=models.ForeignKey(related_name='tasksCreated', to='CampusHelperApp.User'),
            preserve_default=True,
        ),
    ]
