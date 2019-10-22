from django.template import Library

register = Library()


@register.filter
def getCSSpath(filename):
    return 'css/'+filename+'.css'
