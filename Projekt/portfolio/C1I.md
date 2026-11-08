# Kompetenzfeld: C1I

**Feature im Flask-Projekt:** Score für die Rangliste, aufgeteilt in kleine Funktionen

## Kontext und Ziel
Der Score besteht aus zwei Teilen: der Bewertung und einem Bonus für neuere Filme. Ich wollte jeden Teil in eine eigene kleine Funktion packen.

## Konzept in eigenen Worten
Zerlegen heisst: Ich teile eine grosse Aufgabe in kleine Funktionen auf. Jede Funktion macht genau eine Sache. Die Signatur zeigt, was hineingeht und was herauskommt. Kleine Funktionen kann man einzeln testen und später neu zusammensetzen.

## Umsetzung im Projekt
Ich habe drei Funktionen gebaut. `base_score` gibt die Bewertung zurück. `recency_bonus` rechnet den Bonus. `final_score` zählt beides zusammen und rundet. Das Jahr ist ein Parameter (`today_year`). Ich hole es nicht mit `datetime.now()`, sonst wären die Funktionen nicht pure und die Tests würden nächstes Jahr nicht mehr stimmen. Ich hätte alles in eine Zeile schreiben können. Dann könnte ich den Bonus aber nicht allein testen. `base_score` sieht unnötig aus, aber so kann ich die Basis später ändern, ohne den Rest anzufassen.

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
Der Code steht in `movies.py` (Zeilen 170–184). Jede Funktion hat Typen in der Signatur und macht nur eine Sache.

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
Schwierig war, die richtige Grösse für die Funktionen zu finden. Gelernt habe ich, dass ein Parameter wie `today_year` eine Funktion testbar macht. Nächstes Mal würde ich 1990 und 0.02 als Konstanten mit Namen speichern. So eine Aufteilung kann ich auch für Preise mit Rabatt brauchen.
