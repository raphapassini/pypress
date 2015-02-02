import themes as themes_module
import pkgutil

from .models import Config


class ThemeManager():
    _instance = None

    themes = {}
    theme = None
    active = 'default'

    def __new__(cls, *args, **kwargs):
        if not cls._instance:
            cls._instance = super(ThemeManager, cls).__new__(
                cls, *args, **kwargs)
        return cls._instance

    def __init__(self):
        theme = self._get_active_theme()
        self.activate(theme)

    def get_themes(self, force_reload=False):
        if self.themes and not force_reload:
            return self.themes

        package = themes_module
        for importer, modname, ispkg in pkgutil.iter_modules(package.__path__):
            if ispkg:
                self.themes[modname] = {
                    'modname': modname,
                    'module': self._import_theme(modname, importer)
                }

    def activate(self, name):
        self.get_themes(force_reload=True)
        self.active = name
        self.theme = self.themes.get(name)['module']

    def _import_theme(self, modname, importer):
        return importer.find_module(modname).load_module(modname)

    def _get_active_theme(self):
        try:
            config = Config.objects.get(name='active_theme')
        except Config.DoesNotExist:
            config = None

        if config is None:
            config = Config(name='active_theme', value='default')
            config.save()

        return config.value
