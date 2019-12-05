def get_config(name):
    try:
        import json
        import os
        from hackerspace.settings import BASE_DIR
        file_path = os.path.join(BASE_DIR, 'config.json')

        with open(file_path) as json_file:
            selected = json.load(json_file)

        path = name.split('.')
        for part in path:
            selected = selected[part]

        return selected
    except:
        return None
