from django.http import HttpResponse
from django.views import View


class MachinesView(View):
    greeting = "Good Day"

    def get(self, request):
        return HttpResponse(self.greeting)
