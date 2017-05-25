# -*- coding: utf-8 -*-
# Generated by Django 1.10.4 on 2017-01-06 13:12
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Member',
            fields=[
                ('username', models.CharField(max_length=16, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=16)),
                ('following', models.ManyToManyField(to='mainapp.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Message',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('pm', models.BooleanField(default=True)),
                ('time', models.DateTimeField()),
                ('text', models.CharField(max_length=4096)),
                ('recip', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_recip', to='mainapp.Member')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='message_user', to='mainapp.Member')),
            ],
        ),
        migrations.CreateModel(
            name='Profile',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('text', models.CharField(max_length=4096)),
            ],
        ),
        migrations.AddField(
            model_name='member',
            name='profile',
            field=models.OneToOneField(null=True, on_delete=django.db.models.deletion.CASCADE, to='mainapp.Profile'),
        ),
    ]