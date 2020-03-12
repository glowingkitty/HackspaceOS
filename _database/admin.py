from _database.models import Event,Space,Machine,Project,Guilde,Consensus
from django.contrib import admin


class AuthorAdmin(admin.ModelAdmin):
    exclude = ('str_slug', 'int_UNIXtime_created', 'int_UNIXtime_updated',)


# Register your models here.
admin.site.register(Event, AuthorAdmin)
admin.site.register(Project, AuthorAdmin)
admin.site.register(Guilde, AuthorAdmin)
admin.site.register(Machine, AuthorAdmin)
admin.site.register(Space, AuthorAdmin)
admin.site.register(Consensus, AuthorAdmin)
