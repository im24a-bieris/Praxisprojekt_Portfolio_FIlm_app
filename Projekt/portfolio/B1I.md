# Kompetenzfeld: B1I

**Feature im Flask-Projekt:** Rangliste der Filme (`/movies/ranking`)

## Kontext und Ziel
Die App soll eine Rangliste machen. Dabei zählt die Bewertung, und neuere Filme bekommen noch einen kleinen Bonus. Bevor ich den Code geschrieben habe, habe ich ein Design-Blatt gemacht (`docs/design_ranking.md`).

## Konzept in eigenen Worten
Beim deklarativen Entwurf schreibe ich zuerst auf, was am Ende herauskommen soll, und noch nicht, wie der Code aussieht. Danach überlege ich, welche Funktionen ich brauche (filter, map, sorted) und in welcher Reihenfolge die Daten durchgehen. Erst dann fange ich an zu programmieren.

## Umsetzung im Projekt
Meine Anforderung war: "Gib die Filme sortiert nach Score zurück. Der Score ist die Bewertung plus ein Bonus für neuere Filme." Daraus habe ich den Datenfluss und die Funktionen geplant. Das Jahr gebe ich als Parameter mit und hole es nicht mit `datetime.now()`, damit die Funktionen pure bleiben. Ich hätte auch alles in eine grosse Funktion schreiben können, aber dann kann man die Teile nicht einzeln testen.

## Code-Beispiel und Einordnung
```
load_movies → filter → map(score) → sorted → top n → jsonify
```
```python
def rank_movies(movies: Movies, today_year: int) -> Movies:
    """Rangliste nach final_score, bei Gleichstand nach Titel."""
    return tuple(sorted(movies, key=lambda m: (-final_score(m, today_year), m.title)))
```
Oben ist der geplante Datenfluss aus dem Design-Blatt, unten die fertige Funktion in `movies.py` (Zeilen 188–190).

## Pflicht-Artefakt
Design-Blatt `docs/design_ranking.md` mit Anforderungen, Datenfluss, geplanten Funktionen und Entscheidungen.

## Vergleich Plan und Umsetzung
- Geplant war ein eigener `map`-Schritt für den Score. Am Schluss rechne ich den Score direkt in `sorted` aus, das ist kürzer.
- `filter` und `top n` habe ich weggelassen, weil die Rangliste alle Filme zeigen soll.
- Nicht geplant war das Runden. Forrest Gump und The Matrix sollten gleich viele Punkte haben, wegen den Kommazahlen war es aber nicht genau gleich. Jetzt runde ich auf drei Stellen.

## Test und Überprüfung
- Test 1: `rank_movies(load_movies(), 2026)` -> The Dark Knight, Inception, Interstellar zuerst (-> grün)
- Test 2 (Edge Case): `rank_movies((), 2026)` -> `()` (-> grün)

## Reflexion und Transfer
Mit dem Design-Blatt wusste ich schon vor dem Programmieren, welche Funktionen ich brauche. Das Problem mit den Kommazahlen habe ich aber erst beim Testen gesehen. Nächstes Mal schreibe ich die Spezialfälle schon ins Design-Blatt.
