from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.wiki import wiki_search
from hackerspace.models import Event
from django.db.models import Q
from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_SOCIAL_NETWORKS


def search(query):
    if not query:
        return []

    # search in social network accounts
    networks = [x for x in HACKERSPACE_SOCIAL_NETWORKS if query.lower()
                in x['name'].lower()]

    # search in database
    events = Event.objects.filter(
        Q(str_name__icontains=query) | Q(text_description__icontains=query)
    ).upcoming().search_results()[:5]

    # search in wiki
    wiki_search_results = wiki_search(query)

    return networks+events+wiki_search_results[:7]
