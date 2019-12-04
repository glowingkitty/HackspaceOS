from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template

from hackerspace import YOUR_HACKERSPACE as HACKERSPACE
from hackerspace.models import Error, Person,Project, Event, Guilde, MeetingNote, Space, Machine, Consensus,Photo
from hackerspace.tools.space_open import getOpenNowStatus
from hackerspace.tools.tools import make_description_sentence
from hackerspace.Website.search import search
from getKey import STR__get_key


def get_view_response(request, page, sub_page, hashname):
    context = {
        'view': page+'_view',
        'in_space': True if request.COOKIES.get('in_space') else None,
        'HACKERSPACE': HACKERSPACE,
        'hash': hashname,
        'ADMIN_URL': STR__get_key('ADMIN_URL'),
        'user': request.user
    }

    if page == 'landingpage':
        return {**context, **{
            'slug': '/',
            'page_git_url': '/Website/templates/landingpage_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME,
            'page_description': make_description_sentence(),
            'is_open_status': getOpenNowStatus(),
            'upcoming_events': Event.objects.QUERYSET__upcoming()[:5],
            'photos':Photo.objects.latest()[:33]
        }}

    elif page == 'values':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/Website/templates/values_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Values',
            'page_description': 'Our values at '+HACKERSPACE.HACKERSPACE_NAME
        }}

    elif page == 'meetings':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/Website/templates/meetings_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Meetings',
            'page_description': 'Join our weekly meetings!',
            'current_meeting': MeetingNote.objects.current(),
            'next_meeting': Event.objects.QUERYSET__next_meeting(),
            'past_meetings': MeetingNote.objects.past()[:10]
        }}
    elif page == 'meeting':
        selected = MeetingNote.objects.filter(
            text_date=sub_page).first()
        return {**context, **{
            'slug': '/meeting/'+selected.text_date,
            'page_git_url': '/Website/templates/meeting_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Meeting | '+selected.text_date,
            'page_description': 'Join our weekly meetings!',
            'selected': selected,
            'next_meeting': Event.objects.QUERYSET__next_meeting(),
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
            'page_git_url': '/Website/templates/results_list.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Guildes',
            'page_description': 'Join a guilde at '+HACKERSPACE.HACKERSPACE_NAME+'!',
            'headline': 'Guildes',
            'description': 'A guilde is a group at {} with a common interest area, responsible for specific spaces and machines at {}.'.format(HACKERSPACE.HACKERSPACE_NAME, HACKERSPACE.HACKERSPACE_NAME),
            'wiki_url': None,
            'add_new_requires_user': True,
            'addnew_url': '/{}/hackerspace/guilde/add/'.format(STR__get_key('ADMIN_URL')),
            'addnew_text': 'Add guilde',
            'all_results': Guilde.objects.all()[:10],
            'results_count': Guilde.objects.count(),
            'show_more': page
        }}
    elif page == 'guilde':
        if 'guilde/' not in sub_page:
            sub_page = 'guilde/'+sub_page
        selected = Guilde.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/guilde/'+sub_page,
            'page_git_url': '/Website/templates/guilde_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Guilde | '+selected.str_name,
            'page_description': 'Join our weekly meetings!',
            'selected': selected
        }}

    elif page == 'spaces':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/Website/templates/results_list.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Spaces',
            'page_description': HACKERSPACE.HACKERSPACE_NAME+' has many awesome spaces!',
            'headline': 'Spaces',
            'description': 'At {} fellow hackers like you created all kinds of awesome spaces. Check them out!'.format(HACKERSPACE.HACKERSPACE_NAME),
            'wiki_url': None,
            'add_new_requires_user': True,
            'addnew_url': '/{}/hackerspace/space/add/'.format(STR__get_key('ADMIN_URL')),
            'addnew_text': 'Add space',
            'all_results': Space.objects.all()[:10],
            'results_count': Space.objects.count(),
            'show_more': page
        }}
    elif page == 'space':
        if 'space/' not in sub_page:
            sub_page = 'space/'+sub_page
        selected = Space.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/space/'+sub_page,
            'page_git_url': '/Website/templates/space_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Space | '+selected.str_name,
            'page_description': selected.text_description,
            'selected': selected
        }}

    elif page == 'machines':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/Website/templates/results_list.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Machines',
            'page_description': HACKERSPACE.HACKERSPACE_NAME+' has all kinds of awesome machines!',
            'headline': 'Machines',
            'description': 'We have many super useful machines at {}, allowing you to build nearly everything you want to build!'.format(HACKERSPACE.HACKERSPACE_NAME),
            'wiki_url': None,
            'add_new_requires_user': True,
            'addnew_url': '/{}/hackerspace/machine/add/'.format(STR__get_key('ADMIN_URL')),
            'addnew_text': 'Add machine',
            'all_results': Machine.objects.all()[:10],
            'results_count': Machine.objects.count(),
            'show_more': page
        }}
    elif page == 'machine':
        if 'machine/' not in sub_page:
            sub_page = 'machine/'+sub_page
        selected = Machine.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/machine/'+sub_page,
            'page_git_url': '/Website/templates/machine_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Machine | '+selected.str_name,
            'page_description': selected.text_description,
            'selected': selected
        }}

    elif page == 'projects':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/Website/templates/results_list.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Projects',
            'page_description': 'People at '+HACKERSPACE.HACKERSPACE_NAME+' created all kinds of awesome projects!',
            'headline': 'Projects',
            'description': 'At {} fellow hackers like you created all kinds of awesome projects - both their own and projects for the space. Check them out - and create your own one!'.format(HACKERSPACE.HACKERSPACE_NAME),
            'wiki_url': None,
            'add_new_requires_user': False,
            'addnew_url': '{}c/projects/'.format(HACKERSPACE.HACKERSPACE_DISCOURSE_URL),
            'addnew_text': 'Add project',
            'all_results': Project.objects.latest()[:10],
            'results_count': Project.objects.count(),
            'show_more': page
        }}
    elif page == 'project':
        if 'project/' not in sub_page:
            sub_page = 'project/'+sub_page
        selected = Project.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/project/'+sub_page,
            'page_git_url': '/Website/templates/project_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Project | '+selected.str_name,
            'page_description': selected.text_description,
            'selected': selected
        }}

    elif page == 'consensus':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/Website/templates/consensus_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Big-C consensus items',
            'page_description': 'When you want to do something that would drastically change '+HACKERSPACE.HACKERSPACE_NAME+' (or need a lot of money from Noisebridge for a project) - suggest a Big-C consensus item!',
            'all_current_items': Consensus.objects.current(),
            'all_current_items_count': Consensus.objects.current().count(),
            'all_archived_items': Consensus.objects.archived(),
            'all_archived_items_count': Consensus.objects.archived().count(),
        }}

    elif page == 'photos':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/Website/templates/photos_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Photos',
            'page_description': 'Explore '+HACKERSPACE.HACKERSPACE_NAME+'\'s history in photos!',
            'photos': Photo.objects.latest()[:30],
        }}

    elif page == 'events':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/Website/templates/results_list.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Events',
            'page_description': 'At '+HACKERSPACE.HACKERSPACE_NAME+' we have all kinds of cool events - organized by your fellow hackers!',
            'headline': 'Events',
            'description': '{} is a place where people come together to learn, share ideas and have an excellent time. Nearly all of our events are free - so just come by and join us - or organize your own event at {}!'.format(HACKERSPACE.HACKERSPACE_NAME, HACKERSPACE.HACKERSPACE_NAME),
            'add_new_requires_user': False,
            'addnew_url': '/event/new',
            'addnew_text': 'Organize an event',
            'addnew_target': 'same_tab',
            'addnew_menu_selected': 'menu_h_events',
            'all_results': Event.objects.QUERYSET__upcoming()[:10],
            'results_count': Event.objects.count(),
            'show_more': page
        }}
    elif page == 'event':
        if 'event/' not in sub_page:
            sub_page = 'event/'+sub_page
        selected = Event.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/event/'+sub_page,
            'page_git_url': '/Website/templates/event_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | Event | '+selected.str_name,
            'page_description': selected.text_description,
            'selected': selected,
            'photos':Photo.objects.latest()[:33]
        }}
    elif page == 'event_new':
        from django.middleware.csrf import get_token
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/Website/templates/event_new_view.html',
            'page_name': HACKERSPACE.HACKERSPACE_NAME+' | New event',
            'page_description': 'Organize an event at '+HACKERSPACE.HACKERSPACE_NAME,
            'upcoming_events': Event.objects.QUERYSET__upcoming()[:4],
            'default_space': Space.objects.filter(str_name=HACKERSPACE.EVENTS_SPACE_DEFAULT).first(),
            'all_spaces': Space.objects.exclude(str_name=HACKERSPACE.EVENTS_SPACE_DEFAULT),
            'all_guildes':Guilde.objects.all(),
            'csrf_token': get_token(request)
        }}


