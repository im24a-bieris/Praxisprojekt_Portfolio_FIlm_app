# Kompetenzfeld: B1B

**Feature im Flask-Projekt:** Datenteil `movies.py` (Filme laden, filtern, sortieren)

## Kontext und Ziel
Alle Routen holen ihre Daten aus `movies.py`. Ich wollte, dass diese Datei nach Functional Design gebaut ist.

## Konzept in eigenen Worten
Immutable Datentypen kann man nach dem Erstellen nicht mehr ändern. Ein Constructor baut einen neuen Wert. Ein composable Operator bekommt Filme und gibt wieder Filme zurück. Darum kann man mehrere hintereinander hängen, wie Lego-Steine.

## Umsetzung im Projekt
- Immutable: `Movie` ist eine frozen dataclass (`movies.py`, Zeilen 7–14). Alle Funktionen geben Tuples zurück.
- Constructors: `Movie(...)`, `load_movies()` (Zeilen 21–37), `add_movie`, `rate_movie`.
- Composable Operators: `filter_by_genre`, `search_title`, `filter_by_years`, `top_movies`, `rank_movies`.

## Code-Beispiel und Einordnung
```python
@dataclass(frozen=True)
class Movie:
    """Ein Film (unveraenderlich)."""
    id: int
    title: str
    genre: str
    year: int
    rating: float
```
`frozen=True` macht den Film unveränderlich. Weil alle Operatoren ein Tuple bekommen und zurückgeben, geht zum Beispiel `top_movies(filter_by_genre(load_movies(), "Action"), 3)`.

## Pflicht-Artefakt
Liste aller Elemente mit Fundort: `docs/functional_design.md`.

## Test und Überprüfung
- Test 1: `top_movies(filter_by_genre(load_movies(), "Action"), 3)` -> The Dark Knight, Gladiator, John Wick
- Test 2 (Edge Case): `MOVIES[0].rating = 1.0` -> Fehler, weil frozen (-> grün)

## Reflexion und Transfer
Am Anfang gaben meine Funktionen mal Listen, mal Tuples zurück. Erst als alle Tuples zurückgaben, konnte ich sie gut verbinden.
