# Kompetenzfeld: B1I

**Feature im Flask-Projekt:** Rangliste der Filme (`/movies/ranking`)

## Kontext und Ziel
Die App soll eine Rangliste machen. Dabei zählt die Bewertung, aber neuere Filme bekommen einen kleinen Bonus. Bevor ich programmiert habe, habe ich ein Design-Blatt geschrieben (`docs/design_ranking.md`).

## Konzept in eigenen Worten
Deklarativ planen heisst: Ich schreibe zuerst auf, was herauskommen soll, nicht wie der Code aussieht. Dann plane ich, welche Bausteine ich brauche (filter, map, sorted) und in welcher Reihenfolge die Daten durchlaufen. Erst danach programmiere ich.

## Umsetzung im Projekt
Die Anforderung war: "Gib die Filme sortiert nach Score zurück. Der Score ist die Bewertung plus ein Bonus für neuere Filme." Daraus habe ich den Datenfluss und die Funktionen geplant. Entscheidung: Das Jahr wird als Parameter übergeben, nicht mit `datetime.now()` geholt. So bleiben die Funktionen pure. Eine grosse Funktion statt mehrerer kleiner habe ich verworfen, weil man sie schlechter testen kann.

## Code-Beispiel und Einordnung
```
load_movies → filter → map(score) → sorted → top n → jsonify
```
```python
def rank_movies(movies: Movies, today_year: int) -> Movies:
    """Rangliste nach final_score, bei Gleichstand nach Titel."""
    return tuple(sorted(movies, key=lambda m: (-final_score(m, today_year), m.title)))
```
Der erste Block ist der geplante Datenfluss aus dem Design-Blatt. Der zweite ist die Umsetzung in `movies.py` (Zeilen 188–190).

## Pflicht-Artefakt
Design-Blatt `docs/design_ranking.md` mit Anforderungen, Datenfluss, geplanten Funktionen und Entscheidungen.

## Vergleich Plan und Umsetzung
- Geplant war ein eigener `map`-Schritt für den Score. Umgesetzt wird der Score direkt in `sorted` berechnet. Das ist kürzer.
- `filter` und `top n` waren nicht nötig, weil die Rangliste alle Filme zeigt.
- Nicht geplant: Zwei Filme hatten wegen Kommazahlen nicht genau den gleichen Score. Darum runde ich jetzt auf drei Stellen.

## Test und Überprüfung
- Test 1: `rank_movies(load_movies(), 2026)` -> The Dark Knight, Inception, Interstellar zuerst (-> grün)
- Test 2 (Edge Case): `rank_movies((), 2026)` -> `()` (-> grün)

## Reflexion und Transfer
Das Design-Blatt hat geholfen, weil ich vor dem Programmieren schon wusste, welche Funktionen ich brauche. Das Problem mit den Kommazahlen habe ich aber erst beim Testen gefunden. Nächstes Mal schreibe ich auch Spezialfälle ins Design-Blatt.
