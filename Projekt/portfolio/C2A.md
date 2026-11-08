# Kompetenzfeld: C2A

**Feature im Flask-Projekt:** Statistik pro Genre (`/stats/genres`)

## Kontext und Ziel
Die App soll pro Genre zeigen, wie viele Filme es gibt und wie gut sie im Schnitt sind. Das beste Genre kommt zuerst. Bei Gleichstand entscheidet der Name. Das ist das dritte Feature für C2, anders als C2B und C2I.

## Konzept in eigenen Worten
Aggregation heisst: Ich fasse viele Werte zu wenigen zusammen. Hier werden zwölf Filme zu vier Genres. Bei einer eigenen Sortierung gebe ich `sorted` mit `key=` eine Regel mit. Wenn die Regel zwei Werte hat, wird zuerst nach dem ersten und dann nach dem zweiten sortiert.

## Umsetzung im Projekt
`genre_stats` geht mit `reduce` durch alle Filme. Für jeden Film zählt es beim passenden Genre die Anzahl und die Summe hoch. Am Schluss rechnet es den Durchschnitt. `ranked_genre_stats` sortiert dann nach Durchschnitt (höchster zuerst) und bei Gleichstand nach Name.

## Code-Beispiel und Einordnung
```python
# C2A: Aggregation mit reduce
def genre_stats(movies: Movies) -> dict[str, dict[str, float]]:
    """Anzahl und Durchschnitt pro Genre (Aggregation mit reduce)."""
    def add(acc, m):
        count, total = acc.get(m.genre, (0, 0.0))
        return {**acc, m.genre: (count + 1, total + m.rating)}
    grouped = reduce(add, movies, {})
    return {g: {"count": c, "average": round(t / c, 2)}
            for g, (c, t) in sorted(grouped.items())}


# C2A: benutzerdefinierte Sortierung mit mehreren Kriterien
def ranked_genre_stats(movies: Movies) -> tuple[dict, ...]:
    """Genre-Statistik nach Durchschnitt absteigend, bei Gleichstand nach Name."""
    stats = genre_stats(movies)
    rows = ({"genre": g, **values} for g, values in stats.items())
    return tuple(sorted(rows, key=lambda row: (-row["average"], row["genre"])))
```
Der Code steht in `movies.py` (Zeilen 201–217). Oben sieht man die Aggregation mit `reduce`, unten die Sortierung mit zwei Regeln.

## Pflicht-Artefakt
Aggregation (`genre_stats`) und eigene Sortierung (`ranked_genre_stats`), oben.

## Vergleich mit anderen Lösungen
- `reduce` (gewählt): verändert nichts und passt zum Rest von `movies.py`. Nachteil: Bei jedem Film wird das dict kopiert. Bei vielen Daten ist das langsamer.
- `defaultdict`: kurz und schnell. Es ändert aber ein dict in einer Schleife (Mutation).
- `groupby`: elegant, aber die Filme müssen vorher nach Genre sortiert sein. Sonst gibt es falsche Gruppen. Das vergisst man leicht.
Ich nehme `reduce`, weil es nichts verändert und es bei zwölf Filmen keine Rolle spielt, dass es langsamer ist. Bei sehr vielen Filmen würde ich `defaultdict` nehmen.

## Test und Überprüfung
- Test 1: Sci-Fi -> 4 Filme, Durchschnitt 8.53 (-> grün)
- Test 2: Reihenfolge Sci-Fi, Drama, Action, Animation (-> grün)
- Test 3 (Edge Case Gleichstand): Western und Comedy mit je 8.0 -> Comedy zuerst (-> grün)
- Test 4 (Edge Case leer): `genre_stats(())` -> `{}` (-> grün)

## Reflexion und Transfer
Schwierig war, zu verstehen, was in `acc` gerade drin ist. Es war einfacher, Anzahl und Summe zu speichern statt direkt den Durchschnitt. Nächstes Mal würde ich das genauer aufschreiben. Gruppieren und sortieren kann ich auch für andere Auswertungen brauchen, zum Beispiel Noten pro Fach.
