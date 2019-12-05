import requests
from getKey import STR__get_key, BOOLEAN__key_exists
# see Discourse API - https://docs.discourse.org/

DISCOURSE_URL = STR__get_key('DISCOURSE.DISCOURSE_URL')


def discourse_search(query, limit=5):
    print('LOG: discourse_search()')
    results = []
    response_json = requests.get(
        DISCOURSE_URL+'/search/query.json?term='+query).json()
    if 'topics' in response_json:
        for post in response_json['topics']:
            results.append({
                'icon': 'discourse',
                'name': post['title'],
                'url': DISCOURSE_URL+'/t/'+str(post['id'])
            })

    return results


def create_category(name):
    print('LOG: create_category()')
    response_json = requests.post(DISCOURSE_URL+'categories.json', json={
        "name": name,
    }).json()
    print(response_json)


def create_post(str_headline, str_text, str_category):
    # TODO test with API key
    print('LOG: create_post()')
    if BOOLEAN__key_exists('DISCOURSE.API_KEY') == False:
        print('LOG: --> Failed: DISCOURSE.API_KEY not set')
        return None

    import random
    response = requests.post(DISCOURSE_URL+'posts.json',
                             headers={
                                 'content-type': 'application/json'
                             }, json={
                                 "Api-Key": STR__get_key('DISCOURSE.API_KEY'),
                                 "Api-Username": STR__get_key('DISCOURSE.API_USERNAME'),
                                 "title": str_headline,
                                 "topic_id": random.randint(3000, 9000),
                                 "raw": str_text,
                                 "category": str_category
                             })
    if response.status_code == 200:
        return DISCOURSE_URL+'/t/'+str(response.json()['id'])
    else:
        print(response.status_code)
        print(response.json())


def get_categories():
    print('LOG: get_categories()')
    response_json = requests.get(
        DISCOURSE_URL+'categories.json', headers={'Accept': 'application/json'}).json()
    return [x['slug'] for x in response_json['category_list']['categories']]


def get_category_posts(category, all_pages=False):
    print('LOG: get_category_posts()')
    response_json = requests.get(
        DISCOURSE_URL+'c/'+category+'.json', headers={'Accept': 'application/json'}).json()
    if all_pages == True:
        results = response_json['topic_list']['topics']
        page = 1

        while len(response_json['topic_list']['topics']) > 0:
            response_json = requests.get(DISCOURSE_URL+'c/'+category +
                                         '.json?page='+str(page), headers={'Accept': 'application/json'}).json()
            results += response_json['topic_list']['topics']
            page += 1

        return results

    return response_json['topic_list']['topics']


def get_post_details(slug):
    print('LOG: get_post_details()')
    response_json = requests.get(
        DISCOURSE_URL+'t/'+slug+'.json', headers={'Accept': 'application/json'})
    return response_json.json()['post_stream']['posts'][0]


def get_users(sort='days_visited'):
    print('LOG: get_users()')
    results = []
    response_json = requests.get(
        DISCOURSE_URL+'/directory_items.json?period={}&order={}'.format('all', sort), headers={'Accept': 'application/json'}).json()
    results += response_json['directory_items']

    page = 1
    while len(response_json['directory_items']) > 0:
        response_json = requests.get(
            DISCOURSE_URL+'/directory_items.json?page={}&period={}&order={}'.format(page, 'all', sort), headers={'Accept': 'application/json'}).json()
        results += response_json['directory_items']
        page += 1

    return results
