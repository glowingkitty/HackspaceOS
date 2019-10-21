from django.shortcuts import render
from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_NAME
from hackerspace.errors import Error


def error_view(request, error_log, exc_type, exc_value, tb):
    error = Error(
        json_context={
            'origin': 'views.py',
            'error_log': error_log,
            'exc_type': exc_type,
            'exc_value': exc_value,
            'tb': tb
        }
    )

    response = render(request, '500.html', {
        'page_name': HACKERSPACE_NAME+' - Server Error (Code '+(error.str_error_code if error else '????')+')',
        'page_description': 'Sorry, something went wrong! We posted it in our Git repo and the infrastructure Slack channel!',
        'cookie_consent': request.COOKIES.get('consent'),
    }
    )

    return response


def landingpage_view(request):
    try:
        response = render(request, '500.html', {
            'page_name': 'SkillMe - Server Error (Code '+(error.str_error_code if error else '????')+')',
            'page_description': 'Sorry, something went wrong! We got notified and work on fixing it!',
            'page_keywords': 'learn to code,software development',
            'cookie_consent': request.COOKIES.get('consent'),
        }
        )

        return response
    except:
        import sys
        import traceback
        exc_type, exc_value, tb = sys.exc_info()
        error_view(request, traceback.format_exc(), exc_type, exc_value, tb)
