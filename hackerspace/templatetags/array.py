from django.template import Library

register = Library()


@register.filter
def upto(array, number):
    return array[:number]
