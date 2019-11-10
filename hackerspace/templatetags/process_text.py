import re
from django.template import Library
register = Library()


def cleanhtml(raw_html):
    cleanr = re.compile('<.*?>')
    cleantext = re.sub(cleanr, '', raw_html)
    return cleantext


@register.filter
def findSearches(text):
    if not text:
        return text

    text = cleanhtml(text)
    searches = re.findall(r'\{([^{}]*)\}\|search', text)
    for search_query in searches:
        text = text.replace('{'+search_query+'}|search', '<a class="inline_link" onclick="openMenu();enterSearch(\'' +
                            search_query+'\')" href="#">'+search_query+'</a>')

    return text
