from hackerspace.models.events import Event
from hackerspace.models.spaces import Space
from hackerspace.models.persons import Person
from hackerspace.models.machines import Machine
from hackerspace.models.guildes import Guilde
from django.contrib import admin


class AuthorAdmin(admin.ModelAdmin):
    exclude = ('str_slug', 'int_UNIXtime_created', 'int_UNIXtime_updated',)


# Register your models here.
admin.site.register(Event, AuthorAdmin)
admin.site.register(Guilde, AuthorAdmin)
admin.site.register(Machine, AuthorAdmin)
admin.site.register(Person, AuthorAdmin)
admin.site.register(Space, AuthorAdmin)
