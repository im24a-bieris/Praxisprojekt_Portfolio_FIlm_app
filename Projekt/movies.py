"""Pure Funktionen und Daten der Filmdatenbank."""
from dataclasses import dataclass, replace
from functools import lru_cache, reduce
from typing import Callable


@dataclass(frozen=True)
class Movie:
    """Ein Film (unveraenderlich)."""
    id: int
    title: str
    genre: str
    year: int
    rating: float


Movies = tuple[Movie, ...]


# D1B: Performance-Massnahme 1, die Daten werden nur einmal gebaut
@lru_cache(maxsize=1)
def load_movies() -> Movies:
    """Gibt alle Filme als Tuple zurueck."""
    return (
        Movie(1, "Inception", "Sci-Fi", 2010, 8.8),
        Movie(2, "The Dark Knight", "Action", 2008, 9.0),
        Movie(3, "Interstellar", "Sci-Fi", 2014, 8.7),
        Movie(4, "Gladiator", "Action", 2000, 8.5),
        Movie(5, "Titanic", "Drama", 1997, 7.9),
        Movie(6, "The Matrix", "Sci-Fi", 1999, 8.7),
        Movie(7, "Forrest Gump", "Drama", 1994, 8.8),
        Movie(8, "Toy Story", "Animation", 1995, 8.3),
        Movie(9, "Shrek", "Animation", 2001, 7.9),
        Movie(10, "Joker", "Drama", 2019, 8.4),
        Movie(11, "John Wick", "Action", 2014, 7.4),
        Movie(12, "Avatar", "Sci-Fi", 2009, 7.9),
    )


# A1B: Prozedur (Seiteneffekt print, kein Return)
def print_summary(movies: Movies) -> None:
    """Gibt eine Zusammenfassung auf der Konsole aus."""
    count = len(movies)
    average = average_rating(movies)
    print(f"{count} Filme, Durchschnitt {average:.2f}")


# A1B: pure function (gleicher Input, gleicher Output, kein Seiteneffekt)
def summary(movies: Movies) -> str:
    """Gibt die Zusammenfassung als Text zurueck."""
    return f"{len(movies)} Filme, Durchschnitt {average_rating(movies):.2f}"


# C2B: filter
def filter_by_genre(movies: Movies, genre: str) -> Movies:
    """Behaelt nur Filme des Genres (gross/klein egal)."""
    return tuple(filter(lambda m: m.genre.lower() == genre.lower(), movies))


# C2B: filter (Suche im Titel)
def search_title(movies: Movies, text: str) -> Movies:
    """Behaelt Filme, deren Titel den Text enthaelt."""
    return tuple(filter(lambda m: text.lower() in m.title.lower(), movies))


# C2B: filter (Jahresbereich)
def filter_by_years(movies: Movies, year_from: int, year_to: int) -> Movies:
    """Behaelt Filme zwischen year_from und year_to (inklusive)."""
    return tuple(filter(lambda m: year_from <= m.year <= year_to, movies))


# C2B: map
def titles(movies: Movies) -> tuple[str, ...]:
    """Gibt nur die Titel zurueck."""
    return tuple(map(lambda m: m.title, movies))


# C2B: reduce
def total_rating(movies: Movies) -> float:
    """Summe aller Bewertungen (reduce)."""
    return reduce(lambda acc, m: acc + m.rating, movies, 0.0)


def average_rating(movies: Movies) -> float:
    """Durchschnittsbewertung, 0.0 bei leerer Liste."""
    if not movies:
        return 0.0
    return total_rating(movies) / len(movies)


# D1B: Performance-Massnahme 2, Generator-Ausdruck statt Liste
def best_rating(movies: Movies) -> float:
    """Hoechste Bewertung, 0.0 bei leerer Liste."""
    return max((m.rating for m in movies), default=0.0)


# C2B: Funktionen, die in einer Variable gespeichert und weitergegeben werden
def rating_of(movie: Movie) -> float:
    """Gibt die Bewertung eines Films zurueck."""
    return movie.rating


def title_of(movie: Movie) -> str:
    """Gibt den Titel eines Films zurueck."""
    return movie.title


def year_of(movie: Movie) -> int:
    """Gibt das Jahr eines Films zurueck."""
    return movie.year


SORT_KEYS: dict[str, Callable[[Movie], object]] = {
    "rating": rating_of, "title": title_of, "year": year_of,
}


