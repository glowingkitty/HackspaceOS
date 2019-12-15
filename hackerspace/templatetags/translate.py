from django.template import Library
import json

register = Library()

with open('translations.json') as json_file:
    translations = json.load(json_file)


@register.filter
def text(text, language):
    from getConfig import get_config
    try:
        if language in translations[text]:
            text = translations[text][language]
        else:
            text = translations[text]['english']
        if '0SPACE0' in text:
            text = text.replace('0SPACE0', get_config('BASICS.NAME'))
        if '0CITY0' in text:
            text = text.replace('0CITY0', get_config(
                'PHYSICAL_SPACE.ADDRESS.CITY'))
        if '0HACKERS0' in text:
            text = text.replace('0HACKERS0', get_config(
                'PHYSICAL_SPACE.PEOPLE_NAME'))
        return translations[text][language]
    except:
        return text
