from django.urls import path
from _apis.views.hackspace_os_api_view import HackspaceOSapiView
from _apis.views.hackspaces_org_api_view import HackspacesORGapiView

urlpatterns = [
    path('apis/hackspace_os/page/<str:sub_page>',
         HackspaceOSapiView.as_view(path='page'), name='page'),
]

handler404 = '_database.views.handler404'
