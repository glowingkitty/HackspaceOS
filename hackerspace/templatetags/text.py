from django.template import Library
from hackerspace.tools.tools import remove_tags

register = Library()


@register.filter
def prepareForTextCarusel(HACKERSPACE_IS_SENTENCES):
    output = ''
    for sentence in HACKERSPACE_IS_SENTENCES:
        output += '"'+remove_tags(sentence)+'", '
    if output.endswith(', '):
        output = output[:-2]
    return output


@register.filter
def shorten(text, limit):
    if len(text) > limit:
        return text[:limit]+'...'
    else:
        return text


@register.filter
def split(text, separator):
    return text.split(separator)


@register.filter
def classname(value):
    return value.__class__.__name__.lower()


@register.filter
def getDefaultImage(name):
    name = name.lower()
    if 'game' in name:
        return 'game'
    elif 'music' in name:
        return 'music'
    elif 'sewing' in name:
        return 'sewing'
    else:
        return 'class'
