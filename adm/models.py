import json
import ast
from django.db import models
from treemenus.models import MenuItem


class Config(models.Model):
    name = models.SlugField()
    value = models.TextField(blank=True)
    extra = models.TextField(blank=True)

    def __unicode__(self):
        return '{}={}'.format(self.name, self.value.__str__())

    @property
    def clean_value(self):
        extra = json.loads(self.extra)
        return self.decode(extra['klass'], self.value)

    def decode(self, klass, value):
        if klass == 'BooleanField':
            if value == 'False':
                return False
            else:
                return True

        if klass == 'MultipleChoiceField':
            value = ast.literal_eval(value)

        return value


class MenuItemExtension(models.Model):
    MENU_TYPE_OPTIONS = [
        ('page', 'Pages'),
        ('category', 'Categories'),
        ('link', 'Links')
    ]
    menu_item = models.OneToOneField(MenuItem, related_name="extension")
    menu_type = models.CharField(max_length=255, choices=MENU_TYPE_OPTIONS)
    extra = models.TextField(null=True)