def get_page_response(request, page, sub_page=None):
    print('LOG: get_page_response(request,page={},sub_page={})'.format(page,sub_page))
    page = page
    hash_name = request.build_absolute_uri().split(
        '#')[1] if '#' in request.build_absolute_uri() else None

    html = 'page.html' if page != 'meeting_present' else 'meeting_present.html'
    response = render(request, html, get_view_response(
        request, page, sub_page, hash_name))
    return response


def landingpage_view(request):
    print('LOG: landingpage_view(request)')
    return get_page_response(request, 'landingpage')


def values_view(request):
    print('LOG: values_view(request)')
    return get_page_response(request, 'values')


def meetings_view(request):
    print('LOG: meetings_view(request)')
    return get_page_response(request, 'meetings')


def meeting_present_view(request):
    print('LOG: meeting_present_view(request)')
    if not MeetingNote.objects.current():
        return HttpResponseRedirect('/meetings')
    return get_page_response(request, 'meeting_present')


def meeting_view(request, sub_page):
    print('LOG: meeting_view(request,sub_page={})'.format(sub_page))
    # if meeting not found, redirect to all meetings page
    if not MeetingNote.objects.filter(text_date=sub_page).exists():
        return HttpResponseRedirect('/meetings')
    return get_page_response(request, 'meeting', sub_page)


