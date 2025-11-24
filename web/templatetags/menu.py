from django import template
from django.conf import settings
register = template.Library()

@register.inclusion_tag("tag/nb_menu.html")
def nb_menu(request):
    menu_list = settings.NB_MENU.get(request.nb_user.role)
    return {'menu_list': menu_list}

