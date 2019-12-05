from django.template import Library
from getConfig import get_config as get

register = Library()


@register.filter
def get_config(key_name):
    return get(key_name)
