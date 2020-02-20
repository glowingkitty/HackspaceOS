from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.template.loader import get_template

from _database.models import Person, Project, Event, Guilde, MeetingNote, Space, Machine, Consensus, Photo
from _website.tools.space_open import getOpenNowStatus
from _website.tools.tools import make_description_sentence
from _apis.models.search import Search
from secrets import Secret
from config import Config
from log import log


def getLanguage(request):
    if request.GET.get('lang', None):
        return request.GET.get('lang', None)
    elif request.COOKIES.get('lang', None):
        return request.COOKIES.get('lang', None)
    else:
        return 'english'


def get_view_response(request, page, sub_page, hashname):
    context = {
        'view': page+'_view',
        'in_space': True if request.COOKIES.get('in_space') or request.GET.get('in_space', None) == 'True' else False,
        'hash': hashname,
        'ADMIN_URL': Secret('DJANGO.ADMIN_URL').value,
        'user': request.user,
        'language': getLanguage(request),
        'auto_search': request.GET.get('search', None)
    }

    if page == 'landingpage':
        return {**context, **{
            'slug': '/',
            'page_git_url': '/tree/master/_database/templates/landingpage_view.html',
            'page_name': Config('BASICS.NAME').value,
            'page_description': make_description_sentence(),
            'is_open_status': getOpenNowStatus(context['language']),
            'upcoming_events': Event.objects.QUERYSET__upcoming()[:5],
            'photos': Photo.objects.latest()[:33]
        }}

    elif page == 'values':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/tree/master/_database/templates/values_view.html',
            'page_name': Config('BASICS.NAME').value+' | Values',
            'page_description': 'Our values at '+Config('BASICS.NAME').value
        }}

    elif page == 'meetings':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/tree/master/_database/templates/meetings_view.html',
            'page_name': Config('BASICS.NAME').value+' | Meetings',
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
            'page_git_url': '/tree/master/_database/templates/meeting_view.html',
            'page_name': Config('BASICS.NAME').value+' | Meeting | '+selected.text_date,
            'page_description': 'Join our weekly meetings!',
            'selected': selected,
            'next_meeting': Event.objects.QUERYSET__next_meeting(),
            'past_meetings': MeetingNote.objects.past(selected)[:10]
        }}
    elif page == 'meeting_present':
        return {**context, **{
            'slug': '/meeting/present',
            'page_name': Config('BASICS.NAME').value+' | Meeting | Presentation mode',
            'page_description': 'Join our weekly meetings!',
            'current_meeting': MeetingNote.objects.current()
        }}

    elif page == 'guildes':
        all_results = Guilde.objects.all()[:10]
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/tree/master/_database/templates/results_list.html',
            'page_name': Config('BASICS.NAME').value+' | Guildes',
            'page_description': 'Join a guilde at '+Config('BASICS.NAME').value+'!',
            'headline': 'Guildes',
            'description': 'A guilde is ...',
            'wiki_url': None,
            'add_new_requires_user': True,
            'addnew_url': '/{}/_database/guilde/add/'.format(Secret('DJANGO.ADMIN_URL').value),
            'addnew_text': 'Add guilde',
            'all_results': all_results if all_results else True,
            'results_count': Guilde.objects.count(),
            'show_more': page
        }}
    elif page == 'guilde':
        if 'guilde/' not in sub_page:
            sub_page = 'guilde/'+sub_page
        selected = Guilde.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/guilde/'+sub_page,
            'page_git_url': '/tree/master/_database/templates/guilde_view.html',
            'page_name': Config('BASICS.NAME').value+' | Guilde | '+selected.str_name_en_US,
            'page_description': 'Join our weekly meetings!',
            'selected': selected
        }}

    elif page == 'spaces':
        all_results = Space.objects.all()[:10]
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/tree/master/_database/templates/results_list.html',
            'page_name': Config('BASICS.NAME').value+' | Spaces',
            'page_description': Config('BASICS.NAME').value+' has many awesome spaces!',
            'headline': 'Spaces',
            'description': 'At SPACE fellow hackers created all kind of awesome spaces...',
            'wiki_url': None,
            'add_new_requires_user': True,
            'addnew_url': '/{}/_database/space/add/'.format(Secret('DJANGO.ADMIN_URL').value),
            'addnew_text': 'Add space',
            'all_results': all_results if all_results else True,
            'results_count': Space.objects.count(),
            'show_more': page
        }}
    elif page == 'space':
        if 'space/' not in sub_page:
            sub_page = 'space/'+sub_page
        selected = Space.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/space/'+sub_page,
            'page_git_url': '/tree/master/_database/templates/space_view.html',
            'page_name': Config('BASICS.NAME').value+' | Space | '+selected.str_name_en_US,
            'page_description': selected.text_description_en_US,
            'selected': selected
        }}

    elif page == 'machines':
        all_results = Machine.objects.all()[:10]
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/tree/master/_database/templates/results_list.html',
            'page_name': Config('BASICS.NAME').value+' | Machines',
            'page_description': Config('BASICS.NAME').value+' has all kinds of awesome machines!',
            'headline': 'Machines',
            'description': 'We have many useful machines ...',
            'wiki_url': None,
            'add_new_requires_user': True,
            'addnew_url': '/{}/_database/machine/add/'.format(Secret('DJANGO.ADMIN_URL').value),
            'addnew_text': 'Add machine',
            'all_results': all_results if all_results else True,
            'results_count': Machine.objects.count(),
            'show_more': page
        }}
    elif page == 'machine':
        if 'machine/' not in sub_page:
            sub_page = 'machine/'+sub_page
        selected = Machine.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/machine/'+sub_page,
            'page_git_url': '/tree/master/_database/templates/machine_view.html',
            'page_name': Config('BASICS.NAME').value+' | Machine | '+selected.str_name_en_US,
            'page_description': selected.text_description_en_US,
            'selected': selected
        }}

    elif page == 'projects':
        all_results = Project.objects.latest()[:10]
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/tree/master/_database/templates/results_list.html',
            'page_name': Config('BASICS.NAME').value+' | Projects',
            'page_description': 'People at '+Config('BASICS.NAME').value+' created all kinds of awesome projects!',
            'headline': 'Projects',
            'description': 'At SPACE fellow hackers created awesome projects...',
            'wiki_url': None,
            'add_new_requires_user': False,
            'addnew_url': '{}c/projects/'.format(Secret('DISCOURSE.DISCOURSE_URL').value),
            'addnew_text': 'Add project',
            'all_results': all_results if all_results else True,
            'results_count': Project.objects.count(),
            'show_more': page
        }}
    elif page == 'project':
        if 'project/' not in sub_page:
            sub_page = 'project/'+sub_page
        selected = Project.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/project/'+sub_page,
            'page_git_url': '/tree/master/_database/templates/project_view.html',
            'page_name': Config('BASICS.NAME').value+' | Project | '+selected.str_name_en_US,
            'page_description': selected.text_description_en_US,
            'selected': selected
        }}

    elif page == 'consensus':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/tree/master/_database/templates/consensus_view.html',
            'page_name': Config('BASICS.NAME').value+' | Big-C consensus items',
            'page_description': 'When you want to do something that would drastically change '+Config('BASICS.NAME').value+' (or need a lot of money from Noisebridge for a project) - suggest a Big-C consensus item!',
            'all_current_items': Consensus.objects.current(),
            'all_current_items_count': Consensus.objects.current().count(),
            'all_archived_items': Consensus.objects.archived(),
            'all_archived_items_count': Consensus.objects.archived().count(),
        }}

    elif page == 'photos':
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/tree/master/_database/templates/photos_view.html',
            'page_name': Config('BASICS.NAME').value+' | Photos',
            'page_description': 'Explore '+Config('BASICS.NAME').value+'\'s history in photos!',
            'photos': Photo.objects.latest()[:30],
        }}

    elif page == 'events':
        all_results = Event.objects.QUERYSET__upcoming()[:10]
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/tree/master/_database/templates/results_list.html',
            'page_name': Config('BASICS.NAME').value+' | Events',
            'page_description': 'At '+Config('BASICS.NAME').value+' we have all kinds of cool events - organized by your fellow hackers!',
            'headline': 'Events',
            'description': 'SPACE is a place where people come together ...',
            'add_new_requires_user': False,
            'addnew_url': '/event/new',
            'addnew_text': 'Organize an event',
            'addnew_target': 'same_tab',
            'addnew_menu_selected': 'menu_h_events',
            'all_results': all_results if all_results else True,
            'results_count': Event.objects.count(),
            'show_more': page
        }}
    elif page == 'event':
        if 'event/' not in sub_page:
            sub_page = 'event/'+sub_page
        selected = Event.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'slug': '/event/'+sub_page,
            'page_git_url': '/tree/master/_database/templates/event_view.html',
            'page_name': Config('BASICS.NAME').value+' | Event | '+selected.str_name_en_US,
            'page_description': selected.text_description_en_US,
            'selected': selected,
            'photos': Photo.objects.latest()[:33]
        }}
    elif page == 'event_banner':
        if 'event/' not in sub_page:
            sub_page = 'event/'+sub_page
        selected = Event.objects.filter(str_slug=sub_page).first()
        return {**context, **{
            'selected': selected,
        }}
    elif page == 'event_new':
        from django.middleware.csrf import get_token
        EVENTS_SPACE_DEFAULT = Config('EVENTS.EVENTS_SPACE_DEFAULT').value
        return {**context, **{
            'slug': '/'+page,
            'page_git_url': '/tree/master/_database/templates/event_new_view.html',
            'page_name': Config('BASICS.NAME').value+' | New event',
            'page_description': 'Organize an event at '+Config('BASICS.NAME').value,
            'upcoming_events': Event.objects.QUERYSET__upcoming()[:4],
            'default_space': Space.objects.filter(str_name_en_US=EVENTS_SPACE_DEFAULT).first(),
            'all_spaces': Space.objects.exclude(str_name_en_US=EVENTS_SPACE_DEFAULT),
            'all_guildes': Guilde.objects.all(),
            'csrf_token': get_token(request)
        }}


