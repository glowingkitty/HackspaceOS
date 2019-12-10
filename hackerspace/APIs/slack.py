import os
import slack
from getKey import STR__get_key, BOOLEAN__key_exists
from hackerspace.log import log

# API documentation: https://github.com/slackapi/python-slackclient


def send_message(message, channel='#general'):
    log('send_message(message, channel={})'.format(channel))
    if BOOLEAN__key_exists('SLACK.API_TOKEN') == False:
        log('--> KEY MISSING: SLACK.API_TOKEN not defined. Couldnt sent notification via Slack.')
    else:
        client = slack.WebClient(token=STR__get_key('SLACK.API_TOKEN'))

        # see https://github.com/slackapi/python-slackclient#sending-a-message-to-slack
        response = client.chat_postMessage(channel=channel, text=message)

        if response['ok'] == True:
            log('--> Success! Sent message to Slack')
        else:
            log('--> Failed!')
