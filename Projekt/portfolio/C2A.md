# Kompetenzfeld: C2A

**Feature im Flask-Projekt:** Statistik pro Genre (`/stats/genres`)

## Kontext und Ziel
Die App soll pro Genre zeigen, wie viele Filme es gibt und wie gut sie im Schnitt sind. Das beste Genre kommt zuerst, bei Gleichstand wird nach Name sortiert. Das ist das dritte Feature für C2, also anders als bei C2B und C2I.

## Konzept in eigenen Worten
Aggregation bedeutet, dass ich viele Werte zu wenigen zusammenfasse, hier 12 Filme zu 4 Genres. Bei einer eigenen Sortierung gebe ich `sorted` mit `key=` eine Regel mit. Wenn die Regel zwei Werte zurückgibt, wird zuerst nach dem ersten und bei Gleichstand nach dem zweiten sortiert.

## Umsetzung im Projekt
`genre_stats` geht mit `reduce` durch alle Filme und zählt beim passenden Genre die Anzahl und die Summe hoch. Am Ende wird der Durchschnitt ausgerechnet. `ranked_genre_stats` sortiert das dann nach Durchschnitt, der höchste zuerst, und bei Gleichstand nach Name.

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
Der Code ist in `movies.py` (Zeilen 201–217). Oben ist die Aggregation mit `reduce`, unten die Sortierung mit zwei Regeln.

## Pflicht-Artefakt
Aggregation (`genre_stats`) und eigene Sortierung (`ranked_genre_stats`), oben.

## Vergleich mit anderen Lösungen
- `reduce` (gewählt): ändert nichts und passt zum Rest von `movies.py`. Der Nachteil ist, dass bei jedem Film das dict kopiert wird. Bei vielen Daten wird das langsam.
- `defaultdict`: kurz und schnell, aber das dict wird in einer Schleife verändert (Mutation).
- `groupby`: sieht gut aus, aber die Filme müssen vorher nach Genre sortiert sein, sonst kommen falsche Gruppen raus. Das vergisst man schnell.

Ich habe `reduce` genommen, weil es nichts verändert und es bei 12 Filmen egal ist, dass es etwas langsamer ist. Mit sehr vielen Filmen würde ich `defaultdict` nehmen.

## Test und Überprüfung
- Test 1: Sci-Fi -> 4 Filme, Durchschnitt 8.53 (-> grün)
- Test 2: Reihenfolge Sci-Fi, Drama, Action, Animation (-> grün)
- Test 3 (Edge Case Gleichstand): Western und Comedy mit je 8.0 -> Comedy zuerst (-> grün)
- Test 4 (Edge Case leer): `genre_stats(())` -> `{}` (-> grün)

## Reflexion und Transfer
Am Anfang war es schwierig zu verstehen, was gerade in `acc` drin ist. Anzahl und Summe zu speichern war einfacher als direkt den Durchschnitt, weil man mit einem Durchschnitt nicht gut weiterrechnen kann. Das Gruppieren könnte ich auch für andere Auswertungen brauchen, z.B. Noten pro Fach.