def meeting_end_view(request):
    print('LOG: meeting_end_view(request)')
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
    print('LOG: guildes_view(request)')
    return get_page_response(request, 'guildes')


def guilde_view(request, sub_page):
    print('LOG: guilde_view(request, {})'.format(sub_page))
    sub_page = 'guilde/'+sub_page
    # if guilde not found, redirect to all guildes page
    if not Guilde.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/guildes')
    return get_page_response(request, 'guilde', sub_page)


def spaces_view(request):
    print('LOG: spaces_view(request)')
    return get_page_response(request, 'spaces')


def space_view(request, sub_page):
    print('LOG: space_view(request, {})'.format(sub_page))
    sub_page = 'space/'+sub_page
    # if space not found, redirect to all spaces page
    if not Space.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/spaces')
    return get_page_response(request, 'space', sub_page)


def machines_view(request):
    print('LOG: machines_view(request)')
    return get_page_response(request, 'machines')


def machine_view(request, sub_page):
    print('LOG: machine_view(request, {})'.format(sub_page))
    sub_page = 'machine/'+sub_page
    # if space not found, redirect to all spaces page
    if not Machine.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/machines')
    return get_page_response(request, 'machine', sub_page)


def projects_view(request):
    print('LOG: projects_view(request)')
    return get_page_response(request, 'projects')


def project_view(request, sub_page):
    print('LOG: project_view(request, {})'.format(sub_page))
    sub_page = 'project/'+sub_page
    # if space not found, redirect to all spaces page
    if not Project.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/projects')
    return get_page_response(request, 'project', sub_page)


def consensus_view(request):
    print('LOG: consensus_view(request)')
    return get_page_response(request, 'consensus')

def photos_view(request):
    print('LOG: photos_view(request)')
    return get_page_response(request, 'photos')

def events_view(request):
    print('LOG: events_view(request)')
    return get_page_response(request, 'events')

def events_json_view(request):
    print('LOG: events_json_view(request)')
    return Event.objects.QUERYSET__upcoming().RESPONSE__JSON()

def event_new_view(request):
    print('LOG: event_new_view(request)')
    return get_page_response(request, 'event_new')


def event_view(request, sub_page):
    print('LOG: event_view(request, {})'.format(sub_page))
    return_json = False
    if sub_page.endswith('.json'):
        print('LOG: --> detected .json at end of URL')
        sub_page = sub_page.replace('.json','')
        return_json = True
        
    sub_page = 'event/'+sub_page
    # if space not found, redirect to all spaces page
    if not Event.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/events')
    
    # if .json at end of url, return json, else page
    if return_json==True:
        print('LOG: --> return JsonResponse')
        return JsonResponse(Event.objects.filter(str_slug=sub_page).first().json_data)

    else:
        return get_page_response(request, 'event', sub_page)


