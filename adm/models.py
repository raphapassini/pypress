import json
import ast
from django.db import models
from treemenus.models import MenuItem
from core.models import Page, Category


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
        ('page', 'Page'),
        ('category', 'Category'),
        ('link', 'Link')
    ]
    menu_item = models.OneToOneField(MenuItem, related_name="extension")
    menu_type = models.CharField(max_length=255, choices=MENU_TYPE_OPTIONS)
    extra = models.TextField(null=True)

    def extra_to_dict(self):
        try:
            data = json.loads(self.extra)
        except Exception as e:
            data = {'exception': e.__str__()}
        return data

    def get_related_display(self):
        obj = self.get_related_obj()
        if self.menu_type == 'page':
            field = 'title'
        elif self.menu_type == 'category':
            field = 'name'
        elif self.menu_type == 'link':
            return self.menu_item.url

        if hasattr(obj, field):
            return getattr(obj, field)
        else:
            return ''

    def get_related_obj(self):
        extra = self.extra_to_dict()
        pk = extra.get('pk', False)
        if self.menu_type == 'page':
            obj = Page
        elif self.menu_type == 'category':
            obj = Category
        elif self.menu_type == 'link':
            return None

        try:
            return obj.objects.get(pk=pk)
        except obj.DoesNotExist:
            return None
