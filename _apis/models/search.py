from _setup.models import Log
from django.db.models import Q
import time


class Search():
    def __init__(self, show_log=True, test=False):
        self.logs = ['self.__init__']
        self.show_log = show_log
        self.started = round(time.time())
        self.test = test

    @property
    def setup_done(self):
        from _apis.models import Discourse, MediaWiki
        return True if Discourse().setup_done and MediaWiki().setup_done else False

    @property
    def config(self):
        from _apis.models import Discourse, MediaWiki
        return {"Discourse": Discourse().config, "MediaWiki": MediaWiki().config}

    def log(self, text):
        import os
        self.logs.append(text)
        if self.show_log == True:
            Log().print('{}'.format(text), os.path.basename(__file__), self.started)

    def setup(self):
        from _setup.models import Log
        from _apis.models import Discourse, MediaWiki
        try:
            discourse_setup_done = Discourse(test=self.test).setup_done
            mediawiki_setup_done = MediaWiki(test=self.test).setup_done
            if not discourse_setup_done or not mediawiki_setup_done:
                Log().show_messages(
                    ['Let\'s setup the search for your new website!'])

                if not discourse_setup_done:
                    Discourse(test=self.test).setup()

                if not mediawiki_setup_done:
                    MediaWiki(test=self.test).setup()

            Log().show_message('Search setup complete.')
        except KeyboardInterrupt:
            Log().show_message('Ok, canceled setup.')

    def query(self, query, filter_name=None):
        self.log('query()')
        from _apis.models import Discourse, MediaWiki
        from _database.models import Person, Event, MeetingNote, Guilde, Machine, Space, Consensus, Project
        from _setup.models import Config

        if not query:
            return []

        if filter_name and filter_name == 'hosts':
            return Person.objects.filter(Q(str_name_en_US__icontains=query) | Q(url_discourse__icontains=query))

        # search in database
        events = Event.objects.filter(
            Q(boolean_approved=True) &
            (
                Q(str_name_en_US__icontains=query) | Q(
                    text_description_en_US__icontains=query)
            )
        ).QUERYSET__upcoming()

        if filter_name == 'events':
            return events
        else:
            events = events.LIST__search_results()[:5]

        # search in social network accounts
        networks = [{
            'icon': x['name'].lower(),
            'name': x['name'],
            'url': x['url'],
        } for x in Config('SOCIAL.SOCIAL_NETWORKS').value if query.lower()
            in x['name'].lower()]
        internchannels = [{
            'icon': x['name'].lower(),
            'name': x['name'],
            'url': x['url'],
        } for x in Config('SOCIAL.INTERNAL_COMMUNICATION_PLATFORMS').value if query.lower()
            in x['name'].lower()]

        meeting_notes = MeetingNote.objects.filter(
            Q(text_date__icontains=query) | Q(text_keywords__icontains=query)
        ).past().LIST__search_results()[:5]

        guildes = Guilde.objects.filter(
            Q(str_name_en_US__icontains=query) | Q(
                text_description_en_US__icontains=query)
        ).LIST__search_results()[:5]

        machines = Machine.objects.filter(
            Q(str_name_en_US__icontains=query) | Q(
                text_description_en_US__icontains=query)
        ).LIST__search_results()[:5]

        spaces = Space.objects.filter(
            Q(str_name_en_US__icontains=query) | Q(
                text_description_en_US__icontains=query)
        ).LIST__search_results()[:5]

        consensus_items = Consensus.objects.filter(
            Q(str_name_en_US__icontains=query) | Q(
                text_description_en_US__icontains=query)
        ).LIST__search_results()[:5]

        projects = Project.objects.filter(
            Q(str_name_en_US__icontains=query) | Q(
                text_description_en_US__icontains=query)
        ).LIST__search_results()[:5]

        # search in wiki
        try:
            wiki_search_results = MediaWiki().search(query)
        except:
            self.log('-> ERROR: wiki search failed')
            wiki_search_results = []

        # search in discourse
        try:
            discourse_search_results = Discourse().search(query)
        except:
            self.log('-> ERROR: discourse search failed')
            discourse_search_results = []

        return networks+internchannels+events+guildes+machines+spaces+meeting_notes+consensus_items+projects+wiki_search_results+discourse_search_results