def get_view(request):
    print('LOG: get_view(request)')
    in_space = request.COOKIES.get('in_space')
    marry_messages = []
    response = None
    if request.GET.get('what', None) == 'events_slider':
        if in_space:
            events_in_5_minutes = Event.objects.LIST__in_minutes(
                minutes=5, name_only=True)
            events_in_30_minutes = Event.objects.LIST__in_minutes(
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
                        'upcoming_events': Event.objects.QUERYSET__upcoming()[:5]
                    }),
                'marryspeak': marry_messages
            }
        )
    elif request.GET.get('what', None) == 'open_status':
        response = JsonResponse({'html': getOpenNowStatus()})

    elif request.GET.get('what', None) == 'event_overlap':
        str_date = request.GET.get('date', None)
        str_time = request.GET.get('time', None)
        str_duration = request.GET.get('duration', None)
        str_space = request.GET.get('space', None)
        if str_date and str_time and str_duration and str_space:
            from hackerspace.Website.views_helper_functions import INT__UNIX_from_date_and_time_STR,INT__duration_minutes
            
            overlapping_events = Event.objects.JSON__overlapping_events(
                        INT__UNIX_from_date_and_time_STR(str_date, str_time),
                        INT__duration_minutes(str_duration),
                        request.GET.get('space', None),
                    )

            response = JsonResponse({
                'int_overlapping_events':len(overlapping_events['overlapping_events']),
                'html': get_template(
                'components/body/event_new/form_elements/overlapping_events.html').render({
                    'overlapping_events': overlapping_events
                })})

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

        if page == '__':
            page = 'landingpage'
        else:
            page = page.replace('__', '', 1)

        if '__' in page and not page.endswith('__new'):
            page, sub_page = page.split('__')
        else:
            sub_page = None

        page = page.replace('__', '_')

        hashname = page.split('#')[1] if '#' in page else None

        response_context = get_view_response(request, page, sub_page, hashname)
        response = JsonResponse(
            {
                'html': get_template('results_list.html' if 'all_results' in response_context else page+'_view.html').render(response_context),
                'page_name': response_context['page_name']
            }
        )

    if not response:
        response = JsonResponse({'error': 'no "what" defined'})
        response.status_code = 404

    print('LOG: --> return response')
    return response


def load_more_view(request):
    print('LOG: load_more_view(request)')
    from hackerspace.Website.views_helper_functions import JSON_RESPONSE_more_results,JSON_RESPONSE_more_photos

    if request.GET.get('what', None) and request.GET.get('from', None):
        if request.GET.get('what', None) == 'meeting_notes':
            response = JSON_RESPONSE_more_results(
                request, 'meetings/meetings_list.html', MeetingNote.objects.past())
        elif request.GET.get('what', None) == 'events':
            response = JSON_RESPONSE_more_results(
                request, 'results_list_entries.html', Event.objects.QUERYSET__upcoming())
        elif request.GET.get('what', None) == 'projects':
            response = JSON_RESPONSE_more_results(
                request, 'results_list_entries.html', Project.objects.latest())
        elif request.GET.get('what', None) == 'spaces':
            response = JSON_RESPONSE_more_results(
                request, 'results_list_entries.html', Space.objects.all())
        elif request.GET.get('what', None) == 'machines':
            response = JSON_RESPONSE_more_results(
                request, 'results_list_entries.html', Machine.objects.all())
        elif request.GET.get('what', None) == 'guildes':
            response = JSON_RESPONSE_more_results(
                request, 'results_list_entries.html', Guilde.objects.all())
        elif request.GET.get('what', None) == 'consensus':
            response = JSON_RESPONSE_more_results(
                request, 'consensus_items_entries.html', Consensus.objects.latest())
        elif request.GET.get('what', None) == 'photos':
            response = JSON_RESPONSE_more_photos(request)
    else:
        response = JsonResponse({'error': 'Request incomplete or wrong'})
        response.status_code = 404

    print('LOG: --> return response')
    return response


def save_view(request):
    print('LOG: save_view(request)')
    if request.GET.get('keyword', None) and request.GET.get('origin', None) and MeetingNote.objects.filter(text_date=request.GET.get('origin', None).split('/')[1]).exists():
        meeting = MeetingNote.objects.filter(
            text_date=request.GET.get('origin', None).split('/')[1]).first()

        meeting.add_keyword(request.GET.get('keyword'))
        response = JsonResponse({'success': True})
    else:
        response = JsonResponse({'error': 'Request incomplete or wrong'})
        response.status_code = 404

    print('LOG: --> return response')
    return response