def get_page_response(request, page, sub_page=None):
    log('get_page_response(request,page={},sub_page={})'.format(page, sub_page))
    page = page
    hash_name = request.build_absolute_uri().split(
        '#')[1] if '#' in request.build_absolute_uri() else None

    if page == 'meeting_present':
        html = 'meeting_present.html'
    elif page == 'event_banner':
        html = 'event_banner_view.html'
    else:
        html = 'page.html'

    response = render(request, html, get_view_response(
        request, page, sub_page, hash_name))
    return response


def landingpage_view(request):
    log('landingpage_view(request)')
    return get_page_response(request, 'landingpage')


def values_view(request):
    log('values_view(request)')
    return get_page_response(request, 'values')


def meetings_view(request):
    log('meetings_view(request)')
    return get_page_response(request, 'meetings')


def meeting_present_view(request):
    log('meeting_present_view(request)')
    if not MeetingNote.objects.current():
        return HttpResponseRedirect('/meetings')
    return get_page_response(request, 'meeting_present')


def meeting_view(request, sub_page):
    log('meeting_view(request,sub_page={})'.format(sub_page))
    # if meeting not found, redirect to all meetings page
    if not MeetingNote.objects.filter(text_date=sub_page).exists():
        return HttpResponseRedirect('/meetings')
    return get_page_response(request, 'meeting', sub_page)


