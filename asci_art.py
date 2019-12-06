class bcolors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def happy_face():
    print('            ')
    print(bcolors.OKGREEN+'    ^  ^    '+bcolors.ENDC)
    print(bcolors.OKGREEN+'    \__/    '+bcolors.ENDC)
    print('            ')


def confused_face():
    print('            ')
    print(bcolors.WARNING+'    o  O    '+bcolors.ENDC)
    print(bcolors.WARNING+'    ----    '+bcolors.ENDC)
    print('            ')


def sad_face():
    print('            ')
    print(bcolors.FAIL+'    >  <    '+bcolors.ENDC)
    print(bcolors.FAIL+'    ----    '+bcolors.ENDC)
    print('            ')


def show_message(text):
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
    print(bcolors.HEADER+'  /-------------------------------\   '+bcolors.ENDC)
    for line in lines:
        print(bcolors.HEADER+'  |  '+bcolors.ENDC +
              line+bcolors.HEADER+'  |   '+bcolors.ENDC)
    print(bcolors.HEADER+'  \       /-----------------------/   '+bcolors.ENDC)
    print(bcolors.HEADER+'   \     /   '+bcolors.ENDC)
    print(bcolors.HEADER+'    \---/   '+bcolors.ENDC)

    if text.startswith('WARNING:') or text.startswith('Guess later then'):
        confused_face()
    elif text.startswith('ERROR:'):
        sad_face()
    else:
        happy_face()


def show_messages(list_messages):
    for message in list_messages:
        show_message(message)
        input(bcolors.WARNING+"Press Enter to continue..."+bcolors.ENDC)


def set_secret(json_secrets, later_then_message, message, str_level_0, str_level_1=None, str_level_2=None, str_level_3=None):
    if str_level_3:
        show_message(message)
        json_secrets[str_level_0][str_level_1][str_level_2][str_level_3] = input()
        if not json_secrets[str_level_0][str_level_1][str_level_2][str_level_3]:
            json_secrets[str_level_0][str_level_1][str_level_2][str_level_3] = None
            show_message(later_then_message)

    elif str_level_2:
        show_message(message)
        json_secrets[str_level_0][str_level_1][str_level_2] = input()
        if not json_secrets[str_level_0][str_level_1][str_level_2]:
            json_secrets[str_level_0][str_level_1][str_level_2] = None
            show_message(later_then_message)

    elif str_level_1:
        show_message(message)
        json_secrets[str_level_0][str_level_1] = input()
        if not json_secrets[str_level_0][str_level_1]:
            json_secrets[str_level_0][str_level_1] = None
            show_message(later_then_message)

    elif str_level_0:
        show_message(message)
        json_secrets[str_level_0] = input()
        if not json_secrets[str_level_0]:
            json_secrets[str_level_0] = None
            show_message(later_then_message)

    return json_secrets


def set_secrets(json_secrets, later_then_message, str_set_what):
    location = str_set_what.upper()
    for parameter in json_secrets[location]:
        if json_secrets[location][parameter] == None:
            show_message(
                'Please enter your '+parameter+' for '+str_set_what+' (or add it later and press Enter now)')
            json_secrets[location][parameter] = input()
            if not json_secrets[location][parameter]:
                json_secrets[location][parameter] = None
                show_message(later_then_message)
                break

        elif json_secrets[location][parameter] != None:
            for sub_paramter in json_secrets[location][parameter]:
                show_message(
                    'Please enter your '+parameter+' '+sub_paramter+' for '+str_set_what+' (or add it later and press Enter now)')
                json_secrets[location][parameter][sub_paramter] = input()
                if not json_secrets[location][parameter][sub_paramter]:
                    json_secrets[location][parameter][sub_paramter] = None
                    show_message(later_then_message)
                    break

    return json_secrets
