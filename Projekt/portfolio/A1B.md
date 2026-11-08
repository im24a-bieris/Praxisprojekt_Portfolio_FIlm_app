# Kompetenzfeld: A1B

**Feature im Flask-Projekt:** Zusammenfassung der Filme (`/stats/total`)

## Kontext und Ziel
Die App soll anzeigen, wie viele Filme es gibt und was der Durchschnitt ist, z.B. "12 Filme, Durchschnitt 8.36".

## Konzept in eigenen Worten
Eine Prozedur macht etwas, z.B. etwas in die Konsole schreiben, gibt aber nichts zurück. Eine pure function gibt nur etwas zurück und ändert sonst nichts. Wenn ich sie zweimal mit dem gleichen Input aufrufe, kommt zweimal das Gleiche raus. Deshalb könnte man den Aufruf auch durch das Resultat ersetzen, das nennt man referentielle Transparenz.

## Umsetzung im Projekt
Ich habe die Zusammenfassung zweimal geschrieben. `print_summary` schreibt den Text mit `print` in die Konsole, das ist ein Seiteneffekt. `summary` gibt den Text nur zurück. Für die Route `/stats/total` geht nur `summary`, weil die Route den Text ins JSON packen muss. Bei OO wäre es eine Methode in einer Klasse, die auf die Daten vom Objekt zugreift.

## Code-Beispiel und Einordnung
```python
# A1B: Prozedur (Seiteneffekt print, kein Return)
def print_summary(movies: Movies) -> None:
    """Gibt eine Zusammenfassung auf der Konsole aus."""
    count = len(movies)
    average = average_rating(movies)
    print(f"{count} Filme, Durchschnitt {average:.2f}")


# A1B: pure function (gleicher Input, gleicher Output, kein Seiteneffekt)
def summary(movies: Movies) -> str:
    """Gibt die Zusammenfassung als Text zurueck."""
    return f"{len(movies)} Filme, Durchschnitt {average_rating(movies):.2f}"
```
Beide sind in `movies.py` (Zeilen 40–51). Man sieht den Unterschied schon an `-> None` und `-> str`.

## Pflicht-Artefakt
Prozedur `print_summary` und pure function `summary` nebeneinander (oben).

## Test und Überprüfung
- Test 1: `summary(load_movies())` -> "12 Filme, Durchschnitt 8.36" (-> grün)
- Test 2 (Edge Case): `summary(())` -> "0 Filme, Durchschnitt 0.00" (-> grün)

## Reflexion und Transfer
Die Prozedur zu testen war umständlich, ich musste die Ausgabe mit `capsys` abfangen. Die pure function konnte ich einfach mit `==` prüfen. Darum würde ich die Logik immer in pure functions schreiben.
