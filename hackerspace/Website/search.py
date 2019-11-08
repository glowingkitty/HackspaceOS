from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.wiki import wiki_search
from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.discuss import discuss_search
from hackerspace.models import Event, MeetingNote, Guilde
from django.db.models import Q
from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_SOCIAL_NETWORKS, HACKERSPACE_INTERNAL_COMMUNICATION_PLATFORMS


def search(query):
    if not query:
        return []

    # search in social network accounts
    networks = [{
        'icon': x['name'].lower(),
        'name': x['name'],
        'url': x['url'],
    } for x in HACKERSPACE_SOCIAL_NETWORKS if query.lower()
        in x['name'].lower()]
    internchannels = [{
        'icon': x['name'].lower(),
        'name': x['name'],
        'url': x['url'],
    } for x in HACKERSPACE_INTERNAL_COMMUNICATION_PLATFORMS if query.lower()
        in x['name'].lower()]

    # search in database
    events = Event.objects.filter(
        Q(str_name__icontains=query) | Q(text_description__icontains=query)
    ).upcoming().search_results()[:5]

    meeting_notes = MeetingNote.objects.filter(
        Q(text_date__icontains=query) | Q(text_keywords__icontains=query)
    ).past().search_results()[:5]

    guildes = Guilde.objects.filter(
        Q(str_name__icontains=query) | Q(text_description__icontains=query)
    ).search_results()[:5]

    # search in wiki
    wiki_search_results = wiki_search(query)

    # search in discuss
    discuss_search_results = discuss_search(query)

    return networks+internchannels+events+guildes+meeting_notes+wiki_search_results+discuss_search_results
