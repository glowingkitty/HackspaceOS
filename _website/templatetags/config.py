from django.template import Library
from _setup.models import Config
from _apis.models.hackspaceOS_functions.open_status import OpenStatus

register = Library()


@register.filter
def get_config(key_name):
    return Config(key_name).value


@register.filter
def still_temporary_open_status(input):
    return OpenStatus(None).still_temporary
