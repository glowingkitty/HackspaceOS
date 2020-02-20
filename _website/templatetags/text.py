import re
from django.template import Library
from _website.tools.tools import remove_tags

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
def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


@register.filter
def shorten(text, limit):
    if text and len(text) > limit:
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


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


@register.filter
def findSearches(text, while_searching_str):
    if not text:
        return text

    text = cleanhtml(text)
    searches = re.findall(r'\{([^{}]*)\}\|search', text)
    for search_query in searches:
        text = text.replace('{'+search_query+'}|search', '<a class="inline_link" onclick="openMenu();enterSearch(\'' +
                            search_query+'\',\''+while_searching_str+'\')" href="#">'+search_query+'</a>')

    return text


@register.filter
def TEXT_replaceLinkCSS(text):
    from html import unescape
    if not text:
        return None
    return unescape(text.replace('class="linkified"', 'target="_blank" class="inline_link"').replace('\n', '<br>'))


@register.filter
def STR__first_name(text):
    return text.split(' ')[0]


@register.filter
def STR__remove_hash(text):
    if '#' in text:
        return text.split('#')[1]
    else:
        return text


@register.filter
def STR__class_name(text):
    return text.lower().replace(' ', '_')
