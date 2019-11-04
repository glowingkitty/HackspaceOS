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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.landingpage_view, name='landingpage'),

    path('meetings', views.meetings_view, name='meetings'),
    path('meeting', RedirectView.as_view(
         url='meetings', permanent=False), name='meeting'),
    path('meetings/', RedirectView.as_view(
         url='meetings', permanent=False), name='meetings/'),
    path('meeting/', RedirectView.as_view(
        url='meetings', permanent=False), name='meeting/'),

    path('meeting/present', views.meeting_present_view,
         name='meeting_present_view'),
    path('meeting/<str:date>', views.meeting_entry_view,
         name='meeting_present_view'),

    path('get/', views.get_view, name='get'),
    path('save', views.save_view, name='save'),
    path('remove', views.remove_view, name='remove'),
    path('search', views.search_view, name='search'),
    path('new', views.new_view, name='search'),
]
