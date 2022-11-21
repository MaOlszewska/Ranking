import PySimpleGUI as sg

# Elements that are centered
column = [
    [sg.Listbox( size=(25, 15), values=[],key="LIST", select_mode= sg.LISTBOX_SELECT_MODE_MULTIPLE, enable_events=True, highlight_background_color='Purple')],
    [sg.Text("Your choice:  ")],
    [sg.Listbox(size=(25, 10), values=[], key="ACTIVE" )],
    [sg.Text("For active countries press"), sg.Button("SHOW", button_color='White', mouseover_colors=('White','Purple'))]
]
layout = [
    [sg.Text("Add new country: "), sg.In(size=(30, 1), enable_events=True, key="INPUT"), sg.Button("READ", button_color='White', mouseover_colors =('White','Purple'))],
    [sg.Column(column, justification='center')],
    [sg.Button("CLOSE", button_color='White', mouseover_colors =('White','Purple'))]
]

# Create the window
sg.theme_global('LightPurple')
window = sg.Window("Ranking", layout, resizable=True, font= 'Any` 15')

# List with Country data
tab = []
activeCountry = []

while True:
    event, values = window.read()
    # Add new Country
    if event == "READ":
        tab.append(values["INPUT"])
        window["LIST"].update(tab)
    # Close window
    if event == "CLOSE" or event == sg.WIN_CLOSED:
        break
    # Update list with choosen country
    if event == "LIST":
        activeCountry = values['LIST']
        window['ACTIVE'].update(activeCountry)
    # Calculate and show ranking
    if event == "SHOW":
        break


window.close()
