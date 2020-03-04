from django.urls import path
from _apis.views.hackspace_os_api_view import HackspaceOSapiView
from _apis.views.hackspaces_org_api_view import HackspacesORGapiView

urlpatterns = [
    path('apis/hackspace_os/page/<str:sub_page>',
         HackspaceOSapiView.as_view(path='page'), name='page'),
    path('apis/hackspace_os/load_more/<str:sub_page>',
         HackspaceOSapiView.as_view(path='load_more'), name='load_more'),
    path('apis/hackspace_os/open_status',
         HackspaceOSapiView.as_view(path='open_status'), name='open_status'),
    path('apis/hackspace_os/translate',
         HackspaceOSapiView.as_view(path='translate'), name='translate'),
    path('apis/hackspace_os/search',
         HackspaceOSapiView.as_view(path='search'), name='search'),
    path('apis/hackspace_os/image/upload',
         HackspaceOSapiView.as_view(path='image_upload'), name='image_upload'),

    path('apis/hackspace_os/keyword/remove',
         HackspaceOSapiView.as_view(path='keyword_remove'), name='keyword_remove'),
    path('apis/hackspace_os/keyword/save',
         HackspaceOSapiView.as_view(path='keyword_add'), name='keyword_add'),

    path('apis/hackspace_os/events/slider',
         HackspaceOSapiView.as_view(path='events_slider'), name='events_slider'),
    path('apis/hackspace_os/event/create',
         HackspaceOSapiView.as_view(path='event_create'), name='event_create'),
    path('apis/hackspace_os/event/approve',
         HackspaceOSapiView.as_view(path='event_approve'), name='event_approve'),
    path('apis/hackspace_os/event/delete',
         HackspaceOSapiView.as_view(path='event_delete'), name='event_approve'),
    path('apis/hackspace_os/event/overlap',
         HackspaceOSapiView.as_view(path='event_overlap'), name='event_overlap'),

    path('apis/hackspace_os/meeting/duration',
         HackspaceOSapiView.as_view(path='meeting_duration'), name='meeting_duration'),
    path('apis/hackspace_os/meeting/create',
         HackspaceOSapiView.as_view(path='meeting_create'), name='meeting_create'),
    path('apis/hackspace_os/meeting/end',
         HackspaceOSapiView.as_view(path='meeting_end'), name='meeting_end')
]

handler404 = '_database.views.handler404'
