import webbrowser
import PySimpleGUI as sg


def query():
    sg.theme('DarkAmber')
    window = sg.Window('Github-Lizenz-Mining',
                       [[sg.Text('Name des Repository Besitzers eingeben:',
                                                    font=(None, 12),
                                                    size=(35, 1)),
                                                    sg.InputText()],
                        [sg.Text('Name des Repositorys eingeben:',
                                                    font=(None, 12),
                                                    size=(35, 1)),
                                                    sg.InputText()],
                        [sg.Button('Ok', bind_return_key=True)]],
                                    element_justification='center')

    owner, repo = "", ""
    while owner == "" or repo == "":
        event, values = window.read()
        if event == sg.WIN_CLOSED:
            window.close()
            return "end"
        if values[0] != "" and values[1] != "":
            owner = values[0]
            repo = values[1]
            window.close()
        elif values[0] == "":
            sg.popup('Bitte Name des Repository Besitzers eingeben:',
                                                    font=(None, 12))
        elif values[1] == "":
            sg.popup('Bitte Name des Repositorys eingeben:',
                                                    font=(None, 12))

    return [owner, repo]


def printText(text, button_text):
    layout = []

    for t in text:
        for i in t:
            if str(i).startswith("Im Repository"):
                layout += [sg.Text(i, font=(None, 16),
                                      size=(200, 1),
                                      justification='center')],
                break
            if str(i).startswith("Dateilink"):
                layout += [sg.Text(i, font=(None, 12),
                                      text_color="LightBlue",
                                      size=(200, 1),
                                      justification='center',
                                      enable_events=True,
                                      key=f"URL: {i}")],
            else:
                layout += [sg.Text(i, font=(None, 12),
                                      size=(200, 1),
                                      justification='center')],
    layout += [[sg.Button(button_text, bind_return_key=True, key="end")]]

    window = sg.Window('Github-Lizenz-Mining',
                                    [[sg.Column(layout,
                                      size=(1400, 500),
                                      scrollable=True,
                                      element_justification='center')]],
                                      element_justification='center')

    while True:
        event, values = window.read()
        if str(event).startswith("URL: "):
            event = str(event).replace("URL: Dateilink: ", "")
            webbrowser.open_new_tab(event)
        if event == sg.WIN_CLOSED or event == "end":
            window.close()
            return "end"