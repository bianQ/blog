# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-29 03:08
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0007_secondcomment_commented'),
    ]

    operations = [
        migrations.AlterField(
            model_name='secondcomment',
            name='commented',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='blog.SecondComment', verbose_name='被评论'),
        ),
    ]