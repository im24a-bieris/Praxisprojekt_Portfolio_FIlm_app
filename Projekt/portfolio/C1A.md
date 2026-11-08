# Kompetenzfeld: C1A

**Feature im Flask-Projekt:** Rangliste (`/movies/ranking`, Funktion `rank_movies`)

## Kontext und Ziel
Die kleinen Funktionen `base_score`, `recency_bonus` und `final_score` sollen zusammen eine Rangliste ergeben. Bei gleichem Score entscheidet der Titel. Ich wollte verschiedene Lösungen vergleichen und auch Spezialfälle testen.

## Konzept in eigenen Worten
Komposition heisst: Ich verbinde kleine Funktionen zu einem grösseren Ablauf. Jede kleine Funktion ist schon getestet. Den ganzen Ablauf teste ich trotzdem nochmals, vor allem die Spezialfälle: leere Liste, gleicher Score, komische Werte.

## Umsetzung im Projekt
`rank_movies` sortiert mit `sorted`. Der Schlüssel hat zwei Teile: `-final_score` bringt den höchsten Score nach vorne, `m.title` entscheidet bei Gleichstand. Die Route `get_ranking` gibt das Jahr mit (Standard 2026).

## Code-Beispiel und Einordnung
```python
# C1A: Komposition der Teilfunktionen zu einem Ablauf
def rank_movies(movies: Movies, today_year: int) -> Movies:
    """Rangliste nach final_score, bei Gleichstand nach Titel."""
    return tuple(sorted(movies, key=lambda m: (-final_score(m, today_year), m.title)))
```
Die Funktion steht in `movies.py` (Zeilen 187–190). Hier sieht man die Komposition: `rank_movies` ruft `final_score` auf, und `final_score` ruft `base_score` und `recency_bonus` auf.

## Pflicht-Artefakt
Der Ablauf mit Testfällen und Spezialfällen. Die Rangliste 2026 beginnt so: The Dark Knight 9.36, Inception 9.2, Interstellar 9.18, Joker 8.98, Forrest Gump 8.88, The Matrix 8.88.

## Vergleich von drei Lösungen
- Lösung A (gewählt): einmal `sorted` mit dem Schlüssel `(-score, title)`. Eine Zeile, klares Resultat.
- Lösung B: zweimal sortieren, zuerst nach Titel, dann nach Score. Das geht auch, ist aber schwerer zu verstehen.
- Lösung C: zuerst mit `map` Paare (Score, Film) machen, dann sortieren, dann die Filme wieder herausnehmen. So war es im Design-Blatt geplant, aber es braucht mehr Code.
Ich habe A gewählt, weil sie am kürzesten ist und die Regel direkt im Code steht.

## Test und Überprüfung
- Test 1: bester Film zuerst -> The Dark Knight (-> grün)
- Test 2 (Edge Case Gleichstand): Forrest Gump und The Matrix haben beide 8.88 -> Forrest Gump zuerst (-> grün)
- Test 3 (Edge Case leer): `rank_movies((), 2026)` -> `()` (-> grün)
- Test 4 (Edge Case Zukunft): Film von 2030 mit 9.1 bekommt keinen Bonus und kommt nach The Dark Knight (-> grün)

## Reflexion und Transfer
Am schwierigsten war der Gleichstand. Ohne Runden ist 8.7 + 0.18 im Computer nicht genau 8.88. Dann hätte der Titel nie entschieden. Das habe ich nur dank dem Test gemerkt. Sortieren mit mehreren Regeln kann ich auch anderswo brauchen, zum Beispiel für eine Tabelle bei einem Sportturnier.
