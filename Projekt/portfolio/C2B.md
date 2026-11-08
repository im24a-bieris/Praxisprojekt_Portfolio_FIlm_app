# Kompetenzfeld: C2B

**Feature im Flask-Projekt:** Suche und Filter (`/movies?q=...&genre=...&sort=...`)

## Kontext und Ziel
Man soll Filme nach Titel, Genre und Jahr filtern und sortieren können. Die Filter kann man kombinieren.

## Konzept in eigenen Worten
In Python ist eine Funktion auch ein Wert. Man kann sie in eine Variable speichern und weitergeben. `map` macht etwas mit jedem Element. `filter` behält nur passende Elemente. `reduce` macht aus allen Elementen einen einzigen Wert.

## Umsetzung im Projekt
Für jede Operation gibt es eine kleine Funktion in `movies.py`. Die Route holt die passende Sortier-Funktion in die Variable `scorer` und gibt sie an `sort_by` weiter.

## Code-Beispiel und Einordnung
```python
def titles(movies: Movies) -> tuple[str, ...]:
    """Gibt nur die Titel zurueck."""
    return tuple(map(lambda m: m.title, movies))


# C2B: reduce
def total_rating(movies: Movies) -> float:
    """Summe aller Bewertungen (reduce)."""
    return reduce(lambda acc, m: acc + m.rating, movies, 0.0)
```
Das zeigt `map` und `reduce` (`movies.py`, Zeilen 73–81). Die Funktion in einer Variable steht in `app.py` in `get_movies`.

## Pflicht-Artefakt
- Variable: `scorer = rating_of`, dann `sort_by(MOVIES, scorer)` -> John Wick zuerst
- filter: `filter_by_genre(MOVIES, "Action")` -> 3 Filme
- map: `titles(MOVIES)` -> "Inception", "The Dark Knight", ...
- reduce: `total_rating(MOVIES)` -> 100.3

## Test und Überprüfung
- Test 1: `/movies?q=the&genre=action` -> nur The Dark Knight (-> grün)
- Test 2 (Edge Case): Genre "Unbekannt" -> `()` (-> grün)

## Reflexion und Transfer
Zuerst habe ich `rating_of()` mit Klammern geschrieben. Damit habe ich die Funktion aufgerufen, statt sie weiterzugeben.
