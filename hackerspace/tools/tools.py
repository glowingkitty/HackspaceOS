import re
from hackerspace.YOUR_HACKERSPACE import HACKERSPACE_NAME, HACKERSPACE_IS_SENTENCES
TAG_RE = re.compile(r'<[^>]+>')


def remove_tags(text):
    return TAG_RE.sub('', text)


def make_description_sentence():
    return HACKERSPACE_NAME+' '+remove_tags(HACKERSPACE_IS_SENTENCES[0])+('.' if not remove_tags(HACKERSPACE_IS_SENTENCES[0]).endswith('.') else '')
