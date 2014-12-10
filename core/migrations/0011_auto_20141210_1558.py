# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models, migrations
import taggit.managers


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0010_entry_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='tags',
            field=taggit.managers.TaggableManager(to='core.TagEntry', through='core.TaggedWhatever', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
        migrations.AlterField(
            model_name='page',
            name='tags',
            field=taggit.managers.TaggableManager(to='core.TagEntry', through='core.TaggedWhatever', blank=True, help_text='A comma-separated list of tags.', verbose_name='Tags'),
            preserve_default=True,
        ),
    ]
