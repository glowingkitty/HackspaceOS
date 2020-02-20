from django.template import Library

register = Library()


@register.filter
def getTwitterUsername(socialaccounts):
    for social in socialaccounts:
        if social['name'] == 'Twitter':
            return social['url'].split('twitter.com/')[1]


@register.filter
def exists(socialaccounts, socialaccount):
    for social in socialaccounts:
        if social['name'] == socialaccount:
            return True
