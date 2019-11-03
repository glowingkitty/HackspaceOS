import requests
from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_DISCUSS_URL


def discuss_search(query, limit=5):
    results = []
    response_json = requests.get(
        HACKERSPACE_DISCUSS_URL+'/search/query.json?term='+query).json()
    if 'topics' in response_json:
        for post in response_json['topics']:
            results.append({
                'icon': 'discuss',
                'name': post['title'],
                'url': HACKERSPACE_DISCUSS_URL+'/t/'+str(post['id'])
            })

    return results
