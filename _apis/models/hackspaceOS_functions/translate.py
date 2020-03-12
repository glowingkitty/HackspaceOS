class Translate():
    def __init__(self, request=None):
        from django.http import JsonResponse
        import json
        import bleach
        from googletrans import Translator
        import emoji
        from _setup.models import Config
        translator = Translator()

        with open('_translations/languages.json') as json_file:
            language_codes = json.load(json_file)

        if request.GET.get('q', None) and request.GET.get('language', None):
            text = emoji.get_emoji_regexp().sub(u'', request.GET.get('q', None))

            response = JsonResponse({'text': translator.translate(
                text=text,
                dest=request.GET.get('language', None)).text
            })

        elif request.GET.get('q', None):
            LANGUAGES = Config('WEBSITE.LANGUAGES').value
            languages = {}

            text = emoji.get_emoji_regexp().sub(u'', request.GET.get('q', None))

            for language in LANGUAGES:
                if len(LANGUAGES) > 1:
                    languages[language] = translator.translate(
                        text=text,
                        dest=language_codes[language]).text
                else:
                    languages[language] = request.GET.get('q', None)

            response = JsonResponse(languages)

        else:
            response = JsonResponse({'error': 'fields missing'})
            response.status_code = 404

        self.value = response
