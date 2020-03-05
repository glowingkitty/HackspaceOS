from django.template import Library
from _setup.secrets import Secret

register = Library()


@register.filter
def key_exists(str_key_name):
    return Secret(str_key_name).exists


@register.filter
def get_key(str_key_name):
    return Secret(str_key_name).value
