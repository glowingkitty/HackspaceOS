import requests
from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_DISCOURSE_URL
from pprint import pprint
# see Discourse API - https://docs.discourse.org/


def discourse_search(query, limit=5):
    print('discourse_search()')
    results = []
    response_json = requests.get(
        HACKERSPACE_DISCOURSE_URL+'/search/query.json?term='+query).json()
    if 'topics' in response_json:
        for post in response_json['topics']:
            results.append({
                'icon': 'discourse',
                'name': post['title'],
                'url': HACKERSPACE_DISCOURSE_URL+'/t/'+str(post['id'])
            })

    return results


def create_category(name):
    print('create_category()')
    response_json = requests.post(HACKERSPACE_DISCOURSE_URL+'categories.json', json={
        "name": name,
    }).json()
    print(response_json)


def get_categories():
    print('get_categories()')
    response_json = requests.get(
        HACKERSPACE_DISCOURSE_URL+'categories.json', headers={'Accept': 'application/json'}).json()
    return [x['slug'] for x in response_json['category_list']['categories']]


def get_category_posts(category, all_pages=False):
    print('get_category_posts()')
    response_json = requests.get(
        HACKERSPACE_DISCOURSE_URL+'c/'+category+'.json', headers={'Accept': 'application/json'}).json()
    if all_pages == True:
        results = response_json['topic_list']['topics']
        page = 1

        while len(response_json['topic_list']['topics']) > 0:
            response_json = requests.get(HACKERSPACE_DISCOURSE_URL+'c/'+category +
                                         '.json?page='+str(page), headers={'Accept': 'application/json'}).json()
            results += response_json['topic_list']['topics']
            page += 1

        return results

    return response_json['topic_list']['topics']


def get_users(sort='days_visited'):
    print('get_users()')
    results = []
    response_json = requests.get(
        HACKERSPACE_DISCOURSE_URL+'/directory_items.json?period={}&order={}'.format('all', sort), headers={'Accept': 'application/json'}).json()
    results += response_json['directory_items']

    page = 1
    while len(response_json['directory_items']) > 0:
        response_json = requests.get(
            HACKERSPACE_DISCOURSE_URL+'/directory_items.json?page={}&period={}&order={}'.format(page, 'all', sort), headers={'Accept': 'application/json'}).json()
        results += response_json['directory_items']
        page += 1

    return results
