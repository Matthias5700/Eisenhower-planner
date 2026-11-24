# Scoreberechnung (US-SC1 bis US-SC3)
# Ordnet eine Aufgabe einem Eisenhower-Quadranten zu und berechnet einen Score von 0 bis 100.
# Die Funktionen geben nichts auf der Konsole aus. Fehler werden als ValueError gemeldet.

from datetime import datetime

QUADRANTEN = {
    1: "Sofort erledigen",
    2: "Planen",
    3: "Delegieren",
    4: "Eliminieren",
}


def pruefe_wichtigkeit(wichtigkeit):
    # Nur ganze Zahlen von 1 bis 5 sind erlaubt (also nicht "abc", 0 oder 7)
    if type(wichtigkeit) != int or wichtigkeit < 1 or wichtigkeit > 5:
        raise ValueError("Die Wichtigkeit muss eine ganze Zahl von 1 bis 5 sein.")


def pruefe_dringlichkeit(dringlichkeit):
    if dringlichkeit != "j" and dringlichkeit != "n":
        raise ValueError("Die Dringlichkeit muss j oder n sein.")


def lese_deadline(text):
    # Wandelt den Text "TT.MM.JJJJ HH:MM" in ein Datum mit Uhrzeit um
    fehlermeldung = "Die Deadline muss im Format TT.MM.JJJJ HH:MM angegeben werden."
    if type(text) != str:
        raise ValueError(fehlermeldung)
    try:
        datum, zeit = text.split(" ")           # "20.11.2026" und "17:00"
        tag, monat, jahr = datum.split(".")     # "20", "11", "2026"
        stunde, minute = zeit.split(":")        # "17", "00"
        return datetime(int(jahr), int(monat), int(tag), int(stunde), int(minute))
    except ValueError:
        raise ValueError(fehlermeldung)


def stunden_bis(deadline):
    # Negativ, wenn die Deadline schon vorbei ist
    differenz = deadline - datetime.now()
    return differenz.total_seconds() / 3600


def ist_dringend(dringlichkeit, stunden):
    # Dringend, wenn der Benutzer "j" sagt oder die Deadline in höchstens 48 Stunden ist
    return dringlichkeit == "j" or stunden <= 48


def bestimme_quadrant(wichtig, dringend):
    if wichtig and dringend:
        return 1
    if wichtig:
        return 2
    if dringend:
        return 3
    return 4


def berechne_score(wichtigkeit, dringend, stunden):
    score = wichtigkeit * 10  # 10 bis 50 Punkte
    if dringend:
        score = score + 20
    if stunden <= 48:
        score = score + 30
    elif stunden <= 7 * 24:
        score = score + 15
    return score  # höchstens 50 + 20 + 30 = 100


def erstelle_begruendung(wichtigkeit, dringend, stunden):
    if wichtigkeit >= 3:
        teil_wichtig = "Wichtig"
    else:
        teil_wichtig = "Nicht wichtig"

    if dringend:
        teil_dringend = "dringend"
    else:
        teil_dringend = "nicht dringend"

    if stunden < 0:
        teil_deadline = "Deadline überschritten"
    else:
        teil_deadline = f"Deadline in {int(stunden)} Stunden"

    return f"{teil_wichtig} ({wichtigkeit}/5), {teil_dringend} ({teil_deadline})"


def berechne(aufgabe):
    # Hauptfunktion für das Frontend und den Kalender.
    # Erwartet eine Aufgabe als Dictionary gemäss Datenmodell und gibt
    # Quadrant, Score und Begründung als Dictionary zurück.
    pruefe_wichtigkeit(aufgabe.get("wichtigkeit"))
    pruefe_dringlichkeit(aufgabe.get("dringlichkeit"))
    deadline = lese_deadline(aufgabe.get("deadline"))

    wichtigkeit = aufgabe["wichtigkeit"]
    stunden = stunden_bis(deadline)
    wichtig = wichtigkeit >= 3
    dringend = ist_dringend(aufgabe["dringlichkeit"], stunden)

    return {
        "quadrant": bestimme_quadrant(wichtig, dringend),
        "score": berechne_score(wichtigkeit, dringend, stunden),
        "begruendung": erstelle_begruendung(wichtigkeit, dringend, stunden),
    }


def sortiere_nach_score(aufgaben):
    # Gibt eine neue Liste zurück, höchster Score zuerst.
    # Sucht immer die Aufgabe mit dem höchsten Score im Rest und hängt sie hinten an.
    rest = list(aufgaben)
    sortiert = []
    while len(rest) > 0:
        beste = rest[0]
        for aufgabe in rest:
            if aufgabe["score"] > beste["score"]:
                beste = aufgabe
        sortiert.append(beste)
        rest.remove(beste)
    return sortiert
