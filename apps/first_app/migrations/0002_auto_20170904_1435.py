# -*- coding: utf-8 -*-
# Generated by Django 1.11.3 on 2017-09-04 19:35
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('first_app', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='friend',
            old_name='second_friend',
            new_name='other_friend',
        ),
    ]
