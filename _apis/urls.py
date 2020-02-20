from django.urls import path
from _apis.views.hackspace_os_api_view import HackspaceOSapiView
from _apis.views.hackspaces_org_api_view import HackspacesORGapiView

urlpatterns = [
    path('get/', HackspaceOSapiView.as_view(), name='get'),
    path('translate', HackspaceOSapiView.as_view(), name='translate'),
    path('load_more', HackspaceOSapiView.as_view(), name='load_more'),
    path('save', HackspaceOSapiView.as_view(), name='save'),
    path('remove', HackspaceOSapiView.as_view(), name='remove'),
    path('search', HackspaceOSapiView.as_view(), name='search'),
    path('new', HackspaceOSapiView.as_view(), name='search'),
    path('upload/<str:what>', HackspaceOSapiView.as_view(), name='upload'),

    path('approve-event', HackspaceOSapiView.as_view(), name='approve-event'),
    path('delete-event', HackspaceOSapiView.as_view(), name='delete-event'),

    path('logout', HackspaceOSapiView.as_view(), name='logout'),

    path('events.json', HackspacesORGapiView.as_view(), name='events_json')
]

handler404 = '_database.views.handler404'
