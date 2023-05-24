import PySimpleGUI as sg
import os
import threading
import subprocess

def butler_script():
    # Global Variable
    script_logs = []

    # Theme of GUI
    sg.theme('BluePurple')

    # Function: Get all folders
    def get_folders():
        return next(os.walk('./'))[1] # returns an array of folders in current directory

    # Function: Get all scripts
    def get_scripts(folder):
        return next(os.walk("./" + folder))[2] # returns an array of scripts in the selected folder


    # Function: long thread
    def long_function_thread(window):
        script_thread = subprocess.Popen("sh ./run.sh " + selected_folder + " " + selected_script[0], stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        for line in script_thread.stdout:
            if (line.strip() == "Script failed to execute"):
                print("Butler failed to execute script. Check logs.")
            elif (line.strip() == "Script executed successfully"):
                print("Butler executed script successfully.")
            window.write_event_value('Thread Log', line)

    # Function: start long thread
    def long_function():
        threading.Thread(target=long_function_thread, args=(window,), daemon=True).start()

    # Main Tab
    main_tab_layout = [
        [sg.Text("Choose folder:")],
        [sg.Combo(get_folders(), default_value="Select a Folder", key="-FOLDERS-",enable_events=True, expand_x=True)], # combo takes in a list of values
        [sg.Text("Choose script:")],
        [sg.Listbox(key='-SCRIPTS-', s=(0, 5), values=["No folder selected"], expand_x=True, expand_y=True)],
        [sg.Push(), sg.Button('Run'), sg.Push()]
    ]


    # Logs Tab
    logs_tab_layout = [
        [sg.Multiline(key='-LOGS-',expand_y=True, expand_x=True)],
        # [sg.Output()],
        [sg.Button('Export Logs'), sg.Push(), sg.Button('Clear Logs')]
    ]

    # Menu Bar
    menu_def = [['&File', ['!&Open', '&Save::savekey', '---', '&Properties', 'E&xit']],
                ['!&Edit', ['!&Paste', ['Special', 'Normal', ], 'Undo'], ],
                ['&Debugger', ['Local Variables', 'Launch Debugger']],
                ['&Toolbar', ['Command &1', 'Command &2', 'Command &3', 'Command &4']],
                ['&Help', '&About...']]

    menu_elem = sg.Menu(menu_def)

    # OVERALL Layout
    layout = [
        [menu_elem],
        [sg.TabGroup([
            [sg.Tab('Main', main_tab_layout), sg.Tab('Logs', logs_tab_layout)]
        ], expand_x=True, expand_y=True)],
        [sg.Push(), sg.Button('Exit')],
        [sg.Text('Butler'), sg.Output(s=(50, 3), expand_x=True, expand_y=True)]
    ]

    


    window = sg.Window('Butler Script', layout, resizable=True)
    bot_live = False
    
    # Floating window
    # floating_layout = [
    #     [[sg.Col([[sg.Button('Test')]])]]
    # ]
    # floating_window = sg.Window('Butler Script', floating_layout, no_titlebar=True, grab_anywhere=True, margins=(0,0), background_color='black')


    while True:  # Event Loop
        # floating_window.read()
        event, values = window.read(timeout=200)

        if bot_live != True:
            print("Butler at your service! What would you like to do?")
            bot_live = True

        if event == sg.TIMEOUT_KEY:
            continue
        # event, values = window.read()

        # Local variables
        selected_folder = None
        selected_script = values['-SCRIPTS-']

        # Event: Close Window/Program
        if event == sg.WIN_CLOSED or event == 'Exit':
            break


        # Event: Select a folder and Display Scripts on Folder selection
        if values['-FOLDERS-'] != "Select a Folder":
            selected_folder = values['-FOLDERS-']
            display_scripts = get_scripts(selected_folder)
            if len(display_scripts) != 0:
                window['-SCRIPTS-'].update(display_scripts)
            else:
                window['-SCRIPTS-'].update(['No scripts in folder'])
            

        # Event: Run selected script
        if event == 'Run' and selected_folder != None and (len(values['-SCRIPTS-']) == 1):
            selected_script = values['-SCRIPTS-']
            print("You have selected " + selected_script[0] + ". Butler is running script.")
            long_function()
            # os.system("sh ./run.sh " + selected_folder + " " + selected_script[0])

        # Event: Log out from script
        if event == 'Thread Log':
            script_logs.append(values[event])
            window['-LOGS-'].print(values[event])

        # Event: Clear Logs
        if event == 'Clear Logs':
            window['-LOGS-'].update('')
            script_logs = []
            print("Logs have been cleared")

        # Event: Export Logs
        if event == 'Export Logs':
            # python write to file
            print("Logs have been exported")


        # MENU ITEMS
        # Debugger Item
        if event == 'Local Variables':
            sg.show_debugger_popout_window()
            print("Local Variables Monitor launched.")

        if event == 'Launch Debugger':
            sg.show_debugger_window(location=(0, 0))
            print("Debugger launched.")

    window.close()

butler_script()

