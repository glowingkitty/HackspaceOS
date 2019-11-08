from django.template import Library

register = Library()


@register.filter
def upto(array, number):
    if not array:
        return []
    return array[:number]
