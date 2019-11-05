from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import get_template

from hackerspace.models import Error, Event, MeetingNote
from hackerspace.tools.space_open import getOpenNowStatus
from hackerspace.tools.tools import make_description_sentence
from hackerspace import YOUR_HACKERSPACE as HACKERSPACE
from hackerspace.website.search import search
from django.http import HttpResponseRedirect


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
    print('landingpage_view')
    response = render(request, 'page.html', {
        'view': 'landingpage_view',
        'css_files': ['buttons', 'divider', 'fonts', 'body', 'header', 'event_slider', 'result_preview', 'landingpage', 'map', 'footer', 'overlays'],
        'page_name': HACKERSPACE.HACKERSPACE_NAME,
        'page_description': make_description_sentence(),
        'cookie_consent': request.COOKIES.get('consent'),
        'HACKERSPACE': HACKERSPACE,
        'is_open_status': getOpenNowStatus(),
        'upcoming_events': Event.objects.upcoming()[:5]
    }
    )

    return response


def meetings_view(request):
    print('meetings_view')
    response = render(request, 'page.html', {
        'view': 'meetings_view',
        'css_files': ['buttons', 'divider', 'fonts', 'body', 'header', 'result_preview', 'landingpage', 'footer', 'overlays', 'meetings'],
        'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Meetings',
        'page_description': 'Join our weekly meetings!',
        'cookie_consent': request.COOKIES.get('consent'),
        'HACKERSPACE': HACKERSPACE,
        'current_meeting': MeetingNote.objects.current(),
        'next_meeting': Event.objects.next_meeting(),
        'past_meetings': MeetingNote.objects.past()[:4]
    }
    )

    return response


def meeting_present_view(request):
    print('meeting_present_view')
    current_meeting = MeetingNote.objects.current()
    if not current_meeting:
        return HttpResponseRedirect('/meetings')

    response = render(request, 'meeting_present.html', {
        'view': 'meeting_present_view',
        'css_files': ['buttons', 'divider', 'fonts', 'body', 'header', 'meetings', 'overlays'],
        'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Meeting | Presentation mode',
        'page_description': 'Join our weekly meetings!',
        'cookie_consent': request.COOKIES.get('consent'),
        'HACKERSPACE': HACKERSPACE,
        'current_meeting': MeetingNote.objects.current()
    }
    )

    return response


def meeting_end_view(request):
    print('meeting_end_view')
    current_meeting = MeetingNote.objects.current()
    if current_meeting:
        current_meeting.end()
        response = JsonResponse(
            {'meeting_url': '/meeting/'+current_meeting.text_date})

    else:
        response = JsonResponse({'alert': 'No current meeting found'})
        response.status_code = 500

    return response


def meeting_entry_view(request, date):
    print('meeting_entry_view')
    selected_meeting = MeetingNote.objects.filter(text_date=date).first()

    # if meeting not found, redirect to all meetings page
    if not selected_meeting:
        return HttpResponseRedirect('/meetings')

    response = render(request, 'page.html', {
        'view': 'meeting_entry_view',
        'css_files': ['buttons', 'divider', 'fonts', 'body', 'header', 'result_preview', 'landingpage', 'footer', 'overlays', 'meetings'],
        'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Meeting | '+selected_meeting.text_date,
        'page_description': 'Join our weekly meetings!',
        'cookie_consent': request.COOKIES.get('consent'),
        'HACKERSPACE': HACKERSPACE,
        'selected_meeting': selected_meeting,
        'next_meeting': Event.objects.next_meeting(),
        'past_meetings': MeetingNote.objects.past(selected_meeting)[:4]
    }
    )

    return response


def get_view(request):
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
    elif request.GET.get('what', None) == 'start_meeting':
        response = JsonResponse(
            {
                'html': get_template('components/body/meetings/current_meeting.html').render({'HACKERSPACE': HACKERSPACE})
            }
        )

    return response


def save_view(request):
    print('save_view')
    if request.GET.get('keyword', None) and request.META['HTTP_REFERER'] and MeetingNote.objects.filter(text_date=request.META['HTTP_REFERER'].split('meeting/')[1]).exists():
        meeting = MeetingNote.objects.filter(
            text_date=request.META['HTTP_REFERER'].split('meeting/')[1]).first()

        meeting.add_keyword(request.GET.get('keyword'))
        response = JsonResponse({'success': True})
    else:
        response = JsonResponse({'error': 'Request incomplete or wrong'})
        response.status_code = 404

    return response


def remove_view(request):
    print('remove_view')
    print(request.META['HTTP_REFERER'])
    if request.GET.get('keyword', None) and request.META['HTTP_REFERER'] and MeetingNote.objects.filter(text_date=request.META['HTTP_REFERER'].split('meeting/')[1]).exists():
        meeting = MeetingNote.objects.filter(
            text_date=request.META['HTTP_REFERER'].split('meeting/')[1]).first()

        meeting.remove_keyword(request.GET.get('keyword'))
        response = JsonResponse({'success': True})
    else:
        response = JsonResponse({'error': 'Request incomplete or wrong'})
        response.status_code = 404

    return response


def search_view(request):
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


def new_view(request):
    print('new_view')

    if request.GET.get('what', None) == 'meeting':
        new_meeting = MeetingNote()
        new_meeting.save()

        response = JsonResponse(
            {
                'html': get_template(
                    'components/body/meetings/current_meeting.html').render({
                        'current_meeting': new_meeting,
                        'HACKERSPACE': HACKERSPACE,
                    })
            }
        )

    return response
