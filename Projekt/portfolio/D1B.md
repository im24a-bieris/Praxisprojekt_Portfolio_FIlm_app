# Kompetenzfeld: D1B

**Feature im Flask-Projekt:** Highlights (`/movies/highlights`), `load_movies` und `best_rating`

## Kontext und Ziel
Die Funktion für die Highlights war zuerst unordentlich, mit zwei Schleifen und verschachtelten `if`. Ich habe sie aufgeräumt, ohne dass sich das Resultat ändert. Dazu habe ich zwei Stellen schneller gemacht.

## Konzept in eigenen Worten
Refactoring heisst: Code besser lesbar machen, ohne dass sich das Resultat ändert. Die Tests müssen vorher und nachher grün sein.

## Umsetzung im Projekt
1. Extract Function: Die Bedingung und der Text sind jetzt eigene Funktionen (`is_highlight`, `highlight_label`). So sind sie einzeln testbar.
2. Rename: `process` heisst jetzt `highlights`, `tmp` heisst `selected`. So sagt der Name, was die Funktion macht.
3. Replace Loop with Pipeline: Die Schleifen sind durch `filter`, `sorted` und `map` ersetzt. Es braucht keine Hilfslisten mehr.

Performance 1: `lru_cache` auf `load_movies`, die Filme werden nur einmal gebaut. Performance 2: Generator statt Liste in `best_rating`, so entsteht keine extra Liste im Speicher.

## Code-Beispiel und Einordnung
```python
def highlights(movies: Movies) -> tuple[str, ...]:
    """Highlights als Text, aelteste zuerst."""
    return tuple(map(highlight_label, sorted(filter(is_highlight, movies), key=year_of)))
```
Das ist das Resultat der drei Techniken (`movies.py`, Zeilen 235–237).

## Pflicht-Artefakt
Drei Techniken und zwei Performance-Massnahmen, je mit Zweck (oben).

## Test und Überprüfung
- Test 1: `highlights(MOVIES)` beginnt mit "FORREST GUMP (Drama)" (-> grün)
- Test 2: `load_movies() is load_movies()` -> True, der Cache funktioniert (-> grün)

## Reflexion und Transfer
Mit Cache sind 10000 Aufrufe viel schneller (0.278 ms statt 43.677 ms).
