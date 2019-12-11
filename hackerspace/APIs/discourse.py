import requests
from getKey import STR__get_key, BOOLEAN__key_exists
from hackerspace.log import log
# see Discourse API - https://docs.discourse.org/

DISCOURSE_URL = STR__get_key('DISCOURSE.DISCOURSE_URL')


def discourse_search(query, limit=5):
    log('discourse_search()')
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


def BOOLEAN__API_access_works():
    log('BOOLEAN__API_access_works()')
    if BOOLEAN__key_exists('DISCOURSE.API_KEY') == False:
        log('--> Failed: DISCOURSE.API_KEY not set')
        return None

    response = requests.get(DISCOURSE_URL+'notifications.json',
                            headers={
                                'content-type': 'multipart/form-data'
                            }, params={
                                'api_key': STR__get_key('DISCOURSE.API_KEY'),
                                'api_username': STR__get_key('DISCOURSE.API_USERNAME'),
                            })
    if response.status_code == 200:
        return True
    else:
        print(response.status_code)
        print(response.json())
        return False


def create_category(name):
    log('create_category()')
    response_json = requests.post(DISCOURSE_URL+'categories.json', json={
        'name': name,
    }).json()
    print(response_json)


def create_post(str_headline, str_text, str_category):
    log('create_post()')
    if BOOLEAN__key_exists('DISCOURSE.API_KEY') == False:
        log('--> Failed: DISCOURSE.API_KEY not set')
        return None

    response = requests.post(DISCOURSE_URL+'posts.json',
                             headers={
                                 'content-type': 'application/json'
                             }, params={
                                 'api_key': STR__get_key('DISCOURSE.API_KEY'),
                                 'api_username': STR__get_key('DISCOURSE.API_USERNAME'),
                                 'title': str_headline,
                                 'raw': str_text,
                                 'category': get_category_id(str_category)
                                 # TODO add event details
                                 #  'event': {'start': '2019-12-13T15:00:00+00:00', 'end': '2019-12-13T19:00:00+00:00'}
                             })
    if response.status_code == 200:
        return DISCOURSE_URL+'/t/'+str(response.json()['id'])
    else:
        print(response.status_code)
        print(response.json())


def delete_post(post_url):
    log('delete_post()')
    if BOOLEAN__key_exists('DISCOURSE.API_KEY') == False:
        log('--> Failed: DISCOURSE.API_KEY not set')
        return None

    # get ID of post
    response = requests.get(post_url)
    if response.status_code != 200:
        log('--> Couldn\'t find post on Discourse. Skipped deleting.')
        return False
    topic_id = response.url.split('/')[-1]

    response = requests.delete(DISCOURSE_URL+'/t/'+topic_id+'.json',
                               headers={
                                   'content-type': 'application/json'
                               }, params={
                                   'api_key': STR__get_key('DISCOURSE.API_KEY'),
                                   'api_username': STR__get_key('DISCOURSE.API_USERNAME')
                               })
    if response.status_code == 200:
        log('--> Deleted')
        return True
    else:
        log('--> Not deleted')
        print(response.status_code)
        print(response.json())
        return False


def get_categories(output='list'):
    log('get_categories()')
    response = requests.get(
        DISCOURSE_URL+'categories.json', headers={'Accept': 'application/json'})
    if output == 'list' and response.status_code == 200:
        return [x['slug'] for x in response.json()['category_list']['categories']]
    else:
        return response.json()


def get_category_id(str_name_en_US):
    categories = get_categories(output='json')['category_list']['categories']
    for category in categories:
        if category['name'] == str_name_en_US or category['slug'] == str_name_en_US:
            return category['id']
    else:
        return None


def get_category_posts(category, all_pages=False):
    log('get_category_posts()')
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
    log('get_post_details()')
    response_json = requests.get(
        DISCOURSE_URL+'t/'+slug+'.json', headers={'Accept': 'application/json'})
    return response_json.json()['post_stream']['posts'][0]


def get_users(sort='days_visited'):
    log('get_users()')
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
