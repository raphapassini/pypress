import json
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import TemplateView
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse, reverse_lazy
from django.views.generic.edit import (CreateView, UpdateView, FormView)
from django.views.generic.list import ListView
from treemenus.models import Menu, MenuItem
from rest_framework import viewsets
from core.models import Category, Entry, Page

from .serializers import MenuSerializer, MenuItemSerializer
from .models import Config, MenuItemExtension
from .forms import (GeneralConfig, WriteConfig, ReadConfig, CommentConfig,
                    CreateMenuForm, MenuSelectForm, PageSelectForm,
                    CategorySelectForm, ExternalLinkForm)


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
        context['page_form'] = self.get_page_form()
        context['category_form'] = self.get_category_form()
        context['external_link_form'] = self.get_external_link_form()
        context['menu_item_options'] = self.get_menuitem_options()
        return context

    def get_menu_select_form(self):
        return MenuSelectForm

    def get_page_form(self):
        return PageSelectForm

    def get_category_form(self):
        return CategorySelectForm

    def get_external_link_form(self):
        return ExternalLinkForm

    def get_menuitem_options(self):
        return MenuItemExtension.MENU_TYPE_OPTIONS


class MenuViewSet(viewsets.ModelViewSet):
    """
    A viewset for viewing and editing user instances.
    """
    serializer_class = MenuSerializer
    queryset = Menu.objects.all()


def load_template(request, tpl=None):
    tpl = '.'.join([tpl, 'mst'])
    full_tpl_path = '/'.join(['adm', 'js_templates', tpl])
    return render(request, full_tpl_path)


def pypress_javascript(request):
    tpl = 'adm/includes/_pypress_javascript.js'
    d = {
        'template_url': reverse(
            'adm:load-tpl', kwargs={'tpl': '__placeholder__'})
    }
    return render(request, tpl, {'data': json.dumps(d)},
                  content_type="text/javascript")
