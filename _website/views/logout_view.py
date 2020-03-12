from django.contrib.auth import logout
from django.shortcuts import redirect
from _website.views.view import View


class LogoutView(View):
    def get(self, request):
        self.log('LogoutView.get()')
        logout(request)
        return redirect('/')
