# Kompetenzfeld: D1B

**Feature im Flask-Projekt:** Highlights (`/movies/highlights`), `load_movies` und `best_rating`

## Kontext und Ziel
Die Funktion für die Highlights war zuerst unübersichtlich, mit zwei Schleifen und verschachtelten `if`. Ich habe sie aufgeräumt, ohne das Resultat zu ändern. Ausserdem habe ich zwei Sachen schneller gemacht.

## Konzept in eigenen Worten
Beim Refactoring mache ich den Code besser lesbar, aber das Resultat bleibt gleich. Die Tests müssen vorher und nachher grün sein.

## Umsetzung im Projekt
1. Extract Function: Die Bedingung und der Text sind jetzt eigene Funktionen (`is_highlight`, `highlight_label`), damit man sie einzeln testen kann.
2. Rename: `process` heisst jetzt `highlights` und `tmp` heisst `selected`. Jetzt sieht man am Namen, was passiert.
3. Replace Loop with Pipeline: Statt Schleifen benutze ich `filter`, `sorted` und `map`, so braucht es keine Hilfslisten.

Performance 1: `lru_cache` auf `load_movies`, damit die Filme nur einmal erstellt werden. Performance 2: In `best_rating` ein Generator statt einer Liste, so wird keine extra Liste im Speicher gemacht.

## Code-Beispiel und Einordnung
```python
def highlights(movies: Movies) -> tuple[str, ...]:
    """Highlights als Text, aelteste zuerst."""
    return tuple(map(highlight_label, sorted(filter(is_highlight, movies), key=year_of)))
```
So sieht die Funktion nach den drei Schritten aus (`movies.py`, Zeilen 235–237).

## Pflicht-Artefakt
Drei Techniken und zwei Performance-Massnahmen, je mit Zweck (oben).

## Test und Überprüfung
- Test 1: `highlights(MOVIES)` beginnt mit "FORREST GUMP (Drama)" (-> grün)
- Test 2: `load_movies() is load_movies()` -> True, der Cache funktioniert (-> grün)

## Reflexion und Transfer
Mit dem Cache sind 10000 Aufrufe viel schneller (0.278 ms statt 43.677 ms). Das geht aber nur, weil die Filme unveränderlich sind.
