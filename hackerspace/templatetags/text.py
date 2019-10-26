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
