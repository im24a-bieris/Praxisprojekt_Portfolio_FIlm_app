# Kompetenzfeld: B1A

**Feature im Flask-Projekt:** Top-Liste (`/movies/top?n=5`)

## Kontext und Ziel
Die Route soll die n besten Filme zurückgeben. Ich habe die Funktion zuerst imperativ gebaut und danach deklarativ. Dann habe ich beide verglichen und mich entschieden.

## Konzept in eigenen Worten
Imperativ heisst: Ich beschreibe jeden einzelnen Schritt. Ich suche in einer Schleife den besten Film, nehme ihn heraus und wiederhole das. Deklarativ heisst: Ich sage nur, was ich will, also "nach Bewertung sortiert, die ersten n". Python macht den Rest.

## Umsetzung im Projekt
Die imperative Variante `top_movies_imperative` hat zwei Schleifen, ein `if` und zwei Hilfslisten. Die deklarative Variante `top_movies` ist nur eine Zeile mit `sorted`. Die Route benutzt die deklarative. Beim Umbau habe ich einen Fehler gefunden: Mit einem negativen n schneidet `[:n]` Filme am Ende ab. Darum steht dort `max(n, 0)`.

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
Beide stehen in `movies.py` (Zeilen 148–166). Sie geben genau das gleiche Resultat, auch wenn zwei Filme die gleiche Bewertung haben.

## Pflicht-Artefakt
Beide Varianten nebeneinander (oben), mit Vor- und Nachteilen:

- Imperativ: 12 Zeilen. Man sieht jeden Schritt, darum ist Debuggen einfach. Aber es hat viele Variablen und ist bei grossem n langsam.
- Deklarativ: 1 Zeile. Sie liest sich wie die Aufgabe und ist schnell. Aber beim Debuggen sieht man die einzelnen Schritte nicht.

## Test und Überprüfung
Der gleiche Test läuft gegen beide Varianten:
- Test 1: `n=3` -> The Dark Knight, Inception, Forrest Gump (-> beide grün)
- Test 2 (Edge Cases): `n=0` -> `()`, `n=-1` -> `()`, `n=50` -> alle 12 (-> beide grün)

## Entscheidung
Ich nehme die deklarative Variante. Sie ist kürzer, schneller und man versteht sofort, was sie macht. Die imperative ist nur besser, wenn man beim Debuggen jeden Schritt sehen will.

## Reflexion und Transfer
Überrascht hat mich, dass auch die kurze Variante einen Fehler hatte (negatives n). Gelernt habe ich, dass man beim Umbau die gleichen Tests behalten muss. Nur so sieht man, ob noch alles gleich funktioniert. Nächstes Mal schreibe ich Tests für negative Werte gleich am Anfang.
