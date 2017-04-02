# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('answer', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='Candidates',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
            ],
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', models.AutoField(verbose_name='ID', primary_key=True, serialize=False, auto_created=True)),
                ('description', models.CharField(max_length=500)),
            ],
        ),
        migrations.AddField(
            model_name='answers',
            name='candidate',
            field=models.ForeignKey(to='aval.Candidates'),
        ),
        migrations.AddField(
            model_name='answers',
            name='question',
            field=models.ForeignKey(to='aval.Questions'),
        ),
    ]
