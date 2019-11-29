import os
import slack
from getKey import STR__get_key

# API documentation: https://github.com/slackapi/python-slackclient

client = slack.WebClient(token=STR__get_key('SLACK.API_TOKEN'))


def send_message(message, channel='#general'):
    print('LOG: send_message(message, channel={})'.format(channel))
    # see https://github.com/slackapi/python-slackclient#sending-a-message-to-slack
    response = client.chat_postMessage(channel=channel, text=message)

    if response['ok'] == True:
        print('LOG: --> Success! Sent message to Slack')
    else:
        print('LOG: --> Failed!')
