from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import get_template

from hackerspace.models import Error, Event
from hackerspace.tools.space_open import getOpenNowStatus
from hackerspace.tools.tools import make_description_sentence
from hackerspace import YOUR_HACKERSPACE as HACKERSPACE
from hackerspace.website.search import search


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
        'page_name': HACKERSPACE.HACKERSPACE_NAME+' - Server Error (Code '+(error.str_error_code if error else '????')+')',
        'page_description': 'Sorry, something went wrong! We posted it in our Git repo and the infrastructure Slack channel!',
        'cookie_consent': request.COOKIES.get('consent'),
    }
    )

    response.status_code = 500

    return response


def landingpage_view(request):
    try:
        print('landingpage_view')
        response = render(request, 'index.html', {
            'view': 'landingpage_view',
            'css_files': ['body', 'header', 'event_slider', 'result_preview', 'landingpage', 'map', 'footer'],
            'page_name': HACKERSPACE.HACKERSPACE_NAME,
            'page_description': make_description_sentence(),
            'cookie_consent': request.COOKIES.get('consent'),
            'HACKERSPACE': HACKERSPACE,
            'is_open_status': getOpenNowStatus(),
            'upcoming_events': Event.objects.upcoming()[:5]
        }
        )

        return response
    except:
        import sys
        import traceback
        exc_type, exc_value, tb = sys.exc_info()
        error_view(request, traceback.format_exc(), exc_type, exc_value, tb)


def get_view(request):
    try:
        print('get_view')
        if request.GET.get('what', None) == 'events_slider':
            response = JsonResponse(
                {
                    'html': get_template(
                        'components/body/events_slider.html').render({
                            'upcoming_events': Event.objects.upcoming()[:5]
                        })
                }
            )
        elif request.GET.get('what', None) == 'open_status':
            response = JsonResponse(
                {
                    'html': getOpenNowStatus()
                }
            )

        return response
    except:
        import sys
        import traceback
        exc_type, exc_value, tb = sys.exc_info()
        error_view(request, traceback.format_exc(), exc_type, exc_value, tb)


def search_view(request):
    # try:
    print('search_view')
    search_results = search(request.GET.get('q', None))
    response = JsonResponse(
        {
            'num_results': len(search_results),
            'html': get_template(
                'components/search/search_results.html').render({
                    'search_results': search_results
                })
        }
    )

    return response
    # except:
    #     import sys
    #     import traceback
    #     exc_type, exc_value, tb = sys.exc_info()
    #     error_view(request, traceback.format_exc(), exc_type, exc_value, tb)
