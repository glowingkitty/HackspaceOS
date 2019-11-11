from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template

from hackerspace import YOUR_HACKERSPACE as HACKERSPACE
from hackerspace.models import Error, Project, Event, Guilde, MeetingNote, Space, Machine
from hackerspace.tools.space_open import getOpenNowStatus
from hackerspace.tools.tools import make_description_sentence
from hackerspace.website.search import search
from config import ADMIN_URL


def get_view_response(request, page, sub_page, hashname):
    context = {
        'view': page+'_view',
        'inspace': True if request.COOKIES.get('inspace') else None,
        'HACKERSPACE': HACKERSPACE,
        'hash': hashname,
        'page_git_url': HACKERSPACE.WEBSITE_GIT+'/Website/templates/'+page+'_view.html',
        'ADMIN_URL': ADMIN_URL,
        'user': request.user
    }

    if page == 'landingpage':
        return {**context, **{
            'slug': '/',
            'page_name': HACKERSPACE.HACKERSPACE_NAME,
            'page_description': make_description_sentence(),
            'is_open_status': getOpenNowStatus(),
            'upcoming_events': Event.objects.upcoming()[:5]
        }}

    elif page == 'values':
        return {**context, **{
            'slug': '/'+page,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Values',
            'page_description': 'Our values at '+HACKERSPACE.HACKERSPACE_NAME
        }}

    elif page == 'meetings':
        return {**context, **{
            'slug': '/'+page,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Meetings',
            'page_description': 'Join our weekly meetings!',
            'current_meeting': MeetingNote.objects.current(),
            'next_meeting': Event.objects.next_meeting(),
            'past_meetings': MeetingNote.objects.past()[:10]
        }}
    elif page == 'meeting':
        selected = MeetingNote.objects.filter(
            text_date=sub_page).first()
        return {**context, **{
            'slug': '/meeting/'+selected.text_date,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Meeting | '+selected.text_date,
            'page_description': 'Join our weekly meetings!',
            'selected': selected,
            'next_meeting': Event.objects.next_meeting(),
            'past_meetings': MeetingNote.objects.past(selected)[:10]
        }}
    elif page == 'meeting_present':
        return {**context, **{
            'slug': '/meeting/present',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Meeting | Presentation mode',
            'page_description': 'Join our weekly meetings!',
            'current_meeting': MeetingNote.objects.current()
        }}

    elif page == 'guildes':
        return {**context, **{
            'slug': '/'+page,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Guildes',
            'page_description': 'Join a guilde at '+HACKERSPACE.HACKERSPACE_NAME+'!',
            'all_guildes': Guilde.objects.all()[:10]
        }}
    elif page == 'guilde':
        if 'guilde/' not in sub_page:
            sub_page = 'guilde/'+sub_page
        selected = Guilde.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/guilde/'+sub_page,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Guilde | '+selected.str_name,
            'page_description': 'Join our weekly meetings!',
            'selected': selected
        }}

    elif page == 'spaces':
        return {**context, **{
            'slug': '/'+page,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Spaces',
            'page_description': HACKERSPACE.HACKERSPACE_NAME+' has many awesome spaces!',
            'all_spaces': Space.objects.all()[:10]
        }}
    elif page == 'space':
        if 'space/' not in sub_page:
            sub_page = 'space/'+sub_page
        selected = Space.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/space/'+sub_page,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Space | '+selected.str_name,
            'page_description': selected.text_description,
            'selected': selected
        }}

    elif page == 'machines':
        return {**context, **{
            'slug': '/'+page,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Machines',
            'page_description': HACKERSPACE.HACKERSPACE_NAME+' has all kinds of awesome machines!',
            'all_machines': Machine.objects.all()[:10]
        }}
    elif page == 'machine':
        if 'machine/' not in sub_page:
            sub_page = 'machine/'+sub_page
        selected = Machine.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/machine/'+sub_page,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Machine | '+selected.str_name,
            'page_description': selected.text_description,
            'selected': selected
        }}

    elif page == 'projects':
        return {**context, **{
            'slug': '/'+page,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Projects',
            'page_description': 'People at '+HACKERSPACE.HACKERSPACE_NAME+' created all kinds of awesome projects!',
            'all_projects': Project.objects.latest()[:10]
        }}
    elif page == 'project':
        if 'project/' not in sub_page:
            sub_page = 'project/'+sub_page
        selected = Project.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/project/'+sub_page,
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Project | '+selected.str_name,
            'page_description': selected.text_description,
            'selected': selected
        }}


