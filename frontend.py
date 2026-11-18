def frage_titel():
    """Fragt den Titel einer neuen Aufgabe ab."""

    while True:
        titel = input("Titel der Aufgabe: ").strip()

        if titel != "":
            return titel

        print("Bitte gib einen Titel ein.")


if __name__ == "__main__":
    titel = frage_titel()
    print("Erfasster Titel:", titel)