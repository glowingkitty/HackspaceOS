from django.http import JsonResponse
from django.shortcuts import render
from django.template.loader import get_template

from hackerspace.models import Error, Event, MeetingNote
from hackerspace.tools.space_open import getOpenNowStatus
from hackerspace.tools.tools import make_description_sentence
from hackerspace import YOUR_HACKERSPACE as HACKERSPACE
from hackerspace.website.search import search
from django.http import HttpResponseRedirect


def get_view_response(request, page, sub_page, hashname):
    if page == 'landingpage':
        return {
            'slug': '/',
            'view': page+'_view',
            'inspace': True if request.COOKIES.get('inspace') else None,
            'page_name': HACKERSPACE.HACKERSPACE_NAME,
            'page_description': make_description_sentence(),
            'cookie_consent': request.COOKIES.get('consent'),
            'HACKERSPACE': HACKERSPACE,
            'is_open_status': getOpenNowStatus(),
            'upcoming_events': Event.objects.upcoming()[:5],
            'hash': hashname
        }
    elif page == 'meetings':
        return {
            'slug': page,
            'view': page+'_view',
            'inspace': True if request.COOKIES.get('inspace') else None,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Meetings',
            'page_description': 'Join our weekly meetings!',
            'cookie_consent': request.COOKIES.get('consent'),
            'HACKERSPACE': HACKERSPACE,
            'current_meeting': MeetingNote.objects.current(),
            'next_meeting': Event.objects.next_meeting(),
            'past_meetings': MeetingNote.objects.past()[:4],
            'hash': hashname
        }
    elif page == 'meeting':
        selected_meeting = MeetingNote.objects.filter(
            text_date=sub_page).first()
        return {
            'view': page+'_view',
            'inspace': True if request.COOKIES.get('inspace') else None,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Meeting | '+selected_meeting.text_date,
            'page_description': 'Join our weekly meetings!',
            'cookie_consent': request.COOKIES.get('consent'),
            'HACKERSPACE': HACKERSPACE,
            'selected_meeting': selected_meeting,
            'next_meeting': Event.objects.next_meeting(),
            'past_meetings': MeetingNote.objects.past(selected_meeting)[:4]
        }


def get_page_response(request, page, sub_page=None):
    print(page+'_view')
    page = page
    hash_name = request.build_absolute_uri().split(
        '#')[1] if '#' in request.build_absolute_uri() else None
    response = render(request, 'page.html',
                      get_view_response(request, page, sub_page, hash_name))
    return response


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
    return get_page_response(request, 'landingpage')


def meetings_view(request):
    return get_page_response(request, 'meetings')


def meeting_present_view(request):
    print('meeting_present_view')
    current_meeting = MeetingNote.objects.current()
    if not current_meeting:
        return HttpResponseRedirect('/meetings')

    response = render(request, 'meeting_present.html', {
        'view': 'meeting_present_view',
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


def meeting_view(request, date):
    # if meeting not found, redirect to all meetings page
    if not MeetingNote.objects.filter(text_date=date).exists():
        return HttpResponseRedirect('/meetings')
    return get_page_response(request, 'meeting', date)


def get_view(request):
    print('get_view')
    in_space = request.COOKIES.get('in_space')
    if request.GET.get('what', None) == 'events_slider':
        response = JsonResponse(
            {
                'html': get_template(
                    'components/body/events_slider.html').render({
                        'upcoming_events': Event.objects.upcoming()[:5]
                    }),
                'events_in_30_minutes': Event.objects.in_minutes(minutes=30, name_only=True) if in_space else None,
                'events_in_5_minutes': Event.objects.in_minutes(minutes=5, name_only=True) if in_space else None,
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

    elif request.GET.get('what', None):
        page = request.GET.get('what', None)
        if page == '__':
            page = 'landingpage'
        else:
            page = page.replace('__', '', 1)

        if '__' in page:
            page, sub_page = page.split('__')
        else:
            sub_page = None

        hashname = page.split('#')[1] if '#' in page else None
        response_context = get_view_response(request, page, sub_page, hashname)
        response = JsonResponse(
            {
                'html': get_template(page+'_view.html').render(response_context),
                'page_name': response_context['page_name']
            }
        )
    else:
        response = JsonResponse({'error': 'no "what" defined'})
        response.status_code = 404

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