def get_page_response(request, page, sub_page=None):
    print(page+'_view')
    page = page
    hash_name = request.build_absolute_uri().split(
        '#')[1] if '#' in request.build_absolute_uri() else None

    html = 'page.html' if page != 'meeting_present' else 'meeting_present.html'
    response = render(request, html, get_view_response(
        request, page, sub_page, hash_name))
    return response


def landingpage_view(request):
    return get_page_response(request, 'landingpage')


def values_view(request):
    return get_page_response(request, 'values')


def meetings_view(request):
    return get_page_response(request, 'meetings')


def meeting_present_view(request):
    if not MeetingNote.objects.current():
        return HttpResponseRedirect('/meetings')
    return get_page_response(request, 'meeting_present')


def meeting_view(request, sub_page):
    # if meeting not found, redirect to all meetings page
    if not MeetingNote.objects.filter(text_date=sub_page).exists():
        return HttpResponseRedirect('/meetings')
    return get_page_response(request, 'meeting', sub_page)


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


def guildes_view(request):
    return get_page_response(request, 'guildes')


def guilde_view(request, sub_page):
    sub_page = 'guilde/'+sub_page
    # if guilde not found, redirect to all guildes page
    if not Guilde.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/guildes')
    return get_page_response(request, 'guilde', sub_page)


def spaces_view(request):
    return get_page_response(request, 'spaces')


def space_view(request, sub_page):
    sub_page = 'space/'+sub_page
    # if space not found, redirect to all spaces page
    if not Space.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/spaces')
    return get_page_response(request, 'space', sub_page)


def machines_view(request):
    return get_page_response(request, 'machines')


def machine_view(request, sub_page):
    sub_page = 'machine/'+sub_page
    # if space not found, redirect to all spaces page
    if not Machine.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/machines')
    return get_page_response(request, 'machine', sub_page)


def projects_view(request):
    return get_page_response(request, 'projects')


def project_view(request, sub_page):
    sub_page = 'project/'+sub_page
    # if space not found, redirect to all spaces page
    if not Project.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/projects')
    return get_page_response(request, 'projectf', sub_page)


def get_view(request):
    print('get_view')
    in_space = request.COOKIES.get('in_space')
    marry_messages = []
    if request.GET.get('what', None) == 'events_slider':
        if in_space:
            events_in_5_minutes = Event.objects.in_minutes(
                minutes=5, name_only=True)
            events_in_30_minutes = Event.objects.in_minutes(
                minutes=30, name_only=True)
            if events_in_5_minutes or events_in_30_minutes:
                marry_messages.append('We have some awesome events upcoming')
            for event in events_in_5_minutes:
                marry_messages.append(event+' starts in 5 minutes.')
            for event in events_in_30_minutes:
                marry_messages.append(event+' starts in 30 minutes.')

        response = JsonResponse(
            {
                'html': get_template(
                    'components/body/events_slider.html').render({
                        'upcoming_events': Event.objects.upcoming()[:5]
                    }),
                'marryspeak': marry_messages
            }
        )
    elif request.GET.get('what', None) == 'open_status':
        response = JsonResponse({'html': getOpenNowStatus()})

    elif request.GET.get('what', None) == 'meeting_duration':
        running_since = MeetingNote.objects.current().running_since
        if in_space:
            if running_since == '1h 30min':
                marry_messages.append(
                    'Thanks everyone for partipicating in the weekly meeting. The meeting is going on now for 1 hour and 30 minutes')
            elif running_since == '2h 30min':
                marry_messages.append(
                    'I always love people actively discussion topics related to Noisebridge. However, it seems the meeting is going on now for 2 hours and 30 minutes. Please come to an end soon')

        response = JsonResponse(
            {'html': MeetingNote.objects.current().running_since, 'marryspeak': marry_messages})

    elif request.GET.get('what', None) == 'start_meeting':
        response = JsonResponse({'html': get_template(
            'components/body/meetings/current_meeting.html').render({'HACKERSPACE': HACKERSPACE})})

    elif request.GET.get('what', None):
        page = request.GET.get('what', None)
        print(page)
        if page == '__':
            page = 'landingpage'
        else:
            page = page.replace('__', '', 1)

        if '__' in page:
            page, sub_page = page.split('__')
        else:
            sub_page = None

        print(page, sub_page)

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


def load_more_view(request):
    print('load_more_view')
    if request.GET.get('what', None) and request.GET.get('from', None):
        start_from = int(request.GET.get('from', None))
        upt_to = int(start_from+10)
        response = JsonResponse({
            'html': get_template('components/body/meetings/meetings_list.html').render({
                'past_meetings': MeetingNote.objects.past()[start_from:upt_to]
            }),
            'continue_from': upt_to
        })
    else:
        response = JsonResponse({'error': 'Request incomplete or wrong'})
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
