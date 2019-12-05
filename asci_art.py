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
    print('  /-------------------------------\   ')
    for line in lines:
        print('  |  '+line+'  |   ')
    print('  \       /-----------------------/   ')
    print('   \     /   ')
    print('    \---/   ')
    print('            ')
    print('    ^  ^    ')
    print('    \__/     ')
    print('            ')


def show_messages(list_messages):
    for message in list_messages:
        show_message(message)
        input("Press Enter to continue...")


def set_secrets(json_secrets, str_set_what):
    location = str_set_what.upper()
    for parameter in json_secrets[location]:
        if json_secrets[location][parameter] == None:
            show_message(
                'Please enter your '+parameter+' for '+str_set_what+' (or add it later and press Enter now)')
            json_secrets[location][parameter] = input()
            if not json_secrets[location][parameter]:
                json_secrets[location][parameter] = None
                show_message('Guess later then...')
                break

        elif json_secrets[location][parameter] != None:
            for sub_paramter in json_secrets[location][parameter]:
                show_message(
                    'Please enter your '+parameter+' '+sub_paramter+' for '+str_set_what+' (or add it later and press Enter now)')
                json_secrets[location][parameter][sub_paramter] = input()
                if not json_secrets[location][parameter][sub_paramter]:
                    json_secrets[location][parameter][sub_paramter] = None
                    show_message('Guess later then...')
                    break

    return json_secrets
