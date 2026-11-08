# Kompetenzfeld: B1A

**Feature im Flask-Projekt:** Top-Liste (`/movies/top?n=5`)

## Kontext und Ziel
Die Route `/movies/top` gibt die n besten Filme zurück. Ich habe sie zuerst imperativ geschrieben, dann deklarativ, und danach beide verglichen.

## Konzept in eigenen Worten
Imperativ beschreibe ich jeden Schritt selbst: in einer Schleife den besten Film suchen, rausnehmen und das wiederholen. Deklarativ sage ich nur, was ich haben will, also nach Bewertung sortiert und davon die ersten n. Wie das genau passiert, macht Python.

## Umsetzung im Projekt
`top_movies_imperative` hat zwei Schleifen, ein `if` und zwei Hilfslisten. `top_movies` ist nur eine Zeile mit `sorted`. Die Route benutzt `top_movies`. Beim Testen kam heraus, dass `[:n]` bei einem negativen n Filme hinten abschneidet, statt nichts zurückzugeben. Deshalb steht dort `max(n, 0)`.

## Code-Beispiel und Einordnung
```python
# B1A: imperative Variante (Schleife, Hilfsliste, if)
def top_movies_imperative(movies: Movies, n: int) -> Movies:
    """Die n besten Filme, imperativ."""
    remaining = list(movies)
    result = []
    while remaining and len(result) < n:
        best = remaining[0]
        for movie in remaining:
            if movie.rating > best.rating:
                best = movie
        result.append(best)
        remaining.remove(best)
    return tuple(result)


# B1A: deklarative Variante (wird von der Route benutzt)
def top_movies(movies: Movies, n: int) -> Movies:
    """Die n besten Filme, deklarativ."""
    return tuple(sorted(movies, key=lambda m: m.rating, reverse=True)[:max(n, 0)])
```
Beide sind in `movies.py` (Zeilen 148–166) und geben das gleiche Resultat, auch wenn zwei Filme gleich gut bewertet sind.

## Pflicht-Artefakt
Beide Varianten nebeneinander (oben), mit Vor- und Nachteilen:

- Imperativ: 12 Zeilen. Man sieht jeden Schritt, darum ist Debuggen einfach. Dafür gibt es viele Variablen und bei grossem n ist es langsam.
- Deklarativ: 1 Zeile. Man versteht sofort, was gemacht wird, und es ist schnell. Beim Debuggen sieht man aber die einzelnen Schritte nicht.

## Test und Überprüfung
Der gleiche Test läuft gegen beide Varianten:
- Test 1: `n=3` -> The Dark Knight, Inception, Forrest Gump (-> beide grün)
- Test 2 (Edge Cases): `n=0` -> `()`, `n=-1` -> `()`, `n=50` -> alle 12 (-> beide grün)

## Entscheidung
Ich nehme die deklarative Version. Sie ist viel kürzer, schneller und man sieht sofort, was sie macht. Die imperative wäre nur besser, wenn ich beim Debuggen jeden Schritt anschauen will.

## Reflexion und Transfer
Was mich überrascht hat, ist, dass die kurze Variante einen eigenen Fehler hatte (negatives n). Gelernt habe ich, dass man beim Umbau dieselben Tests behalten muss, nur so sieht man, ob sich das Verhalten geändert hat. Für nächstes Mal nehme ich mit, dass die Tests für negative Werte am besten am Anfang geschrieben werden.
