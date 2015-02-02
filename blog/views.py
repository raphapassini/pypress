import os
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from core.models import Entry
from adm.theme_manager import ThemeManager


class ThemeableMixin(object):

    def get_template_names(self):
        tm = ThemeManager()
        theme_path = tm.theme.__path__[0]
        templates = super(ThemeableMixin, self).get_template_names()
        theme_templates = []

        for t in templates:
            new_path = os.path.join(theme_path, t)
            theme_templates.append(new_path)
        return theme_templates


class IndexView(ThemeableMixin, ListView):
    queryset = Entry.objects.all()
    template_name = 'blog/index.html'


class EntryDetailView(ThemeableMixin, DetailView):
    model = Entry
    template_name = 'blog/single_entry.html'
