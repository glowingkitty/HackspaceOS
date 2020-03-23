from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from django.views.generic.base import RedirectView

from _apis.urls import urlpatterns as api_urls
from _setup.models import Config, Log, Secret, Setup
from _website import views

# Check once on starting the server
# Check if setup is completed
if not Setup().complete:
    Setup()._menu()
elif not Setup().database_exists:
    from django.core.management import call_command
    call_command('migrate')
    call_command('update_database')

# ask if user is sure about running server in TEST mode?
MODE = Config('MODE.SELECTED').value
if MODE != 'PRODUCTION':
    Log().show_message('MODE in _setup/config.json is set to TESTING - this makes your server easy to attack, if you use that option on a deployed server that is accessible via the internet. Do you want to continue? (Enter Y to continue)')
    are_you_sure = input()
    if are_you_sure.lower() != 'y':
        Log().show_message(
            'Ok, stopped server. You can change the mode in your _setup/config.json file.')
        exit()

urlpatterns = [
    path(Secret('DJANGO.ADMIN_URL').value+'/', admin.site.urls),
    path('', views.LandingpageView.as_view(), name='landingpage'),

    path('values', views.ValuesView.as_view(), name='values'),
    path('values/', RedirectView.as_view(
         url='values', permanent=False), name='values/'),
    path('ourvalues', RedirectView.as_view(
        url='values', permanent=False), name='ourvalues/'),
    path('ourvalues/', RedirectView.as_view(
        url='values', permanent=False), name='ourvalues'),

    path('meetings', views.MeetingsView.as_view(path='all'), name='meetings'),
    path('meeting', RedirectView.as_view(
         url='meetings', permanent=False), name='meeting'),
    path('meetings/', RedirectView.as_view(
         url='meetings', permanent=False), name='meetings/'),
    path('meeting/', RedirectView.as_view(
        url='meetings', permanent=False), name='meeting/'),
    path('meeting/present', views.MeetingsView.as_view(path='present'),
         name='meeting_present_view'),
    path('meeting/<str:sub_page>', views.MeetingsView.as_view(path='result'),
         name='meeting_present_view'),

    path('guildes', views.GuildesView.as_view(path='all'), name='guildes'),
    path('guilde/<str:sub_page>', views.GuildesView.as_view(path='result'),
         name='guilde_view'),

    path('spaces', views.SpacesView.as_view(path='all'), name='spaces'),
    path('space/<str:sub_page>', views.SpacesView.as_view(path='result'),
         name='space_view'),

    path('machines', views.MachinesView.as_view(path='all'), name='machines'),
    path('machine/<str:sub_page>', views.MachinesView.as_view(path='result'),
         name='machine_view'),

    path('projects', views.ProjectsView.as_view(), name='projects'),

    path('events', views.EventsView.as_view(path='all'), name='events'),
    path('event/new', views.EventsView.as_view(path='new'), name='event_new_view'),
    path('event/<str:sub_page>/banner',
         views.EventsView.as_view(path='banner'), name='event_banner_view'),
    path('event/<str:sub_page>',
         views.EventsView.as_view(path='result'), name='event_view'),

    path('photos', views.PhotosView.as_view(), name='photos'),

    path('consensus', views.ConsensusView.as_view(), name='consensus'),

    path('logout', views.LogoutView.as_view(), name='logout'),

]+api_urls + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

handler404 = '_website.views.handler_404_view.handler404'
