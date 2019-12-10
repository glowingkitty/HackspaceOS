from datetime import datetime


def log(text):
    print(datetime.now().strftime('[%d/%b/%Y %H:%m:%S]')+' '+text)
