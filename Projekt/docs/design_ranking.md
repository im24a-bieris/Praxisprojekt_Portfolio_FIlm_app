# Design-Blatt: Ranking (B1I)

Entwurf **vor** der Umsetzung des Ranking-Algorithmus (Schritt 8).
Tipp für Git: Diese Datei allein committen, **bevor** der Ranking-Code in `movies.py` committet wird.

## 1. Deklarative Anforderungen (Was, nicht Wie)

- Gib die Filme geordnet nach Gesamt-Score zurück.
- Der Score ist die Bewertung plus ein Bonus für neuere Filme.
- Der Bonus ist 0.02 pro Jahr seit 1990 und nie negativ.
- Filme aus der Zukunft (Jahr grösser als das aktuelle Jahr) bekommen keinen Bonus.
- Bei gleichem Score entscheidet der Titel (alphabetisch).
- Das aktuelle Jahr wird von aussen übergeben, damit die Funktionen pure bleiben.
- Eine leere Liste ergibt eine leere Rangliste.

## 2. Datenfluss

```
load_movies → filter → map(score) → sorted → top n → jsonify
```

- `load_movies()`: gibt alle Filme als Tuple.
- `filter`: behält nur die gewünschten Filme (z.B. ein Genre).
- `map(score)`: macht aus jedem Film ein Paar (Score, Film).
- `sorted`: sortiert nach Score (höchster zuerst), dann nach Titel.
- `top n`: nimmt die ersten n.
- `jsonify`: macht daraus die JSON-Antwort der Route.

## 3. Geplante Operatoren mit Signaturen

```
base_score(movie: Movie) -> float
recency_bonus(movie: Movie, today_year: int) -> float
final_score(movie: Movie, today_year: int) -> float
rank_movies(movies: tuple[Movie, ...], today_year: int) -> tuple[Movie, ...]
```

- `filter`: optional über die bestehenden Funktionen `filter_by_genre` / `filter_by_years`.
- `map`: `final_score` auf jeden Film.
- `sorted`: Schlüssel `(-final_score, title)`.
- `reduce`: für das Ranking nicht nötig (es wird nichts zusammengefasst). Wird bei der Genre-Statistik gebraucht.

## 4. Entscheidungen und Alternativen

- `today_year` als Parameter statt `datetime.now()`: Sonst wäre die Funktion nicht pure, und die Tests würden nächstes Jahr nicht mehr stimmen.
- Drei kleine Funktionen statt einer grossen: Jede kann man einzeln testen, und den Bonus kann man später ändern.
- Score auf 3 Stellen runden: Wegen Kommazahlen sollen 8.7 + 0.18 und 8.8 + 0.08 gleich viel ergeben.
- Gleichstand nach Titel statt nach Id: Das Resultat ist eindeutig und für Menschen verständlich.
- Tuple statt Liste: Es ist unveränderlich und passt zu den anderen Funktionen in `movies.py`.
