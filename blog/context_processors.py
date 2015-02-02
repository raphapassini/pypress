from adm.models import Config
from treemenus.models import Menu


def base_info(request):
    configs = ['site_title', 'site_desc']
    context = {}

    for c in configs:
        try:
            config = Config.objects.get(name=c)
        except Config.DoesNotExist:
            config = None

        if config:
            context[c] = config.value

    context['menus'] = {}
    for m in Menu.objects.all():
        context['menus'][m.name] = m

    return context
