"""hackerspace URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from hackerspace.website import views
from django.views.generic.base import RedirectView
from hackerspace.YOUR_HACKERSPACE import ADMIN_URL

urlpatterns = [
    path(ADMIN_URL+'/', admin.site.urls),
    path('', views.landingpage_view, name='landingpage'),

    path('values', views.values_view, name='values'),
    path('values/', RedirectView.as_view(
         url='values', permanent=False), name='values/'),
    path('ourvalues', RedirectView.as_view(
        url='values', permanent=False), name='ourvalues/'),
    path('ourvalues/', RedirectView.as_view(
        url='values', permanent=False), name='ourvalues'),

    path('meetings', views.meetings_view, name='meetings'),
    path('meeting', RedirectView.as_view(
         url='meetings', permanent=False), name='meeting'),
    path('meetings/', RedirectView.as_view(
         url='meetings', permanent=False), name='meetings/'),
    path('meeting/', RedirectView.as_view(
        url='meetings', permanent=False), name='meeting/'),
    path('meeting/present', views.meeting_present_view,
         name='meeting_present_view'),
    path('meeting/end', views.meeting_end_view,
         name='meeting_end_view'),
    path('meeting/<str:sub_page>', views.meeting_view,
         name='meeting_present_view'),

    path('guildes', views.guildes_view, name='guildes'),
    path('guilde/<str:sub_page>', views.guilde_view,
         name='guilde_view'),

    path('spaces', views.spaces_view, name='spaces'),
    path('space/<str:sub_page>', views.space_view,
         name='space_view'),

    path('machines', views.machines_view, name='machines'),
    path('machine/<str:sub_page>', views.machine_view,
         name='machine_view'),

    path('get/', views.get_view, name='get'),
    path('load_more', views.load_more_view, name='load_more'),
    path('save', views.save_view, name='save'),
    path('remove', views.remove_view, name='remove'),
    path('search', views.search_view, name='search'),
    path('new', views.new_view, name='search'),
]
