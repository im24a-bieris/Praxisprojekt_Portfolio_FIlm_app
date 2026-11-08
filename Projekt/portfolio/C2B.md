# Kompetenzfeld: C2B

**Feature im Flask-Projekt:** Suche und Filter (`/movies?q=...&genre=...&sort=...`)

## Kontext und Ziel
Man kann Filme nach Titel, Genre und Jahr filtern und sortieren. Die Filter kann man auch kombinieren.

## Konzept in eigenen Worten
In Python ist eine Funktion auch ein Wert, man kann sie in eine Variable speichern und weitergeben. `map` macht etwas mit jedem Element, `filter` behält nur die passenden und `reduce` macht aus allen zusammen einen Wert.

## Umsetzung im Projekt
Für jede Operation gibt es eine kleine Funktion in `movies.py`. In der Route wird die passende Sortierfunktion in der Variable `scorer` gespeichert und an `sort_by` weitergegeben.

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
Hier sieht man `map` und `reduce` (`movies.py`, Zeilen 73–81). Die Funktion in der Variable ist in `app.py` in `get_movies`.

## Pflicht-Artefakt
- Variable: `scorer = rating_of`, dann `sort_by(MOVIES, scorer)` -> John Wick zuerst
- filter: `filter_by_genre(MOVIES, "Action")` -> 3 Filme
- map: `titles(MOVIES)` -> "Inception", "The Dark Knight", ...
- reduce: `total_rating(MOVIES)` -> 100.3

## Test und Überprüfung
- Test 1: `/movies?q=the&genre=action` -> nur The Dark Knight (-> grün)
- Test 2 (Edge Case): Genre "Unbekannt" -> `()` (-> grün)

## Reflexion und Transfer
Man muss aufpassen, dass man `rating_of` ohne Klammern weitergibt. Mit `rating_of()` würde man die Funktion aufrufen, statt sie weiterzugeben.