def meeting_end_view(request):
    log('meeting_end_view(request)')
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
    log('guildes_view(request)')
    return get_page_response(request, 'guildes')


def guilde_view(request, sub_page):
    log('guilde_view(request, {})'.format(sub_page))
    sub_page = 'guilde/'+sub_page
    # if guilde not found, redirect to all guildes page
    if not Guilde.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/guildes')
    return get_page_response(request, 'guilde', sub_page)


def spaces_view(request):
    log('spaces_view(request)')
    return get_page_response(request, 'spaces')


def space_view(request, sub_page):
    log('space_view(request, {})'.format(sub_page))
    sub_page = 'space/'+sub_page
    # if space not found, redirect to all spaces page
    if not Space.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/spaces')
    return get_page_response(request, 'space', sub_page)


def machines_view(request):
    log('machines_view(request)')
    return get_page_response(request, 'machines')


def machine_view(request, sub_page):
    log('machine_view(request, {})'.format(sub_page))
    sub_page = 'machine/'+sub_page
    # if space not found, redirect to all spaces page
    if not Machine.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/machines')
    return get_page_response(request, 'machine', sub_page)


def projects_view(request):
    log('projects_view(request)')
    return get_page_response(request, 'projects')


def project_view(request, sub_page):
    log('project_view(request, {})'.format(sub_page))
    sub_page = 'project/'+sub_page
    # if space not found, redirect to all spaces page
    if not Project.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/projects')
    return get_page_response(request, 'project', sub_page)


