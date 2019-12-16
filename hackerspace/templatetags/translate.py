from django.template import Library
register = Library()


@register.filter
def landingpage(text, language):
    from django.template.loader import get_template
    try:
        return get_template('translations/landingpage/'+language+'.html').render({
            'word': text
        })
    except:
        try:
            return get_template('translations/landingpage/english.html').render({
                'word': text
            })
        except:
            return text


@register.filter
def donate(text, language):
    from django.template.loader import get_template
    try:
        return get_template('translations/donate/'+language+'.html').render({
            'word': text
        })
    except:
        try:
            return get_template('translations/donate/english.html').render({
                'word': text
            })
        except:
            return text


@register.filter
def menu(text, language):
    from django.template.loader import get_template
    try:
        return get_template('translations/menu/'+language+'.html').render({
            'word': text
        })
    except:
        try:
            return get_template('translations/menu/english.html').render({
                'word': text
            })
        except:
            return text


@register.filter
def values(text, language):
    from django.template.loader import get_template
    try:
        return get_template('translations/values/'+language+'.html').render({
            'word': text
        })
    except:
        try:
            return get_template('translations/values/english.html').render({
                'word': text
            })
        except:
            return text


@register.filter
def events(text, language):
    from django.template.loader import get_template
    try:
        return get_template('translations/events/'+language+'.html').render({
            'word': text
        })
    except:
        try:
            return get_template('translations/events/english.html').render({
                'word': text
            })
        except:
            return text


@register.filter
def photos(text, language):
    from django.template.loader import get_template
    try:
        return get_template('translations/photos/'+language+'.html').render({
            'word': text
        })
    except:
        try:
            return get_template('translations/photos/english.html').render({
                'word': text
            })
        except:
            return text
