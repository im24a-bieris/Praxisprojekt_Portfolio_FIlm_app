# Kompetenzfeld: C1B

**Feature im Flask-Projekt:** Score für die Rangliste (`final_score`)

## Kontext und Ziel
Für die Rangliste bekommt jeder Film einen Score. Neuere Filme bekommen ein bisschen Bonus.

## Konzept in eigenen Worten
Ein Algorithmus ist eine feste Abfolge von Schritten. Mit dem gleichen Input kommt immer das Gleiche raus. Beim Beispieldurchlauf rechne ich die Schritte von Hand nach und vergleiche mit dem Programm.

## Umsetzung im Projekt
Zuerst nehme ich die Bewertung als Basis. Dann kommt der Bonus dazu: 0.02 pro Jahr seit 1990, nie negativ, und Filme aus der Zukunft bekommen gar keinen. Am Schluss werden beide zusammengezählt und gerundet.

## Code-Beispiel und Einordnung
```python
def recency_bonus(movie: Movie, today_year: int) -> float:
    """Bonus fuer neuere Filme: 0.02 pro Jahr seit 1990, nie negativ, 0 fuer Zukunftsfilme."""
    if movie.year > today_year:
        return 0.0
    return max(0.0, (movie.year - 1990) * 0.02)


def final_score(movie: Movie, today_year: int) -> float:
    """Gesamt-Score = Basis-Score + Bonus, auf 3 Stellen gerundet."""
    return round(base_score(movie) + recency_bonus(movie, today_year), 3)
```
Der Code ist in `movies.py` (Zeilen 175–184).

## Pflicht-Artefakt
Beispiel mit Inception (2010, Bewertung 8.8), Jahr 2026:

- Schritt 1, `base_score`: Bewertung = 8.8
- Schritt 2, `recency_bonus`: (2010 − 1990) × 0.02 = 0.4
- Schritt 3, `final_score`: 8.8 + 0.4 = 9.2

## Test und Überprüfung
- Test 1: Inception -> 8.8, 0.4 und 9.2 (-> grün)
- Test 2 (Edge Case): Film von 1980 oder 2030 -> Bonus 0.0 (-> grün)

## Reflexion und Transfer
Bei Kommazahlen rechnet der Computer nicht immer ganz genau, deshalb runde ich am Schluss. Es war praktisch, die Rechnung von Hand direkt als Test zu speichern.
