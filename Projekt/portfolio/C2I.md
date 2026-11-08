# Kompetenzfeld: C2I

**Feature im Flask-Projekt:** Empfehlungen (`/movies/recommend`)

## Kontext und Ziel
Die App soll Filme empfehlen, die gut bewertet sind (ab 8.0) und nicht zu alt (ab 2000). Das Resultat ist eine Liste wie "Inception (2010)", der beste Film zuerst. Das ist ein anderes Feature als bei C2B und C2A.

## Konzept in eigenen Worten
Ein Lambda ist eine kleine Funktion ohne Namen. Man schreibt sie direkt dort, wo man sie braucht. Verketten heisst: Das Resultat von einem Schritt geht direkt in den nächsten, wie bei einem Fliessband.

## Umsetzung im Projekt
Die Kette in `recommend` hat drei Schritte. `filter` behält nur gute und neue Filme. `sorted` ordnet nach Bewertung, die beste zuerst. `map` macht aus jedem Film den Text "Titel (Jahr)". Alle drei benutzen ein Lambda. Ich sortiere vor `map`, weil es nach `map` nur noch Texte gibt. Dann könnte man nicht mehr nach Bewertung sortieren.

## Code-Beispiel und Einordnung
```python
# C2I: Lambda und verkettetes filter -> sorted -> map
def recommend(movies: Movies, min_rating: float = 8.0, min_year: int = 2000) -> tuple[str, ...]:
    """Empfehlungen als 'Titel (Jahr)', beste Bewertung zuerst."""
    good = filter(lambda m: m.rating >= min_rating and m.year >= min_year, movies)
    ordered = sorted(good, key=lambda m: (-m.rating, m.title))
    return tuple(map(lambda m: f"{m.title} ({m.year})", ordered))
```
Der Code steht in `movies.py` (Zeilen 193–198). Jeder Zwischenschritt hat einen Namen (`good`, `ordered`). So kann man die Kette gut lesen.

## Pflicht-Artefakt
Lambdas in `filter`, `sorted` und `map`, verkettet zu einem Ablauf (oben).

## Test und Überprüfung
- Test 1: `recommend(MOVIES)` -> "The Dark Knight (2008)", "Inception (2010)", "Interstellar (2014)", ... (-> grün)
- Test 2 (Edge Case): leere Liste -> `()` (-> grün)
- Test 3 (Edge Case): Mindestbewertung 9.5 -> `()` (-> grün)

## Reflexion und Transfer
Am Anfang stand alles in einer langen Zeile. Das war schwer zu lesen. Mit Zwischenvariablen ist es klarer. Ein Lambda ist hier gut, weil die Bedingungen kurz sind. Wenn ich eine Bedingung an mehreren Orten brauche, nehme ich lieber eine Funktion mit Namen.
