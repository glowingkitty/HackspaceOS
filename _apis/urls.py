from django.urls import path
from _apis.views.hackspace_os_api_view import HackspaceOSapiView
from _apis.views.hackspaces_org_api_view import HackspacesORGapiView

urlpatterns = [
    path('apis/hackspace_os/page/<str:sub_page>',
         HackspaceOSapiView.as_view(path='page'), name='page'),
    path('apis/hackspace_os/load_more/<str:sub_page>',
         HackspaceOSapiView.as_view(path='load_more'), name='load_more'),
    path('apis/hackspace_os/events_slider',
         HackspaceOSapiView.as_view(path='events_slider'), name='events_slider'),
    path('apis/hackspace_os/open_status',
         HackspaceOSapiView.as_view(path='open_status'), name='open_status'),
    path('apis/hackspace_os/event_overlap',
         HackspaceOSapiView.as_view(path='event_overlap'), name='event_overlap'),
]

handler404 = '_database.views.handler404'
