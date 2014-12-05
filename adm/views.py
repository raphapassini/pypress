import json
from django.http import HttpResponseRedirect
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse_lazy
from django.views.generic.edit import (CreateView, UpdateView, FormView)
from django.views.generic.list import ListView
from django.forms.models import formset_factory

from core.models import Category, Entry, Page

from .models import Config
from .forms import (GeneralConfig, WriteConfig, ReadConfig, CommentConfig,
                    CreateMenuForm, MenuSelectForm, MenuItemForm)


class LoginRequiredMixin(object):

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)


class Index(LoginRequiredMixin, TemplateView):
    template_name = 'adm/index.html'


class CategoryListView(LoginRequiredMixin, ListView):
    queryset = Category.objects.all()
    paginate_by = 10


class CategoryCreateView(LoginRequiredMixin, CreateView):
    model = Category
    success_url = reverse_lazy('adm:category-list')


class CategoryEditView(LoginRequiredMixin, UpdateView):
    model = Category
    success_url = reverse_lazy('adm:category-list')


class EntryListView(LoginRequiredMixin, ListView):
    queryset = Entry.objects.all()
    paginate_by = 10


class EntryCreateView(LoginRequiredMixin, CreateView):
    model = Entry
    success_url = reverse_lazy('adm:entry-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class EntryEditView(LoginRequiredMixin, UpdateView):
    model = Entry
    success_url = reverse_lazy('adm:entry-list')


class PageListView(LoginRequiredMixin, ListView):
    queryset = Page.objects.all()
    paginate_by = 10


class PageCreateView(LoginRequiredMixin, CreateView):
    model = Page
    success_url = reverse_lazy('adm:page-list')

    def form_valid(self, form):
        self.object = form.save(commit=False)
        self.object.author = self.request.user
        self.object.save()
        return HttpResponseRedirect(self.get_success_url())


class PageEditView(LoginRequiredMixin, UpdateView):
    model = Page
    success_url = reverse_lazy('adm:page-list')


class ConfigMixin(LoginRequiredMixin):

    def get_initial(self):
        form = self.get_form_class()()
        data = {}
        for k in form.fields:
            try:
                c = Config.objects.get(name=k)
            except Config.DoesNotExist:
                c = None

            if c is not None:
                data[k] = c.clean_value
        return data

    def form_valid(self, form):
        for k in form.fields:
            try:
                c = Config.objects.get(name=k)
            except Config.DoesNotExist:
                c = Config()
                c.name = k

            extra = self.get_extra(form, form.fields[k])
            c.extra = json.dumps(extra)
            c.value = form.cleaned_data[k]
            c.save()
        return super(ConfigMixin, self).form_valid(form)

    def get_extra(self, form, field):
        data = {
            'klass': field.__class__.__name__
        }
        return data


class GeneralConfigView(ConfigMixin, FormView):
    form_class = GeneralConfig
    template_name = 'adm/config_general.html'
    success_url = reverse_lazy('adm:config-general')


class WriteConfigView(ConfigMixin, FormView):
    form_class = WriteConfig
    template_name = 'adm/config_write.html'
    success_url = reverse_lazy('adm:config-write')


class ReadConfigView(ConfigMixin, FormView):
    form_class = ReadConfig
    template_name = 'adm/config_read.html'
    success_url = reverse_lazy('adm:config-read')


class CommentConfigView(ConfigMixin, FormView):
    form_class = CommentConfig
    template_name = 'adm/config_comment.html'
    success_url = reverse_lazy('adm:config-comment')


class MenuEditorView(LoginRequiredMixin, CreateView):
    form_class = CreateMenuForm
    template_name = 'adm/menu_editor.html'
    success_url = reverse_lazy('adm:menu-editor')

    def get_context_data(self, *args, **kwargs):
        context = super(MenuEditorView, self).get_context_data(*args, **kwargs)
        context['select_menu_form'] = self.get_menu_select_form()
        context['menuitem_formset'] = self.get_menuitem_formset()
        return context

    def get_menu_select_form(self):
        return MenuSelectForm()

    def get_menuitem_formset(self):
        return formset_factory(MenuItemForm, extra=2)
