def STR__get_key(name):
    try:
        from config import SECRETS

        selected = SECRETS
        path = name.split('.')
        for part in path:
            selected = selected[part]

        return selected
    except:
        return None
