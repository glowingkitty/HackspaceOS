from django.template import Library
register = Library()


@register.filter
def landingpage(text, language):
    from django.template.loader import get_template
    return get_template('landingpage.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def donate(text, language):
    from django.template.loader import get_template
    return get_template('donate.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def menu(text, language):
    from django.template.loader import get_template
    return get_template('menu.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def values(text, language):
    from django.template.loader import get_template
    return get_template('values.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def results_lists(text, language):
    from django.template.loader import get_template
    return get_template('results_lists.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def events(text, language):
    from django.template.loader import get_template
    return get_template('events.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def photos(text, language):
    from django.template.loader import get_template
    return get_template('photos.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def meetings(text, language):
    from django.template.loader import get_template
    return get_template('meetings.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def get_language_local_name(language):
    languages = {
        'english': 'English',
        'hebrew': 'עברית',
        'german': 'Deutsch'
    }
    return languages[language]
