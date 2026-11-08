# Kompetenzfeld: C2I

**Feature im Flask-Projekt:** Empfehlungen (`/movies/recommend`)

## Kontext und Ziel
Die App soll Filme empfehlen, die gut bewertet (ab 8.0) und nicht zu alt (ab 2000) sind. Raus kommt eine Liste wie "Inception (2010)", der beste zuerst. Das ist ein anderes Feature als bei C2B und C2A.

## Konzept in eigenen Worten
Ein Lambda ist eine kleine Funktion ohne Namen, die man direkt dort hinschreibt, wo man sie braucht. Beim Verketten geht das Resultat von einem Schritt direkt in den nächsten Schritt.

## Umsetzung im Projekt
`recommend` hat drei Schritte. `filter` behält nur gute und neue Filme, `sorted` sortiert nach Bewertung und `map` macht aus jedem Film den Text "Titel (Jahr)". Alle drei brauchen ein Lambda. Ich sortiere vor dem `map`, weil danach nur noch Text da ist und man nicht mehr nach Bewertung sortieren kann.

## Code-Beispiel und Einordnung
```python
# C2I: Lambda und verkettetes filter -> sorted -> map
def recommend(movies: Movies, min_rating: float = 8.0, min_year: int = 2000) -> tuple[str, ...]:
    """Empfehlungen als 'Titel (Jahr)', beste Bewertung zuerst."""
    good = filter(lambda m: m.rating >= min_rating and m.year >= min_year, movies)
    ordered = sorted(good, key=lambda m: (-m.rating, m.title))
    return tuple(map(lambda m: f"{m.title} ({m.year})", ordered))
```
Der Code ist in `movies.py` (Zeilen 193–198). Die Zwischenschritte haben Namen (`good`, `ordered`), damit man die Kette besser lesen kann.

## Pflicht-Artefakt
Lambdas in `filter`, `sorted` und `map`, verkettet zu einem Ablauf (oben).

## Test und Überprüfung
- Test 1: `recommend(MOVIES)` -> "The Dark Knight (2008)", "Inception (2010)", "Interstellar (2014)", ... (-> grün)
- Test 2 (Edge Case): leere Liste -> `()` (-> grün)
- Test 3 (Edge Case): Mindestbewertung 9.5 -> `()` (-> grün)

## Reflexion und Transfer
In einer einzigen Zeile wäre die Kette schwer zu lesen, darum habe ich Zwischenvariablen benutzt. Lambdas passen hier, weil die Bedingungen kurz sind und nur einmal gebraucht werden. Wenn ich die gleiche Bedingung an mehreren Orten brauche, ist eine normale Funktion mit Namen besser, wie `is_highlight` beim Refactoring.
