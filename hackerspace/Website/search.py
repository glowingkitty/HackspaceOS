from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.wiki import wiki_search
from hackerspace.APIs.discourse import discourse_search
from hackerspace.models import Event, MeetingNote, Guilde, Machine, Space, Consensus, Project, Person
from django.db.models import Q


def search(query, filter_name):
    from getConfig import get_config

    if not query:
        return []

    if filter_name and filter_name == 'hosts':
        return Person.objects.filter(Q(str_name_en_US__icontains=query) | Q(url_discourse__icontains=query))

    # search in database
    events = Event.objects.filter(
        Q(boolean_approved=True) &
        (
            Q(str_name_en_US__icontains=query) | Q(
                text_description_en_US__icontains=query)
        )
    ).QUERYSET__upcoming()

    if filter_name == 'events':
        return events
    else:
        events = events.LIST__search_results()[:5]

    # search in social network accounts
    networks = [{
        'icon': x['name'].lower(),
        'name': x['name'],
        'url': x['url'],
    } for x in get_config('SOCIAL.SOCIAL_NETWORKS') if query.lower()
        in x['name'].lower()]
    internchannels = [{
        'icon': x['name'].lower(),
        'name': x['name'],
        'url': x['url'],
    } for x in get_config('SOCIAL.INTERNAL_COMMUNICATION_PLATFORMS') if query.lower()
        in x['name'].lower()]

    meeting_notes = MeetingNote.objects.filter(
        Q(text_date__icontains=query) | Q(text_keywords__icontains=query)
    ).past().LIST__search_results()[:5]

    guildes = Guilde.objects.filter(
        Q(str_name_en_US__icontains=query) | Q(
            text_description_en_US__icontains=query)
    ).LIST__search_results()[:5]

    machines = Machine.objects.filter(
        Q(str_name_en_US__icontains=query) | Q(
            text_description_en_US__icontains=query)
    ).LIST__search_results()[:5]

    spaces = Space.objects.filter(
        Q(str_name_en_US__icontains=query) | Q(
            text_description_en_US__icontains=query)
    ).LIST__search_results()[:5]

    consensus_items = Consensus.objects.filter(
        Q(str_name_en_US__icontains=query) | Q(
            text_description_en_US__icontains=query)
    ).LIST__search_results()[:5]

    projects = Project.objects.filter(
        Q(str_name_en_US__icontains=query) | Q(
            text_description_en_US__icontains=query)
    ).LIST__search_results()[:5]

    # search in wiki
    try:
        wiki_search_results = wiki_search(query)
    except:
        print('wiki search failed')
        wiki_search_results = []

    # search in discourse
    try:
        discourse_search_results = discourse_search(query)
    except:
        print('discourse search failed')
        discourse_search_results = []

    return networks+internchannels+events+guildes+machines+spaces+meeting_notes+consensus_items+projects+wiki_search_results+discourse_search_results
