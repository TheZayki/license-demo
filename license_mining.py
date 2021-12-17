import GUI
import requests
import json


def find_licenses(owner, repo):
    licenses = requests.get(f"https://api.github.com/search/code?q=license+in:file+repo:{owner}/{repo}")
    data = json.loads(licenses.text)
    return data


def conventional_license(owner, repo):
    licenses = requests.get(f"https://api.github.com/repos/{owner}/{repo}/license")
    data = json.loads(licenses.text)
    return data


def analyze_license(url):
    str(url).replace("blob", "raw")
    licenses = requests.get(url)
    licenses = licenses.text

    license_dict = [
        "Academic Free License",
        "Apache License Version 2.0",
        "The Artistic License 2.0",
        "Boost Software License 1.0",
        "BSD 2-Clause License",
        "BSD 3 - Clause License",
        "The Clear BSD License",
        "Creative Commons Legal Code",
        "Creative Commons Attribution 4.0 International Public License",
        "Creative Commons Attribution-ShareAlike 4.0 International Public License",
        "DO WHAT THE FUCK YOU WANT TO PUBLIC LICENSE",
        "Educational Community License Version 2.0",
        "Eclipse Public License",
        "European Union Public License V. 1.1",
        "GNU AFFERO GENERAL PUBLIC LICENSE",
        "GNU GENERAL PUBLIC LICENSE",
        "GNU LESSER GENERAL PUBLIC LICENSE",
        "ISC License",
        "The LaTeX Project Public License",
        "Microsoft Public License(Ms - PL)",
        "MIT License",
        "Mozilla Public License Version 2.0",
        "Open Software License",
        "PostgreSQL License",
        "SIL Open Font License",
        "University of Illinois / NCSA Open Source License",
        "This is free and unencumbered software released into the public domain",
        "zlib License"
    ]

    license_key = ""
    for key in license_dict:
        if key in licenses:
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
            GUI.printText([[f"Das Repository hat eine Lizenzdatei, welche aber nicht im Wurzelverzeichnis liegt:",
                            f"Lizenzdateiname: {items[0]['name']}",
                            f"Lizenzdateipfad: {items[0]['path']}",
                            f"Lizenztyp: {analyze_license(items[0]['html_url'])}",
                            f"Dateilink: {items[0]['html_url']}"]], "Programm beenden")
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
            printString.append([f"Lizenzdateiname: {item['name']}",
                                f"Lizenzdateipfad: {item['path']}",
                                f"Lizenztyp: {analyze_license(item['html_url'])}",
                                f"Dateilink: {item['html_url']}",
                                f"\n"])

        GUI.printText(printString, "Programm beenden")
        return


def main():
    info = GUI.query()

    if checkDone(info):
        return

    main_procedure(info[0], info[1])


main()
