from django.shortcuts import redirect
from _website.views.view import View


def handler404(request, exception, template_name="404.html"):
    return redirect('/?search='+request.path[1:])