def remove_view(request):
    print('LOG: remove_view(request)')
    if request.GET.get('keyword', None) and request.GET.get('origin', None) and MeetingNote.objects.filter(text_date=request.GET.get('origin', None).split('/')[1]).exists():
        meeting = MeetingNote.objects.filter(
            text_date=request.GET.get('origin', None).split('/')[1]).first()

        meeting.remove_keyword(request.GET.get('keyword'))
        response = JsonResponse({'success': True})
    else:
        response = JsonResponse({'error': 'Request incomplete or wrong'})
        response.status_code = 404

    print('LOG: --> return response')
    return response


def search_view(request):
    print('LOG: search_view(request)')
    search_results = search(request.GET.get('q', None),
                            request.GET.get('filter', None))
    response = JsonResponse(
        {
            'num_results': len(search_results),
            'html': get_template(
                'components/search/search_results.html').render({
                    'search_results': search_results
                }) if not request.GET.get('filter', None) else get_template('components/body/event_new/hosts_search_results.html').render({
                    'all_hosts': search_results[:4],
                }) if request.GET.get('filter', None)=='hosts' else get_template('components/body/results_list_entries.html').render({
                    'all_results': search_results[:4],
                }),
        }
    )

    print('LOG: --> return response')
    return response

def new_view(request):
    print('LOG: new_view(request)')

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

    elif request.GET.get('what', None) == 'event':
        from hackerspace.APIs.slack import send_message
        from hackerspace.YOUR_HACKERSPACE import DOMAIN
        from hackerspace.Website.views_helper_functions import INT__UNIX_from_date_and_time_STR,INT__duration_minutes
        int_UNIXtime_event_start = INT__UNIX_from_date_and_time_STR(request.GET.get('date',None),request.GET.get('time',None))
        int_minutes_duration = INT__duration_minutes(request.GET.get('duration',None))
        
        new_event = Event(
            boolean_approved=request.user.is_authenticated,
            str_name=request.GET.get('name',None),
            int_UNIXtime_event_start=int_UNIXtime_event_start,
            int_minutes_duration=int_minutes_duration,
            int_UNIXtime_event_end=int_UNIXtime_event_start+(60*int_minutes_duration),
            url_featured_photo=request.GET.get('photo',None),
            text_description=request.GET.get('description',None),
            one_space=Space.objects.QUERYSET__by_name(request.GET.get('space',None)),
            one_guilde=Guilde.objects.QUERYSET__by_name(request.GET.get('guilde',None)),
            str_crowd_size=request.GET.get('expected_crowd',None),
            str_welcomer=request.GET.get('event_welcomer',None)
        )
        if request.GET.get('location',None):
            if request.GET.get('location',None)!=HACKERSPACE.HACKERSPACE_NAME:
                new_event.str_location = request.GET.get('location',None)
        if request.GET.get('repeating',None):
            # if repeating, mark as such and auto generate new upcoming events with "update_database" command
            str_repeating_how_often = request.GET.get('repeating',None)
            str_repeating_up_to = request.GET.get('repeating_up_to',None)
            
            if str_repeating_how_often and str_repeating_how_often!='':
                new_event.int_series_startUNIX = new_event.int_UNIXtime_event_start
                new_event.str_series_repeat_how_often = str_repeating_how_often
            
            if str_repeating_up_to and str_repeating_up_to!='':
                new_event.int_series_endUNIX = INT__UNIX_from_date_and_time_STR(str_repeating_up_to,request.GET.get('time',None))


        if request.GET.get('volunteers',None)=='yes' and request.user.is_authenticated:
            # create wish entry and save URL
            new_event = new_event.create_volunteer_wish()

        new_event.save()

        hosts = request.GET.get('hosts',None)
        if hosts:
            if hosts.startswith(','):
                hosts = hosts[1:]
            hosts = hosts.split(',')
            for host in hosts:
                new_event.many_hosts.add(Person.objects.by_url_discourse(host))

        # if event is repeating, create upcoming instances
        new_event = new_event.create_upcoming_instances()

        # if loggedin user: share event to other platforms (Meetup, Discourse, etc.)
        if request.user.is_authenticated:
            new_event.create_discourse_event()
            new_event.create_meetup_event()
        
        # else (if event created via live website) inform via slack about new event and give community chance to delete it or confirm it
        elif 'HTTP_HOST' in request.META and request.META['HTTP_HOST']==DOMAIN:
            send_message(
                'A website visitor created a new event via our website.\n'+
                'If no one deletes it within the next 24 hours, it will be automatically published and appears in our website search'+(', meetup group' if STR__get_key('MEETUP.ACCESS_TOKEN') else '')+(' and discourse' if STR__get_key('DISCOURSE_API_KEY') else '')+'.\n'+
                '🚫-> Does this event already exist or is it spam? Open on the following event link and click "Delete event".\n'+
                '✅-> You have a user account for our website and want to publish the event directly? Open on the following event link and click "Approve event".\n'+
                'https://'+DOMAIN+'/'+new_event.str_slug
                )
        else:
            print('LOG: --> Request not sent via hackerspace domain. Skipped notifying via Slack.')

        # if user is signed in and event autoapproved - direct to event page, else show info
        response = JsonResponse(
            {
                'url_next': '/'+new_event.str_slug
            }
        )

    print('LOG: --> return response')
    return response



