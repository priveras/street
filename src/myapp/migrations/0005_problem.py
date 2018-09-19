# -*- coding: utf-8 -*-
# Generated by Django 1.10.8 on 2018-09-09 01:16
from __future__ import unicode_literals

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('myapp', '0004_assumption'),
    ]

    operations = [
        migrations.CreateModel(
            name='Problem',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.TextField(blank=True)),
                ('status', models.CharField(blank=True, choices=[('Validated', 'Validated'), ('In Progress', 'In Progress'), ('Invalidated', 'Invalidated')], max_length=200)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('created_at', models.DateTimeField(auto_now_add=True, db_index=True)),
                ('project', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='myapp.Project')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
