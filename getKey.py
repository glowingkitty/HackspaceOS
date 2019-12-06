def STR__get_key(name):
    try:
        import json
        import os
        from hackerspace.settings import BASE_DIR
        file_path = os.path.join(BASE_DIR, 'secrets.json')

        with open(file_path) as json_file:
            selected = json.load(json_file)

        path = name.split('.')
        for part in path:
            selected = selected[part]

        return selected
    except:
        return None


def BOOLEAN__key_exists(name):
    if STR__get_key(name):
        return True
    else:
        return False
