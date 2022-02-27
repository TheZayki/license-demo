import base64

import GUI
import requests
import json

global auth


def find_licenses(owner, repo):
    if auth != "":
        licenses = requests.get(f"https://api.github.com/search/code?q=license+in:file+repo:{owner}/{repo}",
                                headers={'Authorization': f"Token {auth}"})
    else:
        licenses = requests.get(f"https://api.github.com/search/code?q=license+in:file+repo:{owner}/{repo}")

    data = json.loads(licenses.text)
    return data


def conventional_license(owner, repo):
    if auth != "":
        licenses = requests.get(f"https://api.github.com/repos/{owner}/{repo}/license",
                                headers={'Authorization': f"Token {auth}"})
    else:
        licenses = requests.get(f"https://api.github.com/repos/{owner}/{repo}/license")
    data = json.loads(licenses.text)
    return data


def analyze_license(url):
    if auth != "":
        licenses = requests.get(url, headers={'Authorization': f"Token {auth}"})
    else:
        licenses = requests.get(url)
    licenses = json.loads(licenses.text)

    try:
        licenses = base64.b64decode(licenses['content']).decode()
    except KeyError:
        return "API rate limit exceeded."

    license_dict = [
        "Academic&nbsp;Free License",
        "Apache&nbsp;License Version 2.0",
        "Artistic&nbsp;License 2.0",
        "Boost&nbsp;Software License 1.0",
        "BSD&nbsp;2 - Clause License",
        "BSD&nbsp;3 - Clause License",
        "Clear&nbsp;BSD License",
        "Creative Commons Legal Code",
        "Creative Commons Attribution 4.0 International Public License",
        "Creative Commons Attribution-ShareAlike 4.0 International Public License",
        "DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE",
        "Educational&nbsp;Community License Version 2.0",
        "Eclipse&nbsp;Public License",
        "European Union Public License V. 1.1",
        "GNU AFFERO GENERAL PUBLIC LICENSE",
        "GNU GENERAL PUBLIC LICENSE",
        "GNU LESSER GENERAL PUBLIC LICENSE",
        "ISC&nbsp;License",
        "LaTeX Project Public License",
        "Microsoft Public License (Ms - PL)",
        "MIT&nbsp;License",
        "Mozilla Public License Version 2.0",
        "Open&nbsp;Software License",
        "PostgreSQL License",
        "SIL Open Font License",
        "University of Illinois / NCSA Open Source License",
        "free and unencumbered software released into the public domain",
        "zlib License"
    ]

    license_key = ""
    for key in license_dict:
        license_key = ""
        found = True
        temp_key = key.split(" ")
        for i in temp_key:
            i = i.replace("&nbsp;", " ")
            if i not in licenses:
                found = False

        if found:
            license_key = key
            break

    if license_key != "":
        return license_key
    return "unbekannt"


def checkDone(info):
    if info == "end":
        return True
    return False


def main_procedure(owner, repo):
    data = find_licenses(owner, repo)
    print(data)

    if "errors" in data:
        info = GUI.printText([["Der Besitzer oder Name des Repositorys konnte nicht gefunden werden.\n"]],
                             "Programm neu starten")
        if checkDone(info):
            return
        main()
        return

    if data["total_count"] == 0:
        GUI.printText([["Das Repository hat keine Lizenzdatei -> Alle Rechte vorbehalten"]], "Programm beenden")
        return

    elif data["total_count"] == 1:
        one_license = conventional_license(owner, repo)

        if "message" in one_license:
            items = data["items"]
            found_license = analyze_license(items[0]['url'])

            if found_license != "API rate limit exceeded.":
                GUI.printText([[f"Das Repository hat eine Lizenzdatei, welche aber nicht im Wurzelverzeichnis liegt:",
                                f"Lizenzdateiname: {items[0]['name']}",
                                f"Lizenzdateipfad: {items[0]['path']}",
                                f"Lizenztyp: {found_license}",
                                f"Dateilink: {items[0]['html_url']}"]], "Programm beenden")
            else:
                GUI.printText([[f"Das API rate limit wurde überschritten. Bitte authentifizieren um Fortzufahren."]],
                              "Programm beenden")
        else:
            GUI.printText([[f"Das Repository hat eine Lizenzdatei, welche im Wurzelverzeichnis liegt:",
                            f"Lizenzdateiname: {one_license['name']}",
                            f"Lizenzdateipfad: {one_license['path']}",
                            f"Lizenztyp: {one_license['license']['name']}",
                            f"Dateilink: {one_license['html_url']}"]], "Programm beenden")
        return

    elif data["total_count"] > 1:
        items = data['items']
        printString = [[f"Im Repository wurden folgende {data['total_count']} Lizenzen gefunden"]]

        for item in items:
            found_license = analyze_license(item['url'])
            if found_license != "API rate limit exceeded.":
                printString.append([f"Lizenzdateiname: {item['name']}",
                                    f"Lizenzdateipfad: {item['path']}",
                                    f"Lizenztyp: {found_license}",
                                    f"Dateilink: {item['html_url']}",
                                    f"\n"])

            else:
                GUI.printText([[f"Das API rate limit wurde überschritten. Bitte authentifizieren um Fortzufahren."]],
                              "Programm beenden")
                return

        GUI.printText(printString, "Programm beenden")
        return


def main():
    info = GUI.query()

    if checkDone(info):
        return

    global auth
    auth = info[2]

    main_procedure(info[0], info[1])


main()
