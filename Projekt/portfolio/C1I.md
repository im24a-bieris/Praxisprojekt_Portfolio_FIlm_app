# Kompetenzfeld: C1I

**Feature im Flask-Projekt:** Score für die Rangliste, aufgeteilt in kleine Funktionen

## Kontext und Ziel
Der Score besteht aus der Bewertung und einem Bonus für neuere Filme. Jeder Teil soll eine eigene kleine Funktion sein.

## Konzept in eigenen Worten
Beim Zerlegen teile ich eine grössere Aufgabe in kleine Funktionen auf, die jeweils nur eine Sache machen. An der Signatur sieht man, was reingeht und was rauskommt. Kleine Funktionen kann man einzeln testen und später anders zusammensetzen.

## Umsetzung im Projekt
`base_score` gibt die Bewertung zurück, `recency_bonus` rechnet den Bonus aus und `final_score` zählt beides zusammen und rundet. Das Jahr übergebe ich als Parameter `today_year`. Mit `datetime.now()` wäre die Funktion nicht mehr pure, und die Tests würden nächstes Jahr ein anderes Resultat geben. Man könnte alles in eine Zeile schreiben, aber dann kann ich den Bonus nicht mehr alleine testen. `base_score` macht im Moment fast nichts, aber so kann ich die Basis später ändern, ohne `final_score` anzufassen.

## Code-Beispiel und Einordnung
```python
def base_score(movie: Movie) -> float:
    """Basis-Score = Bewertung."""
    return movie.rating


def recency_bonus(movie: Movie, today_year: int) -> float:
    """Bonus fuer neuere Filme: 0.02 pro Jahr seit 1990, nie negativ, 0 fuer Zukunftsfilme."""
    if movie.year > today_year:
        return 0.0
    return max(0.0, (movie.year - 1990) * 0.02)


def final_score(movie: Movie, today_year: int) -> float:
    """Gesamt-Score = Basis-Score + Bonus, auf 3 Stellen gerundet."""
    return round(base_score(movie) + recency_bonus(movie, today_year), 3)
```
Der Code ist in `movies.py` (Zeilen 170–184). Jede Funktion hat Typen in der Signatur.

## Pflicht-Artefakt
Die Signaturen:
- `base_score(movie: Movie) -> float`: die Basis
- `recency_bonus(movie: Movie, today_year: int) -> float`: der Bonus
- `final_score(movie: Movie, today_year: int) -> float`: beides zusammen

## Test und Überprüfung
- Test 1: Bonus für einen Film von 2030 -> 0.0 (-> grün)
- Test 2: Bonus für einen Film von 1980 -> 0.0, nicht negativ (-> grün)
- Test 3 (Edge Case): Bewertung 0, Jahr 2020 -> Score 0.6 (-> grün)

## Reflexion und Transfer
Am schwierigsten war zu entscheiden, wie klein die Funktionen sein sollen. Durch `today_year` als Parameter sind die Funktionen gut testbar. Die Zahlen 1990 und 0.02 würde ich nächstes Mal als Konstanten mit Namen speichern.
