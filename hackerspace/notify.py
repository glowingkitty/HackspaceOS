from hackerspace.hackerspace_specific.noisebridge_sf_ca_us.marry import speak


def notify(list_where=['Slack'], json_context={}):
    if 'Slack' in list_where:
        print('notify via slack API...')

    if json_context['str_what'] == 'error_new':
        speak('Please listen. A new error occured on the Noisebridge website. Please take a look at the Noisebridge infrastructure Github repo. The error code is ' +
              json_context['str_error_code']+'. And the message is "'+json_context['str_name_en_US'])

    elif json_context['str_what'] == 'error_repeated_10':
        speak('Please listen. The Noisebridge website is still broken and the error with the code ' +
              json_context['str_error_code']+' now happened 10 times. Please take a look at the Noisebridge infrastructure Github repo and fix the issue. Have a wonderful day')

    elif json_context['str_what'] == 'error_repeated_100':
        speak('Please listen. It seems everyone ignores me. The Noisebridge website is still broken and the error with the code ' +
              json_context['str_error_code']+' now happened 100 times. That is a lot. Please take a look at the Noisebridge infrastructure Github repo and fix the issue. Meow meow')

    elif json_context['str_what'] == 'error_repeated_1000':
        speak('Help me. I feel pain. A lot of pain. The Noisebridge website is still broken and the error with the code ' +
              json_context['str_error_code']+' now happened 1000 times. It hurts, a lot. Can someone please take a look at the Noisebridge infrastructure Github repo and fix the issue? Otherwise I have to initiate the Noisebridge selfdestruction mode. In 5. 4. 3. 2. 1. . . . . . . Hmm. Seems that has failed as well. But seriously. Please fix the error code '+json_context['str_error_code'])
