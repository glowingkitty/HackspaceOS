# by Marco Bartsch
import time

# Python program to print 
# colored text and background 
def prRed(skk): 
    return "\033[91m {}\033[00m" .format(skk)

def prGreen(skk): 
    return "\033[92m {}\033[00m" .format(skk)

def prYellow(skk):
    return "\033[93m {}\033[00m" .format(skk)

def prLightPurple(skk):
    return "\033[94m {}\033[00m" .format(skk)

def prPurple(skk):
    return "\033[95m {}\033[00m" .format(skk)

def prCyan(skk):
    return "\033[96m {}\033[00m" .format(skk)

def prLightGray(skk):
    return "\033[97m {}\033[00m" .format(skk)

def prBlack(skk): 
    return "\033[98m {}\033[00m" .format(skk)
  
def log(text,filename=None,script_started_time=None,show_datetime=False):
    string = ''
    if filename:
        string += filename+ ' | '
    if script_started_time:
        seconds_passed = round(time.time()-script_started_time)
        hh = int(seconds_passed/60/60)
        seconds_passed = seconds_passed-(60*60*hh)
        if hh<10:
            hh='0'+str(hh)
        mm = int(seconds_passed/60)
        ss = seconds_passed-(60*mm)
        if mm<10:
            mm='0'+str(mm)
        if ss<10:
            ss='0'+str(ss)
        string += '{}:{}:{} | '.format(hh,mm,ss)

    else:
        from datetime import datetime
        string += str(datetime.now())+' | '

    if 'error' in text.lower():
        print(string+prRed(text))
    elif 'failed' in text.lower():
        print(string+prYellow(text))
    else:
        print(string+prGreen(text))
