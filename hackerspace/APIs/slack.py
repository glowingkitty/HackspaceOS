import os
import slack
from getKey import STR__get_key, BOOLEAN__key_exists

# API documentation: https://github.com/slackapi/python-slackclient


def send_message(message, channel='#general'):
    print('LOG: send_message(message, channel={})'.format(channel))
    if BOOLEAN__key_exists('SLACK.API_TOKEN') == False:
        print('LOG: --> KEY MISSING: SLACK.API_TOKEN not defined. Couldnt sent notification via Slack.')
    else:
        client = slack.WebClient(token=STR__get_key('SLACK.API_TOKEN'))

        # see https://github.com/slackapi/python-slackclient#sending-a-message-to-slack
        response = client.chat_postMessage(channel=channel, text=message)

        if response['ok'] == True:
            print('LOG: --> Success! Sent message to Slack')
        else:
            print('LOG: --> Failed!')
