# Kompetenzfeld: C1A

**Feature im Flask-Projekt:** Rangliste (`/movies/ranking`, Funktion `rank_movies`)

## Kontext und Ziel
Aus den Funktionen `base_score`, `recency_bonus` und `final_score` soll eine Rangliste werden. Wenn zwei Filme gleich viele Punkte haben, entscheidet der Titel.

## Konzept in eigenen Worten
Bei der Komposition setze ich kleine Funktionen zu einem grösseren Ablauf zusammen. Auch wenn jede kleine Funktion schon getestet ist, teste ich den ganzen Ablauf nochmals. Wichtig sind vor allem Spezialfälle wie eine leere Liste oder ein Gleichstand.

## Umsetzung im Projekt
`rank_movies` sortiert mit `sorted` und einem Schlüssel aus zwei Teilen. `-final_score` bringt den höchsten Score nach vorne, und `m.title` entscheidet bei Gleichstand. Die Route `get_ranking` übergibt das Jahr, standardmässig 2026.

## Code-Beispiel und Einordnung
```python
# C1A: Komposition der Teilfunktionen zu einem Ablauf
def rank_movies(movies: Movies, today_year: int) -> Movies:
    """Rangliste nach final_score, bei Gleichstand nach Titel."""
    return tuple(sorted(movies, key=lambda m: (-final_score(m, today_year), m.title)))
```
Die Funktion ist in `movies.py` (Zeilen 187–190). `rank_movies` ruft `final_score` auf, und `final_score` ruft `base_score` und `recency_bonus` auf. So hängen die Funktionen zusammen.

## Pflicht-Artefakt
Der Ablauf mit Testfällen und Spezialfällen. Die Rangliste 2026 beginnt so: The Dark Knight 9.36, Inception 9.2, Interstellar 9.18, Joker 8.98, Forrest Gump 8.88, The Matrix 8.88.

## Vergleich von drei Lösungen
- Lösung A (gewählt): einmal `sorted` mit dem Schlüssel `(-score, title)`. Kurz und eindeutig.
- Lösung B: zweimal sortieren, zuerst nach Titel und dann nach Score. Funktioniert auch, aber man muss wissen, dass `sorted` bei Gleichstand die Reihenfolge behält.
- Lösung C: zuerst mit `map` Paare aus Score und Film machen, diese sortieren und dann die Filme wieder rausholen. So hatte ich es im Design-Blatt geplant, aber es ist mehr Code.

Ich habe A genommen, weil sie am kürzesten ist und man die Sortierregel direkt im Code sieht.

## Test und Überprüfung
- Test 1: bester Film zuerst -> The Dark Knight (-> grün)
- Test 2 (Edge Case Gleichstand): Forrest Gump und The Matrix haben beide 8.88 -> Forrest Gump zuerst (-> grün)
- Test 3 (Edge Case leer): `rank_movies((), 2026)` -> `()` (-> grün)
- Test 4 (Edge Case Zukunft): Film von 2030 mit 9.1 bekommt keinen Bonus und kommt nach The Dark Knight (-> grün)

## Reflexion und Transfer
Der Gleichstand war am schwierigsten. Ohne Runden gibt 8.7 + 0.18 im Computer nicht genau 8.88, und dann würde der Titel nie entscheiden. Das hat erst der Test gezeigt. Sortieren mit mehreren Regeln braucht man oft, z.B. bei einer Rangliste im Sport.
