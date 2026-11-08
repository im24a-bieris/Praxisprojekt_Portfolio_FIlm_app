# Kompetenzfeld: A1B

**Feature im Flask-Projekt:** Zusammenfassung der Filme (`/stats/total`)

## Kontext und Ziel
Die App soll zeigen, wie viele Filme es gibt und wie gut sie im Schnitt sind, zum Beispiel "12 Filme, Durchschnitt 8.36".

## Konzept in eigenen Worten
Eine Prozedur macht etwas, zum Beispiel etwas auf der Konsole ausgeben, und gibt nichts zurück. Eine pure function gibt nur ein Resultat zurück und ändert sonst nichts. Gleicher Input gibt immer gleichen Output. Darum kann man den Aufruf durch sein Resultat ersetzen. Das nennt man referentielle Transparenz.

## Umsetzung im Projekt
Ich habe dieselbe Aufgabe zweimal gebaut. `print_summary` gibt den Text mit `print` aus, das ist ein Seiteneffekt. `summary` gibt den Text zurück. In der Route kann ich nur `summary` brauchen, weil die Route einen Wert für das JSON braucht. In OO wäre das eine Methode, die mit den Daten im Objekt arbeitet.

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
Beide stehen in `movies.py` (Zeilen 40–51). Den Unterschied sieht man schon an `-> None` und `-> str`.

## Pflicht-Artefakt
Prozedur `print_summary` und pure function `summary` nebeneinander (oben).

## Test und Überprüfung
- Test 1: `summary(load_movies())` -> "12 Filme, Durchschnitt 8.36" (-> grün)
- Test 2 (Edge Case): `summary(())` -> "0 Filme, Durchschnitt 0.00" (-> grün)

## Reflexion und Transfer
Die Prozedur war schwer zu testen, die pure function ganz einfach. Nächstes Mal schreibe ich zuerst pure functions.
