def STR__get_key(name):
    try:
        import json

        with open('config.json') as json_file:
            selected = json.load(json_file)

        path = name.split('.')
        for part in path:
            selected = selected[part]

        return selected
    except:
        return None