def upload_view(request,what):
    print('LOG: upload_view(request,what={})'.format(what))

    if what == 'event-image':
        if request.FILES['images[0]'].content_type!='image/jpeg' and request.FILES['images[0]'].content_type!='image/png':
            response = JsonResponse({
                            'notification': get_template('components/notification.html').render({
                                'text_message': 'Please upload a JPG or PNG image.',
                                'str_icon': 'error'
                            })})
            response.status_code = 500

        else:
            import boto3
            import os,sys
            from hackerspace.YOUR_HACKERSPACE import AWS_S3_BUCKET_NAME,AWS_S3_URL
            from getKey import STR__get_key
            
            
            session = boto3.Session(
                aws_access_key_id=STR__get_key('AWS_ACCESS_KEYID'),
                aws_secret_access_key=STR__get_key('AWS_SECRET_ACCESS_KEY'),
            )
            s3 = session.resource('s3')
            image = request.FILES['images[0]']

            s3.Bucket(AWS_S3_BUCKET_NAME).put_object(Key=image.name, Body=image,ACL='public-read')
            response = JsonResponse({'url_image': 'https://'+AWS_S3_URL+'/'+image.name})

    print('LOG: --> return response')
    return response


def approve_event_view(request):
    print('LOG: approve_event_view(request)')

    if request.user.is_authenticated()==False:
        print('LOG: --> Failed: User not logged in')
        response = JsonResponse({'success': False})
        response.status_code = 403
    elif not request.GET.get('str_slug', None) or Event.objects.filter(boolean_approved=False,str_slug=request.GET.get('str_slug', None)).exists()==False:
        print('LOG: --> Failed: Result not found')
        response = JsonResponse({'success': False})
        response.status_code = 404
    else:
        from hackerspace.APIs.slack import send_message
        from hackerspace.YOUR_HACKERSPACE import DOMAIN
        # approve event and all upcoming ones
        event = Event.objects.filter(boolean_approved=False,str_slug=request.GET.get('str_slug', None)).first()

        upcoming_events = Event.objects.filter(boolean_approved=False,str_name=event.str_name).all()
        print('LOG: --> Approve all upcoming events')
        for event in upcoming_events:
            event.boolean_approved=True
            event.save()

        # notify via slack that event was approved and by who
        if 'HTTP_HOST' in request.META and request.META['HTTP_HOST']==DOMAIN:
            send_message('✅'+str(request.user)+' approved the event "'+event.str_name+'":\nhttps://'+DOMAIN+'/'+event.str_slug)

        response = JsonResponse({'success': True})
        response.status_code = 200

    print('LOG: --> return response')
    return response


def delete_event_view(request):
    print('LOG: delete_event_view(request)')

    if not request.GET.get('str_slug', None) or Event.objects.filter(str_slug=request.GET.get('str_slug', None)).exists()==False:
        print('LOG: --> Failed: Result not found')
        response = JsonResponse({'success': False})
        response.status_code = 404
    else:
        from hackerspace.APIs.slack import send_message
        from hackerspace.YOUR_HACKERSPACE import DOMAIN
        # approve event and all upcoming ones
        event = Event.objects.filter(str_slug=request.GET.get('str_slug', None)).first()

        print('LOG: --> Delete all upcoming events')
        Event.objects.filter(str_name=event.str_name).delete()

        # notify via slack that event was deleted and by who
        if 'HTTP_HOST' in request.META and request.META['HTTP_HOST']==DOMAIN:
            send_message('🚫'+str(request.user)+' deleted the event "'+event.str_name+'"')

        response = JsonResponse({'success': True})
        response.status_code = 200

    print('LOG: --> return response')
    return response