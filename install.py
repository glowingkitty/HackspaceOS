import os
import platform

system = platform.system()
if system == 'Windows':
    print('It seems you are using Windows. Please download Ubuntu or another Linux Subsystem from the Windows 10 AppStore and install the HackspaceOS inside the Linux Subsystem - or alternatively install Linux or MacOS on your device instead.')
else:
    main_folder_path = os.path.dirname(
        os.path.abspath(__file__))
    python = main_folder_path+"/HackspaceOSVenv/bin/python"
    pip = main_folder_path+"/HackspaceOSVenv/bin/pip"

    if os.path.isdir('HackspaceOSVenv') == False:
        print('Setting up the Python Virtual Environment...')
        os.system('python3 -m venv HackspaceOSVenv')

    print('Installing requirements.txt...')
    os.system('cat requirements.txt | xargs -n 1 {} install'.format(pip))

    print('Start / setup server')
    os.system(python+' manage.py runserver')
