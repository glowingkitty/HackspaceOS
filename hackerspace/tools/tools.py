import re
TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def make_description_sentence():
    from getConfig import get_config
    HACKERSPACE_IS_SENTENCES = get_config('BASICS.HACKERSPACE_IS_SENTENCES')
    return get_config('BASICS.NAME')+' '+remove_tags(HACKERSPACE_IS_SENTENCES['english'][0])+('.' if not remove_tags(HACKERSPACE_IS_SENTENCES['english'][0]).endswith('.') else '')
