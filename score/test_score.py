# Unit Tests für score.py. Ausführen im Terminal mit: python test_score.py
# Ein bestandener assert gibt nichts aus. Ein falscher assert bricht mit AssertionError ab.

from score import berechne
from score import berechne_score
from score import bestimme_quadrant
from score import erstelle_begruendung
from score import ist_dringend
from score import sortiere_nach_score

# Feste Deadlines, damit die Tests an jedem Tag dasselbe Ergebnis liefern
VERGANGEN = "01.01.2000 12:00"   # schon vorbei, also immer dringend
ZUKUNFT = "01.01.2099 12:00"     # weit weg, also nie dringend wegen der Deadline


def loest_fehler_aus(aufgabe):
    # True, wenn berechne() für diese Aufgabe einen ValueError auslöst
    try:
        berechne(aufgabe)
    except ValueError:
        return True
    return False


# US-SC1: Kategorisierung

assert bestimme_quadrant(True, True) == 1
assert bestimme_quadrant(True, False) == 2
assert bestimme_quadrant(False, True) == 3
assert bestimme_quadrant(False, False) == 4

assert berechne({"wichtigkeit": 4, "dringlichkeit": "j", "deadline": ZUKUNFT})["quadrant"] == 1
assert berechne({"wichtigkeit": 4, "dringlichkeit": "n", "deadline": ZUKUNFT})["quadrant"] == 2
assert berechne({"wichtigkeit": 2, "dringlichkeit": "j", "deadline": ZUKUNFT})["quadrant"] == 3
assert berechne({"wichtigkeit": 1, "dringlichkeit": "n", "deadline": ZUKUNFT})["quadrant"] == 4

# Grenzwert Wichtigkeit: 3 ist wichtig, 2 nicht
assert berechne({"wichtigkeit": 3, "dringlichkeit": "n", "deadline": ZUKUNFT})["quadrant"] == 2
assert berechne({"wichtigkeit": 2, "dringlichkeit": "n", "deadline": ZUKUNFT})["quadrant"] == 4

# Grenzwert Deadline: genau 48 Stunden ist dringend, 49 nicht
assert ist_dringend("n", 24) == True
assert ist_dringend("n", 48) == True
assert ist_dringend("n", 49) == False
assert ist_dringend("j", 500) == True

# Gleiche Eingaben ergeben das gleiche Ergebnis, der Titel spielt keine Rolle
aufgabe_a = {"titel": "A", "wichtigkeit": 2, "dringlichkeit": "n", "deadline": ZUKUNFT}
aufgabe_b = {"titel": "B", "wichtigkeit": 2, "dringlichkeit": "n", "deadline": ZUKUNFT}
assert berechne(aufgabe_a) == berechne(aufgabe_b)


# US-SC2: Ungültige Eingaben

# Deadline in der Vergangenheit ist kein Fehler, sondern dringend
assert berechne({"wichtigkeit": 4, "dringlichkeit": "n", "deadline": VERGANGEN})["quadrant"] == 1

assert loest_fehler_aus({"wichtigkeit": 0, "dringlichkeit": "n", "deadline": ZUKUNFT})
assert loest_fehler_aus({"wichtigkeit": 7, "dringlichkeit": "n", "deadline": ZUKUNFT})
assert loest_fehler_aus({"wichtigkeit": "abc", "dringlichkeit": "n", "deadline": ZUKUNFT})
assert loest_fehler_aus({"wichtigkeit": "4", "dringlichkeit": "n", "deadline": ZUKUNFT})

assert loest_fehler_aus({"wichtigkeit": 4, "dringlichkeit": "x", "deadline": ZUKUNFT})

assert loest_fehler_aus({"wichtigkeit": 4, "dringlichkeit": "n"})
assert loest_fehler_aus({"wichtigkeit": 4, "dringlichkeit": "n", "deadline": ""})
assert loest_fehler_aus({"wichtigkeit": 4, "dringlichkeit": "n", "deadline": "20.11.2026"})
assert loest_fehler_aus({"wichtigkeit": 4, "dringlichkeit": "n", "deadline": "2026-11-20 17:00"})
assert loest_fehler_aus({"wichtigkeit": 4, "dringlichkeit": "n", "deadline": "31.02.2026 12:00"})
assert loest_fehler_aus({"wichtigkeit": 4, "dringlichkeit": "n", "deadline": "20.11.2026 25:00"})


# US-SC3: Nachvollziehbarer Score

assert berechne_score(5, True, 1) == 100     # höchster Score
assert berechne_score(1, False, 500) == 10   # tiefster Score
assert berechne_score(4, True, 24) == 90
assert berechne_score(3, False, 96) == 45    # Deadline in 4 Tagen

# Wichtigere Aufgabe und frühere Deadline geben einen höheren Score
assert berechne_score(5, False, 500) > berechne_score(3, False, 500)
assert berechne_score(4, True, 24) > berechne_score(4, True, 240)

assert erstelle_begruendung(4, True, 20.5) == "Wichtig (4/5), dringend (Deadline in 20 Stunden)"
assert erstelle_begruendung(2, False, 300) == "Nicht wichtig (2/5), nicht dringend (Deadline in 300 Stunden)"
assert berechne({"wichtigkeit": 5, "dringlichkeit": "n", "deadline": VERGANGEN})["begruendung"] == "Wichtig (5/5), dringend (Deadline überschritten)"

liste = [{"titel": "B", "score": 30}, {"titel": "A", "score": 90}, {"titel": "C", "score": 60}]
sortiert = sortiere_nach_score(liste)
assert sortiert[0]["titel"] == "A"
assert sortiert[1]["titel"] == "C"
assert sortiert[2]["titel"] == "B"
assert liste[0]["titel"] == "B"   # die ursprüngliche Liste bleibt unverändert

print("Alle Tests bestanden.")
