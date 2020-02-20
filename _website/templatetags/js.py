import sys
from django.template import Library
from os import listdir
from os.path import isfile, join
register = Library()


@register.filter
def getJSfiles(placeholder):
    js_files = [f.replace('.js', '') for f in listdir(join(
        sys.path[0], '_database/static/js')) if isfile(join(join(
            sys.path[0], '_database/static/js'), f))]
    return js_files


@register.filter
def getJSpath(filename):
    return 'js/'+filename+'.js'
