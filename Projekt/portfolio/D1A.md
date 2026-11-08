# Kompetenzfeld: D1A

**Feature im Flask-Projekt:** Film nach Id suchen (`/movies/<id>`), Messung in `bench.py`

## Kontext und Ziel
Die Route `/movies/7` soll den Film mit der Id 7 finden. Ich wollte messen, was schneller ist: in einer Liste suchen oder in einem dict. Dann wollte ich mich begründet entscheiden.

## Konzept in eigenen Worten
In einer Liste muss man im schlimmsten Fall jeden Film anschauen. Doppelt so viele Filme heisst doppelt so lange (O(n)). Ein dict weiss direkt, wo der Film mit dieser Id liegt. Das geht immer etwa gleich schnell, egal wie viele Filme es gibt (O(1)). Dafür muss man das dict zuerst einmal bauen.

## Umsetzung im Projekt
`find_by_id` sucht in der Liste, Film für Film. `movie_index` baut ein dict von Id zu Film. In `bench.py` erzeuge ich 100000 Filme mit festem Zufall (`random.seed(42)`), damit die Messung wiederholbar ist. Dann suche ich 1000 Ids auf beide Arten. Jede Messung läuft fünfmal, und ich nehme den mittleren Wert (Median).

## Code-Beispiel und Einordnung
```python
# D1A: lineare Suche in der Liste (O(n))
def find_by_id(movies: Movies, movie_id: int) -> Movie | None:
    """Sucht einen Film durch alle Elemente hindurch."""
    return next((m for m in movies if m.id == movie_id), None)


# D1A: Index als dict (Aufbau O(n), danach Suche O(1))
def movie_index(movies: Movies) -> dict[int, Movie]:
    """Baut ein dict von Id auf Film."""
    return {m.id: m for m in movies}
```
Die Funktionen stehen in `movies.py` (Zeilen 240–249), die Messung in `bench.py`.

## Pflicht-Artefakt
Messung vom 08.11.2026, Python 3.14.3, 100000 Filme, 1000 Suchen:

- Liste durchsuchen: 943.298 ms
- dict durchsuchen: 0.054 ms
- dict einmal bauen: 6.192 ms

## Interpretation und Begründung
Das dict ist bei der Suche etwa 17000-mal schneller. Das dict zu bauen dauert so lange wie etwa sieben Suchen in der Liste. Wenn man also öfter als siebenmal sucht, lohnt sich das dict. Ich nehme für die Suche nach Id das dict, weil jede Id nur einmal vorkommt. Für die Filme selbst behalte ich das Tuple, weil es gut zu filter, map und sorted passt.

## Grenzen der Messung
Ich habe nur auf meinem Laptop gemessen, und andere Programme liefen nebenbei. Die Filme sind erfunden. In der echten App gibt es nur 12 Filme, dort merkt man keinen Unterschied. Ausserdem baut die Route das dict bei jedem Aufruf neu.

## Test und Überprüfung
- Test 1: Id 7 -> beide Arten finden Forrest Gump (-> grün)
- Test 2 (Edge Case): Id 99 -> `None`, Route gibt 404 (-> grün)

## Reflexion und Transfer
Ich wusste, dass das dict schneller ist, aber nicht so viel. Gelernt habe ich, dass man auch die Zeit zum Bauen messen muss, sonst ist der Vergleich unfair. Nächstes Mal würde ich mit verschiedenen Mengen messen.
