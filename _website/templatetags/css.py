import sys
from django.template import Library
from os import listdir
from os.path import isfile, join
register = Library()


@register.filter
def getCSSfiles(placeholder):
    css_files = [f.replace('.css', '') for f in listdir(join(
        sys.path[0], '_database/static/css')) if isfile(join(join(
            sys.path[0], '_database/static/css'), f))]
    return css_files


@register.filter
def getCSSpath(filename):
    return 'css/'+filename+'.css'


@register.filter
def image_exists(filename):
    return isfile(join(sys.path[0], '_database/static/images/'+filename))
