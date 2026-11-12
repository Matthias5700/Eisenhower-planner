# Eisenhower-planner

## Worum geht es?

Die Eisenhower-Matrix teilt Aufgaben nach zwei Fragen ein: *Ist die Aufgabe wichtig?* und *Ist sie dringend?* Daraus ergeben sich vier Quadranten:

|  | **dringend** | **nicht dringend** |
|---|---|---|
| **wichtig** | **Q1** Sofort erledigen | **Q2** Planen |
| **nicht wichtig** | **Q3** Delegieren | **Q4** Eliminieren |

Die App führt den Benutzer im Terminal Schritt für Schritt durch die Erfassung einer Aufgabe. Danach ordnet sie die Aufgabe automatisch einem Quadranten zu und berechnet einen Score für die Priorisierung.

## Funktionen

- **Aufgaben erfassen**: geführter Dialog mit Titel, Kurzbeschreibung, Wichtigkeit (1–5), Dringlichkeit (j/n) und Deadline (Datum und Uhrzeit), inklusive Hilfetexten und Eingabeprüfung
- **Automatische Einteilung**: Quadrant, Score (0–100) und eine kurze Begründung für jede Aufgabe
- **Aufgaben verwalten**: Angaben vor dem Speichern prüfen und korrigieren; bestehende Aufgaben bearbeiten, löschen oder als erledigt markieren
- **Filtern**: nach Quadrant, nach Deadline (überfällig oder bis zu einem Datum) und nach Stichwort
- **Speichern**: alle Aufgaben werden automatisch in `aufgaben.json` gespeichert und beim nächsten Start wieder geladen
- **Kalender**: Aufgaben als `.ics`-Datei exportieren (z. B. für Apple Kalender, Google Calendar oder Outlook) und `.ics`-Dateien importieren

## Team und Teilbereiche

| Teilbereich | Verantwortlich | User Stories |
|---|---|---|
| Frontend (Dialog mit dem Benutzer) | Alice | US-FE1 bis US-FE3 |
| Scoreberechnung | Matthias | US-SC1 bis US-SC3 |
| Filter | Nikola | US-FI1 bis US-FI3 |
| Kalender und Datenspeicherung | Huy | US-KA1 bis US-KA4 |

## Installation und Start

Voraussetzung ist Python 3. Zusätzliche Pakete werden nicht benötigt.

```bash
python main.py
```

---

## Scoreberechnung (`score.py`)

Die Scoreberechnung ist der «Rechenkern» der App. Sie bekommt eine Aufgabe und gibt zurück, **in welchen Quadranten** sie gehört, **wie hoch ihr Score** ist und **warum**. Sie fragt nichts ab, liest keine Dateien und gibt nichts auf der Konsole aus. Dadurch lässt sie sich unabhängig vom Rest der App testen.

### Verwendung

```python
from score import berechne

aufgabe = {"titel": "Projektarbeit", "wichtigkeit": 4, "dringlichkeit": "n", "deadline": "06.12.2026 23:55"}

try:
    aufgabe.update(berechne(aufgabe))
except ValueError as fehler:
    print(fehler)

# aufgabe enthält jetzt zusätzlich:
# "quadrant": 2, "score": 40, "begruendung": "Wichtig (4/5), nicht dringend (Deadline in 585 Stunden)"
```

### So wird gerechnet

1. **Wichtig** ist eine Aufgabe ab Wichtigkeit **3** (Skala 1–5).
2. **Dringend** ist eine Aufgabe, wenn der Benutzer «j» eingegeben hat **oder** die Deadline in **höchstens 48 Stunden** erreicht oder schon vorbei ist.
3. Daraus folgt der **Quadrant** (siehe Tabelle oben).
4. Der **Score** wird zusammengezählt:

| Teil | Punkte |
|---|---|
| Wichtigkeit × 10 | 10–50 |
| + dringend | 20 |
| + Deadline in ≤ 48 Stunden | 30 |
| + Deadline in ≤ 7 Tagen | 15 |

Beispiel: Wichtigkeit 4, Dringlichkeit «n», Deadline in 24 Stunden ergibt Quadrant 1 und einen Score von 40 + 20 + 30 = **90**.

### Fehlerbehandlung

Bei ungültigen Eingaben (z. B. Wichtigkeit 7, Dringlichkeit «x», Deadline ohne Uhrzeit oder 31.02.) löst `berechne()` einen `ValueError` mit einer verständlichen Meldung aus. Das Frontend fängt diesen Fehler ab und zeigt die Meldung an.

### Tests

```bash
python test_score.py
```

Die Tests prüfen alle vier Quadranten, die Grenzwerte (Wichtigkeit 3, Deadline genau 48 Stunden), alle Fehlerfälle und die Score-Berechnung. Wenn alles stimmt, erscheint `Alle Tests bestanden.`
