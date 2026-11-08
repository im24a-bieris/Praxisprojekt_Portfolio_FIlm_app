# Kompetenzfeld: B1B

**Feature im Flask-Projekt:** Datenteil `movies.py` (Filme laden, filtern, sortieren)

## Kontext und Ziel
Alle Routen holen die Daten aus `movies.py`. Diese Datei habe ich nach Functional Design aufgebaut.

## Konzept in eigenen Worten
Immutable Datentypen kann man nach dem Erstellen nicht mehr ändern. Ein Constructor erstellt einen neuen Wert. Ein composable Operator bekommt Filme und gibt wieder Filme zurück. Deshalb kann man mehrere davon hintereinander aufrufen.

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
`frozen=True` sorgt dafür, dass man einen Film nicht mehr ändern kann. Weil alle Operatoren ein Tuple bekommen und eins zurückgeben, kann ich sie verschachteln, z.B. `top_movies(filter_by_genre(load_movies(), "Action"), 3)`.

## Pflicht-Artefakt
Liste aller Elemente mit Fundort: `docs/functional_design.md`.

## Test und Überprüfung
- Test 1: `top_movies(filter_by_genre(load_movies(), "Action"), 3)` -> The Dark Knight, Gladiator, John Wick
- Test 2 (Edge Case): `MOVIES[0].rating = 1.0` -> Fehler, weil frozen (-> grün)

## Reflexion und Transfer
Am Anfang gaben meine Funktionen mal Listen, mal Tuples zurück. Erst als alle Tuples zurückgaben, liessen sie sich besser zusammenführen. Das Prinzip "gleicher Typ rein und raus" nehme ich mit.
