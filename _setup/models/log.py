import time


class Log():
    def print(self, text, filename=None, script_started_time=None, show_datetime=False):
        string = ''
        if filename:
            string += filename + ' | '
        if script_started_time:
            seconds_passed = round(time.time()-script_started_time)
            hh = int(seconds_passed/60/60)
            seconds_passed = seconds_passed-(60*60*hh)
            if hh < 10:
                hh = '0'+str(hh)
            mm = int(seconds_passed/60)
            ss = seconds_passed-(60*mm)
            if mm < 10:
                mm = '0'+str(mm)
            if ss < 10:
                ss = '0'+str(ss)
            string += '{}:{}:{} | '.format(hh, mm, ss)

        else:
            from datetime import datetime
            string += str(datetime.now())+' | '

        if 'error' in text.lower():
            print(string+self.prRed(text))
        elif 'failed' in text.lower():
            print(string+self.prYellow(text))
        else:
            print(string+self.prGreen(text))

    def show_message(self, text):
        if type(text) != str:
            raise TypeError

        # split up string so it fits into lines (27 character per lines)
        words = text.split(' ')
        lines = []
        while len(words) > 0:
            line = ''
            for word in words:
                if len(line)+len(word) > 27:
                    break
                else:
                    line = line+word+' '
                    words = words[1:]

            while len(line) < 27:
                line = line + ' '
            lines.append(line)

        print('                                      ')
        print('                                      ')
        print('                                      ')
        print(self.prPurple('  /-------------------------------\   '))
        for line in lines:
            print(self.prPurple('  |  ') + line + self.prPurple('  |   '))
        print(self.prPurple('  \       /-----------------------/   '))
        print(self.prPurple('   \     /   '))
        print(self.prPurple('    \---/   '))

        if text.startswith('WARNING:') or text.startswith('Guess later then'):
            self.confused_face()
        elif text.startswith('ERROR:'):
            self.sad_face()
        else:
            self.happy_face()

    def show_messages(self, list_messages):
        if type(list_messages) != list:
            raise TypeError

        for message in list_messages:
            self.show_message(message)
            print(self.prYellow("Continue in 3 seconds..."))
            time.sleep(3)

    def happy_face(self):
        print('            ')
        print(self.prGreen('    ^  ^    '))
        print(self.prGreen('    \__/    '))
        print('            ')

    def confused_face(self):
        print('            ')
        print(self.prYellow('    o  O    '))
        print(self.prYellow('    ----    '))
        print('            ')

    def sad_face(self):
        print('            ')
        print(self.prRed('    >  <    '))
        print(self.prRed('    ----    '))
        print('            ')

    def prRed(self, text):
        return "\033[91m {}\033[00m" .format(text)

    def prGreen(self, text):
        return "\033[92m {}\033[00m" .format(text)

    def prYellow(self, text):
        return "\033[93m {}\033[00m" .format(text)

    def prLightPurple(self, text):
        return "\033[94m {}\033[00m" .format(text)

    def prPurple(self, text):
        return "\033[95m {}\033[00m" .format(text)

    def prCyan(self, text):
        return "\033[96m {}\033[00m" .format(text)

    def prLightGray(self, text):
        return "\033[97m {}\033[00m" .format(text)

    def prBlack(self, text):
        return "\033[98m {}\033[00m" .format(text)
