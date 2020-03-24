import sys
from os import listdir
from os.path import isfile, join

from django.template import Library

register = Library()


@register.filter
def getCSSfiles(placeholder):
    css_files = [f.replace('.css', '') for f in listdir(join(
        sys.path[0].split('HackspaceOS')[0]+'HackspaceOS', '_website/static/css')) if isfile(join(join(
            sys.path[0].split('HackspaceOS')[0]+'HackspaceOS', '_website/static/css'), f))]
    return css_files


@register.filter
def getCSSpath(filename):
    return 'css/'+filename+'.css'


@register.filter
def image_exists(filename):
    return isfile(join(sys.path[0].split('HackspaceOS')[0]+'HackspaceOS', '_website/static/images/'+filename))