def sort_by(movies: Movies, key_func: Callable[[Movie], object]) -> Movies:
    """Sortiert die Filme mit einer uebergebenen Funktion."""
    return tuple(sorted(movies, key=key_func))


# A1I: mutierende Variante (veraendert die uebergebene Liste)
def add_movie_mutating(movies_list: list[Movie], movie: Movie) -> None:
    """Haengt den Film an die bestehende Liste an (Mutation)."""
    movies_list.append(movie)


# A1I: immutable Variante (gibt ein neues Tuple zurueck)
def add_movie(movies: Movies, movie: Movie) -> Movies:
    """Immutable: gibt ein neues Tuple zurueck. Doppelte Id gibt ValueError."""
    if any(m.id == movie.id for m in movies):
        raise ValueError(f"Id {movie.id} existiert schon")
    return movies + (movie,)


# A1I: immutable Aenderung eines Films
def rate_movie(movie: Movie, rating: float) -> Movie:
    """Immutable: gibt einen neuen Film mit neuer Bewertung zurueck."""
    return replace(movie, rating=rating)


def next_id(movies: Movies) -> int:
    """Naechste freie Id (1 bei leerer Liste)."""
    return max((m.id for m in movies), default=0) + 1


# B1A: imperative Variante (Schleife, Hilfsliste, if)
def top_movies_imperative(movies: Movies, n: int) -> Movies:
    """Die n besten Filme, imperativ."""
    remaining = list(movies)
    result = []
    while remaining and len(result) < n:
        best = remaining[0]
        for movie in remaining:
            if movie.rating > best.rating:
                best = movie
        result.append(best)
        remaining.remove(best)
    return tuple(result)


# B1A: deklarative Variante (wird von der Route benutzt)
def top_movies(movies: Movies, n: int) -> Movies:
    """Die n besten Filme, deklarativ."""
    return tuple(sorted(movies, key=lambda m: m.rating, reverse=True)[:max(n, 0)])


# C1B / C1I: Teilfunktionen des Ranking-Algorithmus
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


# C1A: Komposition der Teilfunktionen zu einem Ablauf
def rank_movies(movies: Movies, today_year: int) -> Movies:
    """Rangliste nach final_score, bei Gleichstand nach Titel."""
    return tuple(sorted(movies, key=lambda m: (-final_score(m, today_year), m.title)))


# C2I: Lambda und verkettetes filter -> sorted -> map
def recommend(movies: Movies, min_rating: float = 8.0, min_year: int = 2000) -> tuple[str, ...]:
    """Empfehlungen als 'Titel (Jahr)', beste Bewertung zuerst."""
    good = filter(lambda m: m.rating >= min_rating and m.year >= min_year, movies)
    ordered = sorted(good, key=lambda m: (-m.rating, m.title))
    return tuple(map(lambda m: f"{m.title} ({m.year})", ordered))


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


# D1I: Refactoring Schritt 2 (Rename)
HIGHLIGHT_MIN_RATING = 8.5
HIGHLIGHT_MIN_YEAR = 1990


def is_highlight(movie: Movie) -> bool:
    """Ein Highlight ist gut bewertet und nicht zu alt."""
    return movie.rating >= HIGHLIGHT_MIN_RATING and movie.year >= HIGHLIGHT_MIN_YEAR


def highlight_label(movie: Movie) -> str:
    """Anzeigetext fuer ein Highlight, z.B. 'INCEPTION (Sci-Fi)'."""
    return f"{movie.title.upper()} ({movie.genre})"


def highlights(movies: Movies) -> tuple[str, ...]:
    """Highlights als Text, aelteste zuerst."""
    selected = []
    for movie in movies:
        if is_highlight(movie):
            selected.append(movie)
    selected.sort(key=lambda movie: movie.year)
    labels = []
    for movie in selected:
        labels.append(highlight_label(movie))
    return tuple(labels)


# D1A: lineare Suche in der Liste (O(n))
def find_by_id(movies: Movies, movie_id: int) -> Movie | None:
    """Sucht einen Film durch alle Elemente hindurch."""
    return next((m for m in movies if m.id == movie_id), None)


# D1A: Index als dict (Aufbau O(n), danach Suche O(1))
def movie_index(movies: Movies) -> dict[int, Movie]:
    """Baut ein dict von Id auf Film."""
    return {m.id: m for m in movies}
