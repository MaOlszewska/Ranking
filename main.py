
import PySimpleGUI as sg
from ranking_maker import calculate_ranking
# Elements that are centered

column_countries = [
    [sg.Text("Countries:  ")],
    [sg.Listbox( size=(25, 13), values=[
        'Spain', 'Poland', 'Germany',
        'Italy', 'Switzerland', 'Norway',
        'Greece','France','Russia',
        'England',
        'Ireland','Turkey','Belarus'
        ],key="LIST", select_mode= sg.LISTBOX_SELECT_MODE_MULTIPLE, enable_events=True, highlight_background_color='Purple')],
]
column_priority = [
    [sg.Text("On a scale of 1-17, compare the following pairs")],
    [sg.Text("Polulation - Average life length")],
    [sg.Text("Polulation - PKB")],
    [sg.Text("Population - Happiness")],
    [sg.Text("Average life length - PKB")],
    [sg.Text("Average life length - Happiness")],
    [sg.Text("PKB - Happiness")],
]
column_input = [
    [sg.Text("")],
    [sg.In("12", size=(5, 1), enable_events=True, key="POP-AVG")],
    [sg.In("12", size=(5, 1), enable_events=True, key="POP-PKB")],
    [sg.In("11", size=(5, 1), enable_events=True, key="POP-HAPP")],
    [sg.In("14", size=(5, 1), enable_events=True, key="AVG-PKB")],
    [sg.In("13", size=(5, 1), enable_events=True, key="AVG-HAPP")],
    [sg.In("10", size=(5, 1), enable_events=True, key="PKB-HAPP")],
]
column_ranking = [
    [sg.Text("Ranking:  ")],
    [sg.Listbox(size=(25, 13), values=[], key="RANKING",  no_scrollbar=True )],
]
layout = [
    [sg.Text("For example:")],
    [sg.Text("If PKB is more important than Happiness type 1 but if Happiness is more important than PKB type 17.", justification='left')],
    [sg.Text("If you type 9 it means that both are equally important.", justification='left')],
    [sg.Column(column_priority, justification='left'),
     sg.Column(column_input, justification="left"),
     sg.Column(column_countries, justification='left'),
     sg.Column(column_ranking, justification='left')],
    [sg.Text("For active countries press"),
     sg.Button("SHOW", button_color='White', mouseover_colors=('White', 'Purple'))],
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
    # Calculate and show ranking
    if event == "SHOW":
        priority = []
        activeCountry = values['LIST']
        priority.append(values['POP-AVG'])
        priority.append(values['POP-PKB'])
        priority.append(values['POP-HAPP'])
        priority.append(values['AVG-PKB'])
        priority.append(values['AVG-HAPP'])
        priority.append(values['PKB-HAPP'])
        print(activeCountry)
        print(priority)
        ranking = calculate_ranking(priority, activeCountry)
        window['RANKING'].update(ranking)

window.close()