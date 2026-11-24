from pathlib import Path

BENOETIGTE_DATEIEN = [
    "score/score.py",
    "frontend.py",
]


def fehlende_dateien():
    """Gibt eine Liste aller benötigten Dateien zurück, die fehlen."""
    fehlend = []
    for datei in BENOETIGTE_DATEIEN:
        if not Path(datei).exists():
            fehlend.append(datei)
    return fehlend


def main():
    fehlend = fehlende_dateien()
    if len(fehlend) > 0:
        print("Das Programm kann nicht starten. Folgende Dateien fehlen:")
        for datei in fehlend:
            print("-", datei)
        return



from score.score import lese_deadline, berechne

def frage_titel():
    """Fragt den Titel einer neuen Aufgabe ab."""

    while True:
        titel = input("Titel der Aufgabe: ").strip()

        if titel != "":
            return titel

        print("Bitte gib einen Titel ein.")


def frage_kurzbeschreibung():
    """Fragt eine optionale Kurzbeschreibung ab."""
    beschreibung = input("Kurzbeschreibung (optional): ").strip()
    return beschreibung




def frage_wichtigkeit():
    """Fragt die Wichtigkeit einer Aufgabe von 1 bis 5 ab."""

    while True:
        eingabe = input("Wichtigkeit (1 bis 5, ? für Hilfe): ").strip()

        if eingabe == "?":
            print("1 = Sehr wenig wichtig")
            print("2 = Eher wenig wichtig")
            print("3 = Mittelmässig wichtig")
            print("4 = Wichtig")
            print("5 = Sehr wichtig")

        else:
            try:
                wichtigkeit = int(eingabe)

                if 1 <= wichtigkeit <= 5:
                    return wichtigkeit

                print("Bitte gib eine Zahl zwischen 1 und 5 ein.")

            except ValueError:
                print("Ungültige Eingabe. Bitte gib eine ganze Zahl ein.")



def frage_dringlichkeit():
    """Fragt die Dringlichkeit einer Aufgabe ab."""

    while True:
        dringlichkeit = input(
            "Ist die Aufgabe dringend? (j/n, ? für Hilfe): "
        ).strip().lower()

        if dringlichkeit == "?":
            print("Dringend bedeutet, dass eine Aufgabe zeitnah erledigt werden muss.")

        elif dringlichkeit in ["j", "n"]:
            return dringlichkeit

        else:
            print("Ungültige Eingabe. Bitte j, n oder ? eingeben.")


def frage_deadline():
    """Fragt die Deadline einer Aufgabe ab."""

    while True:
        eingabe = input("Deadline (TT.MM.JJJJ HH:MM): ").strip()

        try:
            lese_deadline(eingabe)
            return eingabe

        except ValueError:
            print("Ungültige Deadline. Bitte Datum und Uhrzeit korrekt eingeben.")

if __name__ == "__main__":
    titel = frage_titel()
    beschreibung = frage_kurzbeschreibung()
    wichtigkeit = frage_wichtigkeit()
    dringlichkeit = frage_dringlichkeit()
    deadline = frage_deadline()
    aufgabe = {
        "titel": titel,
        "kurzbeschreibung": beschreibung,
        "wichtigkeit": wichtigkeit,
        "dringlichkeit": dringlichkeit,
        "deadline": deadline
    }
    while True:
        ergebnis = berechne(aufgabe)
        print("Erfasster Titel:", aufgabe["titel"])
        print("Erfasste Kurzbeschreibung:", aufgabe["kurzbeschreibung"])
        print("Erfasste Wichtigkeit:", aufgabe["wichtigkeit"])
        print("Erfasste Dringlichkeit:", aufgabe["dringlichkeit"])
        print("Erfasste Deadline:", aufgabe["deadline"])
        print("Quadrant:", ergebnis["quadrant"])
        print("Score:", ergebnis["score"])
        print("Begründung:", ergebnis["begruendung"])
        while True:
            auswahl = input(
                "Aufgabe bestätigen (b), korrigieren (k) oder verwerfen (v)? "
            ).strip().lower()

            if auswahl in ["b", "k", "v"]:
                break

            print("Ungültige Eingabe. Bitte b, k oder v eingeben.")

        if auswahl == "b":
            print("Aufgabe bestätigt.")
            break

        elif auswahl == "v":
            print("Aufgabe verworfen.")
            break

        elif auswahl == "k":
            print("Aufgabe korrigieren.")
            print("Was möchtest du korrigieren?")
            print("1 = Titel")
            print("2 = Kurzbeschreibung")
            print("3 = Wichtigkeit")
            print("4 = Dringlichkeit")
            print("5 = Deadline")

        feld = input("Bitte wähle eine Zahl von 1 bis 5: ").strip()
        
        if feld == "1":
            titel = frage_titel()
            aufgabe["titel"] = titel
            print("Titel wurde korrigiert.")
        elif feld == "2":
            beschreibung = frage_kurzbeschreibung()
            aufgabe["kurzbeschreibung"] = beschreibung
            print("Kurzbeschreibung wurde korrigiert.")
        elif feld == "3":
            wichtigkeit = frage_wichtigkeit()
            aufgabe["wichtigkeit"] = wichtigkeit
            print("Wichtigkeit wurde korrigiert.")
        elif feld == "4":
            dringlichkeit = frage_dringlichkeit()
            aufgabe["dringlichkeit"] = dringlichkeit
            print("Dringlichkeit wurde korrigiert.")
        elif feld == "5":
            deadline = frage_deadline()
            aufgabe["deadline"] = deadline
            print("Deadline wurde korrigiert.")
        else:
            print("Ungültige Auswahl. Bitte eine Zahl von 1 bis 5 eingeben.")
        
        ergebnis = berechne(aufgabe)
        print("Neuer Quadrant:", ergebnis["quadrant"])
        print("Neuer Score:", ergebnis["score"])
        print("Neue Begründung:", ergebnis["begruendung"])