def consensus_view(request):
    log('consensus_view(request)')
    return get_page_response(request, 'consensus')


def photos_view(request):
    log('photos_view(request)')
    return get_page_response(request, 'photos')


def events_view(request):
    log('events_view(request)')
    return get_page_response(request, 'events')


def events_json_view(request):
    log('events_json_view(request)')
    return Event.objects.QUERYSET__upcoming().RESPONSE__JSON()


def event_new_view(request):
    log('event_new_view(request)')
    return get_page_response(request, 'event_new')


def event_banner_view(request, sub_page):
    log('event_banner_view(request)')
    return get_page_response(request, 'event_banner', sub_page)


def event_view(request, sub_page):
    log('event_view(request, {})'.format(sub_page))
    return_json = False
    if sub_page.endswith('.json'):
        log('--> detected .json at end of URL')
        sub_page = sub_page.replace('.json', '')
        return_json = True

    sub_page = 'event/'+sub_page
    # if space not found, redirect to all spaces page
    if not Event.objects.filter(str_slug=sub_page).exists():
        return HttpResponseRedirect('/events')

    # if .json at end of url, return json, else page
    if return_json == True:
        log('--> return JsonResponse')
        return JsonResponse(Event.objects.filter(str_slug=sub_page).first().json_data)

    else:
        return get_page_response(request, 'event', sub_page)


