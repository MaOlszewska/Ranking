
import PySimpleGUI as sg
from evm_ranking import calculate_ranking_EVM
from gmm_ranking import calculate_ranking_GMM
# Elements that are centered
experts = 0
column_countries = [
    [sg.Text("Countries:  ")],
    [sg.Listbox( size=(25, 13), values=[
        'Spain', 'Poland', 'Germany',
        'Italy', 'Switzerland', 'Norway',
        'Greece','France','Russia',
        'England',
        'Ireland','Turkey','Belarus'
        ],key="LIST", select_mode= sg.LISTBOX_SELECT_MODE_MULTIPLE, enable_events=True, highlight_background_color='DarkBlue')],
]
column_priority = [
    
    [sg.Text("On a scale of 0-10, compare the following pairs")],
    [sg.Text("Polulation - Average life length")],
    [sg.Text("Polulation - PKB")],
    [sg.Text("Population - Happiness")],
    [sg.Text("Average life length - PKB")],
    [sg.Text("Average life length - Happiness")],
    [sg.Text("PKB - Happiness")],
]
column_input = [
    [sg.Text("")],
    [sg.In("7", size=(5, 1), enable_events=True, key="POP-AVG")],
    [sg.In("7", size=(5, 1), enable_events=True, key="POP-PKB")],
    [sg.In("6", size=(5, 1), enable_events=True, key="POP-HAPP")],
    [sg.In("8", size=(5, 1), enable_events=True, key="AVG-PKB")],
    [sg.In("9", size=(5, 1), enable_events=True, key="AVG-HAPP")],
    [sg.In("6", size=(5, 1), enable_events=True, key="PKB-HAPP")],
]
column_ranking_EVM = [
    [sg.Text("Ranking EVM:  ")],
    [sg.Listbox(size=(25, 13), values=[], key="RANKING_EVM",  no_scrollbar=True )],
]

column_ranking_GMM = [
    [sg.Text("Ranking GMM:  ")],
    [sg.Listbox(size=(25, 13), values=[], key="RANKING_GMM",  no_scrollbar=True )],
]

layout = [
    [sg.Text("For example:")],
    [sg.Text("If PKB is more important than Happiness type 0 but if Happiness is more important than PKB type 10.", justification='left')],
    [sg.Text("If you type 5 it means that both are equally important.", justification='left')],
    [sg.Column(column_priority, justification='left'),
     sg.Column(column_input, justification="left"),
     sg.Column(column_countries, justification='left'),
     sg.Column(column_ranking_EVM, justification='left'),
     sg.Column(column_ranking_GMM, justification='left')
    ],
    [sg.Text("Add next expert"),
    sg.Button("ADD", button_color='Red', mouseover_colors=('White', 'Green')),
    sg.Text("Current experts added: 0", key="expcnt", text_color="Red")],
    [sg.Text("Clear experts"),
    sg.Button("CLEAR", button_color='Red', mouseover_colors=('White', 'Green'))],
    [sg.Text("For active countries"),
    sg.Button("Calculate rankings", button_color='Red', mouseover_colors=('White', 'Green'))],
    [sg.Button("CLOSE", button_color='Red', mouseover_colors =('White','LightGreen'))]
]

# Create the window
sg.theme_global('DarkGreen')
window = sg.Window("Ranking", layout, resizable=True, font= 'Any` 15')

# List with Country data
tab = []
activeCountry = []
prio = []
while True:
    event, values = window.read()
    # Add new Country
    if event == "READ":
        tab.append(values["INPUT"])
        window["LIST"].update(tab)
    # Close window
    if event == "CLOSE" or event == sg.WIN_CLOSED:
        break
    if event == "CLEAR":
        prio = []
        experts = 0
        window["expcnt"].update(f"Current experts added: {experts}")
    if event == "ADD":
        experts += 1
        priority = []
        priority.append(values['POP-AVG'])
        priority.append(values['POP-PKB'])
        priority.append(values['POP-HAPP'])
        priority.append(values['AVG-PKB'])
        priority.append(values['AVG-HAPP'])
        priority.append(values['PKB-HAPP'])
        prio.append(priority)
        window["expcnt"].update(f"Current experts added: {experts}")
    # Calculate and show ranking
    if event == "Calculate rankings":
        activeCountry = values['LIST']
        if len(prio) < 1:
            print("You need to add at least one expert")
            sg.Popup('You need to add at least one expert', keep_on_top=True)
            continue
        if len(activeCountry) < 1:
            print("You need to add at least one Country")
            sg.Popup('You need to add at least one Country', keep_on_top=True)
            continue
        # print(activeCountry)
        # print(priority)
        w = [0, 0]
        ranking_evm, w[0]= calculate_ranking_EVM(prio, activeCountry)
        # print(ranking)
        window['RANKING_EVM'].update(ranking_evm)
        ranking_gmm, w[1]= calculate_ranking_GMM(prio, activeCountry)
        # print(ranking)
        # print(w[0])
        # print(w[1])
        window['RANKING_GMM'].update(ranking_gmm)

window.close()