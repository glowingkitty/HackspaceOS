from django.core.management.base import BaseCommand


class Command(BaseCommand):
    help = "Update translations"

    def handle(self, *args, **options):
        # if a language doesn't exist yet for a word, get translation via Google Translate
        # this way improved translations don't get overwritten by Google Translate
        import json
        from googletrans import Translator
        from hackerspace.log import log
        import time
        translator = Translator()

        log('Update translations...')

        with open('hackerspace/Website/templates/languages.json') as json_file:
            language_codes = json.load(json_file)
        with open('translations.json') as json_file:
            translations = json.load(json_file)

        # TODO: replace with create list of words first and translate list of words -> prevent hitting API rate limit
        for word in translations:
            for language_code in language_codes:
                if language_code not in translations[word]:
                    translations[word][language_code] = translator.translate(
                        text=translations[word]['english'],
                        dest=language_codes[language_code]).text
                    time.sleep(0.5)

        with open('translations.json', 'w') as outfile:
            json.dump(translations, outfile, indent=4)

        log('--> Done!')
