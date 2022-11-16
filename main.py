import PySimpleGUI as sg

layout = [
    [sg.Text("Hello")],
    [sg.Button("Close")],
    [sg.Text("For active countries press"), sg.Button("Show")],
    [sg.In(size=(25, 1), enable_events=True, key="xd")],
    [sg.Button("Read")],
    [sg.Text(size=(25, 3), key="c")],
    [sg.Listbox(size=(25, 3), values=[], enable_events=True, key="list")]]

# Create the window
window = sg.Window("Demo", layout)
tab = []
# Create an event loop
while True:
    event, values = window.read()
    # End program if user closes window or
    # presses the OK button
    if event == "Read":
        tab.append(values["xd"])
        print(values["xd"])
        window["c"].update(tab)
        window["list"].update(tab)
    if event == "Close" or event == sg.WIN_CLOSED:
        break

window.close()
