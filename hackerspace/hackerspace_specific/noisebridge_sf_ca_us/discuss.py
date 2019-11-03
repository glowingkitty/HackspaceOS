import requests


def discuss_search(query, limit=5):
    results = []
    response_json = requests.get(
        'https://discuss.noisebridge.info/search/query.json?term='+query).json()
    if 'topics' in response_json:
        for post in response_json['topics']:
            results.append({
                'icon': 'discuss',
                'name': post['title'],
                'url': 'https://discuss.noisebridge.info/t/'+str(post['id'])
            })

    return results
