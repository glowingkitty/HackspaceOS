from django.template import Library
from getKey import BOOLEAN__key_exists, STR__get_key

register = Library()


@register.filter
def key_exists(str_key_name):
    return BOOLEAN__key_exists(str_key_name)


@register.filter
def get_key(str_key_name):
    return STR__get_key(str_key_name)
