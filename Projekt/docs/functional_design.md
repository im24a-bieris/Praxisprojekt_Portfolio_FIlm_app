# Functional-Design-Elemente im Projekt (B1B)

## 1. Immutable Datentypen

- `Movie` (`movies.py`, Zeilen 7–14): frozen dataclass. `movie.rating = 1.0` gibt einen Fehler.
- Tuples (`movies.py`, `load_movies` Zeilen 21–37 und alle Rückgaben): Ein Tuple kann man nicht verändern.
- `Movies` (`movies.py`, Zeile 17): Name für `tuple[Movie, ...]`, damit man in jeder Funktion sieht, dass es ein Tuple ist.
- Zustand der App (`app.py`, Zeile 14 und `post_movie` Zeilen 49–60): wird nicht verändert, sondern durch ein neues Tuple ersetzt.

## 2. Constructors

- `Movie(...)` (`movies.py`, Zeilen 7–14): baut einen neuen Film.
- `load_movies()` (`movies.py`, Zeilen 21–37): baut die 12 Startfilme.
- `rate_movie(movie, rating)` (`movies.py`, Zeilen 138–140): baut einen neuen Film mit neuer Bewertung.
- `add_movie(movies, movie)` (`movies.py`, Zeilen 130–134): baut ein neues Tuple mit einem Film mehr.

## 3. Composable Operators

Alle bekommen Filme und geben wieder Filme zurück. Darum kann man sie hintereinander hängen.

- `filter_by_genre` (`movies.py`, Zeilen 55–57): nur ein Genre
- `search_title` (`movies.py`, Zeilen 61–63): Suche im Titel
- `filter_by_years` (`movies.py`, Zeilen 67–69): nur bestimmte Jahre
- `sort_by` (`movies.py`, Zeilen 118–120): sortieren mit einer Funktion
- `top_movies` (`movies.py`, Zeilen 164–166): die n besten
- `rank_movies` (`movies.py`, Zeilen 188–190): Rangliste

## 4. Verkettung (Beispiele)

```python
top_movies(filter_by_genre(load_movies(), "Action"), 3)
# -> The Dark Knight, Gladiator, John Wick

rank_movies(filter_by_years(load_movies(), 2000, 2010), 2026)
# -> The Dark Knight, Inception, Gladiator, Avatar, Shrek
```

In der App verkettet `get_movies` (`app.py`, Zeilen 30–46) die Filter, je nachdem, was in der URL steht.
