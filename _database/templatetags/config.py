from django.template import Library
from config import Config

register = Library()


@register.filter
def get_config(key_name):
    return Config(key_name).value
