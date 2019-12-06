import requests
from hackerspace.models import MeetingNote


def wiki_search(query, limit=5):
    from getConfig import get_config
    if not get_config('BASICS.WIKI.API_URL'):
        print('LOG: --> BASICS.WIKI.API_URL not found in config.json -> BASICS - Please add your WIKI_API_URL first.')
        return []

    # search in the Noisebridge wiki -> returns the search suggestions of the mini search bar on the top right
    response_json = requests.get(get_config('BASICS.WIKI.API_URL')+'?action=opensearch&format=json&formatversion=2&search=' +
                                 query+'&namespace=0&limit='+str(limit)+'&suggest=true').json()

    result_names = response_json[1]
    result_urls = response_json[3]

    results = []
    for idx, val in enumerate(result_names):
        results.append({
            'icon': 'wiki',
            'name': val,
            'url': result_urls[idx]
        })

    return results


def save_from_wiki__meeting(url):
    # save the archived meeting notes into our database
    date = ''
    text = ''

    MeetingNote(
        int_UNIXtime_created='',
        text_notes=text
    ).save()
