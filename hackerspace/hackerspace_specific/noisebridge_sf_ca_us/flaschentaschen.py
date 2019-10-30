import requests


def showText(text):
    try:
        requests.post('http://pegasus.noise:4444/api/text', {'text': text})
    except:
        print('Couldnt talk to Flaschentaschen. Make sure to deactivate your VPN connection and be in the local Noisebridge network.')
