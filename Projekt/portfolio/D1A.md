# Kompetenzfeld: D1A

**Feature im Flask-Projekt:** Film nach Id suchen (`/movies/<id>`), Messung in `bench.py`

## Kontext und Ziel
Die Route `/movies/7` soll den Film mit der Id 7 finden. Ich wollte messen, ob die Suche in einer Liste oder in einem dict schneller ist, und dann entscheiden.

## Konzept in eigenen Worten
In einer Liste muss man im schlimmsten Fall jeden Film anschauen. Bei doppelt so vielen Filmen dauert es also doppelt so lange (O(n)). Ein dict findet den Film über die Id direkt, das dauert immer etwa gleich lang (O(1)). Dafür muss man das dict zuerst einmal aufbauen.

## Umsetzung im Projekt
`find_by_id` geht die Liste Film für Film durch. `movie_index` baut ein dict, in dem man mit der Id nachschauen kann. In `bench.py` erstelle ich 100000 Filme. Mit `random.seed(42)` kommen jedes Mal die gleichen Zufallsfilme raus, so kann man die Messung wiederholen. Dann suche ich 1000 Ids mit beiden Methoden. Jede Messung läuft fünfmal und ich nehme den Median.

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
Die Funktionen sind in `movies.py` (Zeilen 240–249), die Messung in `bench.py`.

## Pflicht-Artefakt
Messung vom 08.11.2026, Python 3.14.3, 100000 Filme, 1000 Suchen:

- Liste durchsuchen: 943.298 ms
- dict durchsuchen: 0.054 ms
- dict einmal bauen: 6.192 ms

## Interpretation und Begründung
Das dict ist bei der Suche etwa 17000-mal schneller. Das dict aufzubauen dauert ungefähr so lange wie sieben Suchen in der Liste. Ab etwa sieben Suchen lohnt es sich also. Für die Suche nach Id nehme ich das dict, weil jede Id nur einmal vorkommt. Die Filme selbst lasse ich im Tuple, weil das gut mit filter, map und sorted geht.

## Grenzen der Messung
Ich habe nur auf meinem Laptop gemessen, und nebenbei liefen andere Programme. Die Filme sind zufällig erstellt. In der richtigen App gibt es nur 12 Filme, da merkt man keinen Unterschied. Ausserdem baut die Route das dict bei jedem Aufruf neu.

## Test und Überprüfung
- Test 1: Id 7 -> beide Methoden finden Forrest Gump (-> grün)
- Test 2 (Edge Case): Id 99 -> `None`, Route gibt 404 (-> grün)

## Reflexion und Transfer
Dass das dict schneller ist, war klar, aber nicht, dass es so viel ist. Man muss auch die Zeit für das Aufbauen mitmessen, sonst ist der Vergleich nicht fair. Nächstes Mal würde ich noch mit verschiedenen Mengen messen.
