# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Category',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127)),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='CategoryImage',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('image', models.ImageField(upload_to=b'/Users/aamirbhatt/Aamir/aza.shoping/shoping/media/category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('name', models.CharField(max_length=127)),
                ('image', models.ImageField(upload_to=b'/Users/aamirbhatt/Aamir/aza.shoping/shoping/media/product')),
                ('description', models.TextField()),
                ('price', models.IntegerField()),
                ('ideal_for', models.CharField(max_length=127)),
                ('stone', models.CharField(max_length=127)),
                ('material', models.CharField(max_length=127)),
                ('category', models.ForeignKey(to='item.Category')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
        migrations.AddField(
            model_name='category',
            name='images',
            field=models.ManyToManyField(to='item.CategoryImage'),
            preserve_default=True,
        ),
    ]
