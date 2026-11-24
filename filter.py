from datetime import datetime
from score.score import lese_deadline



def filter_nach_quadrant(aufgaben):
    """Filtert Aufgaben nach einem gewählten Eisenhower-Quadranten."""
    gefilterte_aufgaben = []

    while True:
        
        eingabe = input("Welcher Quadrant soll angezeigt werden? (1-4):" )

        if eingabe in ["1", "2", "3", "4"]:
            gewählter_quadrant = int(eingabe)
            break
        else:
            print ("Ungültige Eingabe")

    for aufgabe in aufgaben:
        if aufgabe["quadrant"] == gewählter_quadrant:
            gefilterte_aufgaben.append(aufgabe)
    gefilterte_aufgaben = sorted(gefilterte_aufgaben, key=lambda aufgabe: aufgabe["score"], reverse=True)

    if len(gefilterte_aufgaben) == 0:
        print("Keine Aufgaben gefunden")
        return
    else:
        return gefilterte_aufgaben



def filter_nach_stichwort(aufgaben):
    """Filtert Aufgaben nach einem Stichwort im Titel oder in der Kurzbeschreibung."""
    gefilterte_aufgaben = []

    eingabe = input("Nach welchem Stichwort soll gefiltert werden? ").lower()
    
    for aufgabe in aufgaben:
        if eingabe in aufgabe["titel"].lower() or eingabe in aufgabe["kurzbeschreibung"].lower():
            gefilterte_aufgaben.append(aufgabe)

    if len(gefilterte_aufgaben) == 0:
        print("Keine Aufgaben gefunden")

    return gefilterte_aufgaben



def filter_nach_deadline(aufgaben):
    gefilterte_aufgaben = []

    eingabe = input("1 = überfällige Aufgaben, 2 = Aufgaben bis zu einem bestimmten Datum: ")

    if eingabe == "1":
        aktueller_zeitpunkt = datetime.now()

        for aufgabe in aufgaben:
            deadline = lese_deadline(aufgabe["deadline"])

            if aufgabe["status"] == "offen" and deadline < aktueller_zeitpunkt:
                gefilterte_aufgaben.append(aufgabe)

    elif eingabe == "2":
        datum = input("Bis zu welchem Datum soll gefiltert werden? (TT.MM.JJJJ): ")
        