import re
TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def make_description_sentence():
    from config import Config
    HACKERSPACE_IS_SENTENCES = Config('BASICS.HACKERSPACE_IS_SENTENCES').value
    return Config('BASICS.NAME').value+' '+remove_tags(HACKERSPACE_IS_SENTENCES['english'][0])+('.' if not remove_tags(HACKERSPACE_IS_SENTENCES['english'][0]).endswith('.') else '')