def get_view(request):
    log('get_view(request)')
    in_space = request.COOKIES.get('in_space')
    language = getLanguage(request)
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
                        'language': language,
                        'upcoming_events': Event.objects.QUERYSET__upcoming()[:5]
                    }),
                'marryspeak': marry_messages
            }
        )
    elif request.GET.get('what', None) == 'open_status':
        response = JsonResponse({'html': getOpenNowStatus(language)})

    elif request.GET.get('what', None) == 'event_overlap':
        str_date = request.GET.get('date', None)
        str_time = request.GET.get('time', None)
        str_duration = request.GET.get('duration', None)
        if str_date and str_time and str_duration:
            from _database.views_helper_functions import INT__UNIX_from_date_and_time_STR, INT__duration_minutes

            overlapping_events = Event.objects.JSON__overlapping_events(
                INT__UNIX_from_date_and_time_STR(str_date, str_time),
                INT__duration_minutes(str_duration),
                request.GET.get('space', None),
            )

            response = JsonResponse({
                'int_overlapping_events': len(overlapping_events['overlapping_events']),
                'html': get_template(
                    'components/body/event_new/form_elements/overlapping_events.html').render({
                        'language': getLanguage(request),
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
            'components/body/meetings/current_meeting.html').render({'language': getLanguage(request)}
                                                                    )})

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

    log('--> return response')
    return response


def translate_view(request):
    log('translate_view(request)')
    import json
    import bleach
    from googletrans import Translator
    import emoji
    translator = Translator()

    with open('_database/templates/languages.json') as json_file:
        language_codes = json.load(json_file)

    if request.GET.get('q', None) and request.GET.get('language', None):
        text = emoji.get_emoji_regexp().sub(u'', request.GET.get('q', None))

        response = JsonResponse({'text': translator.translate(
            text=text,
            dest=request.GET.get('language', None)).text
        })

    elif request.GET.get('q', None):
        LANGUAGES = Config('WEBSITE.LANGUAGES').value
        languages = {}

        text = emoji.get_emoji_regexp().sub(u'', request.GET.get('q', None))

        for language in LANGUAGES:
            if len(LANGUAGES) > 1:
                languages[language] = translator.translate(
                    text=text,
                    dest=language_codes[language]).text
            else:
                languages[language] = request.GET.get('q', None)

        response = JsonResponse(languages)

    else:
        response = JsonResponse({'error': 'fields missing'})
        response.status_code = 404

    return response


def load_more_view(request):
    log('load_more_view(request)')
    from _database.models import Helper

    if request.GET.get('what', None) and request.GET.get('from', None):
        if request.GET.get('what', None) == 'meeting_notes':
            response = Helper().JSON_RESPONSE_more_results(
                request, 'meetings/meetings_list.html', MeetingNote.objects.past())
        elif request.GET.get('what', None) == 'events':
            response = Helper().JSON_RESPONSE_more_results(
                request, 'results_list_entries.html', Event.objects.QUERYSET__upcoming())
        elif request.GET.get('what', None) == 'projects':
            response = Helper().JSON_RESPONSE_more_results(
                request, 'results_list_entries.html', Project.objects.latest())
        elif request.GET.get('what', None) == 'spaces':
            response = Helper().JSON_RESPONSE_more_results(
                request, 'results_list_entries.html', Space.objects.all())
        elif request.GET.get('what', None) == 'machines':
            response = Helper().JSON_RESPONSE_more_results(
                request, 'results_list_entries.html', Machine.objects.all())
        elif request.GET.get('what', None) == 'guildes':
            response = Helper().JSON_RESPONSE_more_results(
                request, 'results_list_entries.html', Guilde.objects.all())
        elif request.GET.get('what', None) == 'consensus':
            response = Helper().JSON_RESPONSE_more_results(
                request, 'consensus_items_entries.html', Consensus.objects.latest())
        elif request.GET.get('what', None) == 'photos':
            response = Helper().JSON_RESPONSE_more_photos(request)
    else:
        response = JsonResponse({'error': 'Request incomplete or wrong'})
        response.status_code = 404

    log('--> return response')
    return response


def save_view(request):
    log('save_view(request)')
    if request.GET.get('keyword', None) and request.GET.get('origin', None) and MeetingNote.objects.filter(text_date=request.GET.get('origin', None).split('/')[1]).exists():
        meeting = MeetingNote.objects.filter(
            text_date=request.GET.get('origin', None).split('/')[1]).first()

        meeting.add_keyword(request.GET.get('keyword'))
        response = JsonResponse({'success': True})
    else:
        response = JsonResponse({'error': 'Request incomplete or wrong'})
        response.status_code = 404

    log('--> return response')
    return response


def remove_view(request):
    log('remove_view(request)')
    if request.GET.get('keyword', None) and request.GET.get('origin', None) and MeetingNote.objects.filter(text_date=request.GET.get('origin', None).split('/')[1]).exists():
        meeting = MeetingNote.objects.filter(
            text_date=request.GET.get('origin', None).split('/')[1]).first()

        meeting.remove_keyword(request.GET.get('keyword'))
        response = JsonResponse({'success': True})
    else:
        response = JsonResponse({'error': 'Request incomplete or wrong'})
        response.status_code = 404

    log('--> return response')
    return response


def search_view(request):
    log('search_view(request)')
    language = getLanguage(request)
    search_results = search(request.GET.get('q', None),
                            request.GET.get('filter', None))
    response = JsonResponse(
        {
            'num_results': len(search_results),
            'html': get_template(
                'components/search/search_results.html').render({
                    'language': language,
                    'search_results': search_results
                }) if not request.GET.get('filter', None) else get_template('components/body/event_new/hosts_search_results.html').render({
                    'language': language,
                    'all_hosts': search_results[:4],
                }) if request.GET.get('filter', None) == 'hosts' else get_template('components/body/results_list_entries.html').render({
                    'language': language,
                    'all_results': search_results[:4],
                }),
        }
    )

    log('--> return response')
    return response


def new_view(request):
    log('new_view(request)')

    if request.method == 'GET' and request.GET.get('what', None) == 'meeting':
        new_meeting = MeetingNote()
        new_meeting.save()

        response = JsonResponse(
            {
                'html': get_template(
                    'components/body/meetings/current_meeting.html').render({
                        'language': getLanguage(request),
                        'current_meeting': new_meeting
                    })
            }
        )

    elif request.method == 'POST' and request.POST.get('what', None) == 'event':
        from _apis.slack import message
        from _database.views_helper_functions import INT__UNIX_from_date_and_time_STR, INT__duration_minutes

        DOMAIN = Config('WEBSITE.DOMAIN').value

        int_UNIXtime_event_start = INT__UNIX_from_date_and_time_STR(
            request.POST.get('date', None), request.POST.get('time', None))
        int_minutes_duration = INT__duration_minutes(
            request.POST.get('duration', None))

        try:
            if request.FILES['images[0]'].content_type == 'image/jpeg' or request.FILES['images[0]'].content_type == 'image/png':
                image = request.FILES['images[0]']
            else:
                image = None
        except:
            image = None

        uploaded_photo_url = request.POST.get('photo', None)

        new_event = Event(
            boolean_approved=request.user.is_authenticated,
            str_name_en_US=request.POST.get('name_english', None),
            str_name_he_IL=request.POST.get('name_hebrew', None),
            int_UNIXtime_event_start=int_UNIXtime_event_start,
            int_minutes_duration=int_minutes_duration,
            int_UNIXtime_event_end=int_UNIXtime_event_start +
            (60*int_minutes_duration),
            url_featured_photo=uploaded_photo_url if 'https' in uploaded_photo_url else None,
            image_featured_photo=image,
            text_description_en_US=request.POST.get(
                'description_english', None),
            text_description_he_IL=request.POST.get(
                'description_hebrew', None),
            one_space=Space.objects.QUERYSET__by_name(
                request.POST.get('space', None)),
            one_guilde=Guilde.objects.QUERYSET__by_name(
                request.POST.get('guilde', None)),
            str_crowd_size=request.POST.get('expected_crowd', None),
            str_welcomer=request.POST.get('event_welcomer', None),
            boolean_looking_for_volunteers=True if request.POST.get(
                'volunteers', None) == 'yes' else False
        )
        if request.POST.get('location', None):
            if request.POST.get('location', None) != Config('BASICS.NAME').value:
                new_event.str_location = request.POST.get('location', None)
        if request.POST.get('repeating', None):
            # if repeating, mark as such and auto generate new upcoming events with "update_database" command
            str_repeating_how_often = request.POST.get('repeating', None)
            str_repeating_up_to = request.POST.get('repeating_up_to', None)

            if str_repeating_how_often and str_repeating_how_often != '':
                new_event.int_series_startUNIX = new_event.int_UNIXtime_event_start
                new_event.str_series_repeat_how_often = str_repeating_how_often

            if str_repeating_up_to and str_repeating_up_to != '':
                new_event.int_series_endUNIX = INT__UNIX_from_date_and_time_STR(
                    str_repeating_up_to, request.POST.get('time', None))

        new_event.save()

        hosts = request.POST.get('hosts', None)
        if hosts:
            if hosts.startswith(','):
                hosts = hosts[1:]
            hosts = hosts.split(',')
            for host in hosts:
                new_event.many_hosts.add(Person.objects.by_url_discourse(host))

        # if loggedin user: share event to other platforms (Meetup, Discourse, etc.)
        if request.user.is_authenticated:
            new_event.create_discourse_event()
            new_event.create_meetup_event()

        # else (if event created via live website) inform via slack about new event and give community chance to delete it or confirm it
        elif 'HTTP_HOST' in request.META and request.META['HTTP_HOST'] == DOMAIN:
            message(
                'A website visitor created a new event via our website.\n' +
                'If no one deletes it within the next 24 hours, it will be automatically published and appears in our website search'+(', meetup group' if Secret('MEETUP.ACCESS_TOKEN').value else '')+(' and discourse' if Secret('DISCOURSE.API_KEY').exists == True else '')+'.\n' +
                '🚫-> Does this event already exist or is it spam? Open on the following event link and click "Delete event".\n' +
                '✅-> You have a user account for our website and want to publish the event directly? Open on the following event link and click "Approve event".\n' +
                'https://'+DOMAIN+'/'+new_event.str_slug
            )
        else:
            log('--> Request not sent via hackerspace domain. Skipped notifying via Slack.')

        # if event is repeating, create upcoming instances
        new_event = new_event.create_upcoming_instances()

        # if user is signed in and event autoapproved - direct to event page, else show info
        response = JsonResponse(
            {
                'url_next': '/'+new_event.str_slug
            }
        )

    log('--> return response')
    return response


def upload_view(request, what):
    log('upload_view(request,what={})'.format(what))

    if what == 'event-image':
        if request.FILES['images[0]'].content_type != 'image/jpeg' and request.FILES['images[0]'].content_type != 'image/png':
            response = JsonResponse({
                'notification': get_template('components/notification.html').render({
                    'text_message': 'Please upload a JPG or PNG image.',
                    'str_icon': 'error'
                })})
            response.status_code = 500

        else:
            from _apis.models import Aws

            image_s3_url = Aws().upload(request.FILES['images[0]'])

            if image_s3_url:
                response = JsonResponse({'url_image': image_s3_url})
            else:
                log('--> AWS secrets are missing. Couldnt upload image.')
                response = JsonResponse({'url_image': None})

    log('--> return response')
    return response


def approve_event_view(request):
    log('approve_event_view(request)')

    if request.user.is_authenticated == False:
        log('--> Failed: User not logged in')
        response = JsonResponse({'success': False})
        response.status_code = 403
    elif not request.GET.get('str_slug', None) or Event.objects.filter(boolean_approved=False, str_slug=request.GET.get('str_slug', None)).exists() == False:
        log('--> Failed: Result not found')
        response = JsonResponse({'success': False})
        response.status_code = 404
    else:
        from _apis.slack import message

        DOMAIN = Config('WEBSITE.DOMAIN').value
        # approve event and all upcoming ones
        event = Event.objects.filter(
            boolean_approved=False, str_slug=request.GET.get('str_slug', None)).first()

        upcoming_events = Event.objects.filter(
            boolean_approved=False, str_name_en_US=event.str_name_en_US).all()
        log('--> Approve all upcoming events')
        for event in upcoming_events:
            event.publish()

        # notify via slack that event was approved and by who
        if 'HTTP_HOST' in request.META and request.META['HTTP_HOST'] == DOMAIN:
            message('✅'+str(request.user)+' approved the event "' +
                    event.str_name_en_US+'":\nhttps://'+DOMAIN+'/'+event.str_slug)

        response = JsonResponse({'success': True})
        response.status_code = 200

    log('--> return response')
    return response


def delete_event_view(request):
    log('delete_event_view(request)')

    if not request.GET.get('str_slug', None) or Event.objects.filter(str_slug=request.GET.get('str_slug', None)).exists() == False:
        log('--> Failed: Result not found')
        response = JsonResponse({'success': False})
        response.status_code = 404
    else:
        from _apis.slack import message

        # approve event and all upcoming ones
        event = Event.objects.filter(
            str_slug=request.GET.get('str_slug', None)).first()

        log('--> Delete all upcoming events')
        event.delete_series()

        # notify via slack that event was deleted and by who
        if 'HTTP_HOST' in request.META and request.META['HTTP_HOST'] == Config('WEBSITE.DOMAIN').value:
            message('🚫'+str(request.user)+' deleted the event "' +
                    event.str_name_en_US+'"')

        response = JsonResponse({'success': True})
        response.status_code = 200

    log('--> return response')
    return response


def logout_view(request):
    from django.contrib.auth import logout
    from django.shortcuts import redirect

    logout(request)
    return redirect('/')


def handler404(request, exception, template_name="404.html"):
    from django.shortcuts import redirect
    return redirect('/?search='+request.path[1:])
