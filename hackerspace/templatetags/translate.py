from django.template import Library
register = Library()


@register.filter
def landingpage(text, language):
    from django.template.loader import get_template
    return get_template('translations/landingpage.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def donate(text, language):
    from django.template.loader import get_template
    return get_template('translations/donate.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def menu(text, language):
    from django.template.loader import get_template
    return get_template('translations/menu.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def values(text, language):
    from django.template.loader import get_template
    return get_template('translations/values.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def results_lists(text, language):
    from django.template.loader import get_template
    return get_template('translations/results_lists.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def events(text, language):
    from django.template.loader import get_template
    return get_template('translations/events.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def photos(text, language):
    from django.template.loader import get_template
    return get_template('translations/photos.html').render({
        'word': text,
        'language': language
    }).lstrip().rstrip()


@register.filter
def meetings(text, language):
    from django.template.loader import get_template
    return get_template('translations/meetings.html').render({
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
