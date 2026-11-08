# Kompetenzfeld: C1B

**Feature im Flask-Projekt:** Score für die Rangliste (`final_score`)

## Kontext und Ziel
Für die Rangliste bekommt jeder Film einen Score. Neuere Filme bekommen einen kleinen Bonus.

## Konzept in eigenen Worten
Ein Algorithmus ist eine feste Reihenfolge von Schritten. Aus dem gleichen Input kommt immer der gleiche Output. Bei einem Beispieldurchlauf rechne ich die Schritte von Hand nach.

## Umsetzung im Projekt
Schritt 1: Der Basis-Score ist die Bewertung. Schritt 2: Der Bonus ist 0.02 pro Jahr seit 1990. Er ist nie negativ, und Filme aus der Zukunft bekommen keinen. Schritt 3: Basis plus Bonus, gerundet.

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
Der Code steht in `movies.py` (Zeilen 175–184).

## Pflicht-Artefakt
Beispiel mit Inception (2010, Bewertung 8.8), Jahr 2026:

- Schritt 1, `base_score`: Bewertung = 8.8
- Schritt 2, `recency_bonus`: (2010 − 1990) × 0.02 = 0.4
- Schritt 3, `final_score`: 8.8 + 0.4 = 9.2

## Test und Überprüfung
- Test 1: Inception -> 8.8, 0.4 und 9.2 (-> grün)
- Test 2 (Edge Case): Film von 1980 oder 2030 -> Bonus 0.0 (-> grün)

## Reflexion und Transfer
Mit Kommazahlen rechnet der Computer nicht immer genau. Darum runde ich. Die Rechnung von Hand als Test zu speichern, mache ich wieder so.
