# -*- coding: utf-8 -*-
# Generated by Django 1.11.1 on 2017-06-28 09:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20170603_1906'),
    ]

    operations = [
        migrations.CreateModel(
            name='SecondComment',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_name', models.CharField(max_length=200, verbose_name='评论者名字')),
                ('user_email', models.EmailField(max_length=200, verbose_name='评论者邮箱')),
                ('body', models.TextField(verbose_name='评论内容')),
                ('created_time', models.DateTimeField(auto_now_add=True, verbose_name='评论发表时间')),
            ],
        ),
        migrations.RemoveField(
            model_name='article',
            name='abstract',
        ),
        migrations.AlterField(
            model_name='blogcomment',
            name='article',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.Article', verbose_name='主评论'),
        ),
        migrations.AddField(
            model_name='secondcomment',
            name='father_comment',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='blog.BlogComment', verbose_name='子评论'),
        ),
    ]