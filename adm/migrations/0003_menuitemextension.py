# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations


class Migration(migrations.Migration):

    dependencies = [
        ('treemenus', '__first__'),
        ('adm', '0002_auto_20141202_0029'),
    ]

    operations = [
        migrations.CreateModel(
            name='MenuItemExtension',
            fields=[
                ('id', models.AutoField(verbose_name='ID', serialize=False, auto_created=True, primary_key=True)),
                ('menu_type', models.CharField(max_length=255, choices=[(b'page', b'Pages'), (b'category', b'Categories'), (b'link', b'Links')])),
                ('extra', models.TextField(null=True)),
                ('menu_item', models.OneToOneField(related_name='extension', to='treemenus.MenuItem')),
            ],
            options={
            },
            bases=(models.Model,),
        ),
    ]
