from django.template import Library
from getKey import BOOLEAN__key_exists

register = Library()


@register.filter
def key_exists(str_key_name):
    return BOOLEAN__key_exists(str_key_name)
