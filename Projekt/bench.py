"""D1A: Messung Suche nach Id in list (linear) gegen dict (Index), dazu lru_cache vorher/nachher."""
import platform
import random
import statistics
import timeit
from datetime import date

from movies import Movie, find_by_id, load_movies, movie_index

SIZE = 100_000
LOOKUPS = 1_000
REPEATS = 5
GENRES = ("Action", "Drama", "Sci-Fi", "Animation")


def make_movies(size):
    """Erzeugt size zufaellige Filme mit festem Seed (wiederholbar)."""
    random.seed(42)
    return tuple(
        Movie(i, f"Film {i}", random.choice(GENRES), random.randint(1950, 2025),
              round(random.uniform(1, 10), 1))
        for i in range(1, size + 1)
    )


def median_ms(stmt, number):
    """Fuehrt stmt REPEATS mal aus und gibt den Median in Millisekunden zurueck."""
    runs = timeit.repeat(stmt, number=number, repeat=REPEATS)
    return statistics.median(runs) * 1000


def main():
    """Fuehrt alle Messungen aus und gibt die Resultate aus."""
    movies = make_movies(SIZE)
    random.seed(7)
    ids = [random.randint(1, SIZE) for _ in range(LOOKUPS)]
    index = movie_index(movies)

    linear = median_ms(lambda: [find_by_id(movies, i) for i in ids], 1)
    indexed = median_ms(lambda: [index.get(i) for i in ids], 1)
    build = median_ms(lambda: movie_index(movies), 1)
    uncached = median_ms(load_movies.__wrapped__, 10_000)
    cached = median_ms(load_movies, 10_000)

    print(f"Python {platform.python_version()}, {date.today().isoformat()}, {SIZE} Filme, "
          f"{LOOKUPS} Suchen, Median aus {REPEATS} Laeufen")
    print(f"list (linear, find_by_id): {linear:10.3f} ms")
    print(f"dict (index.get):          {indexed:10.3f} ms")
    print(f"dict einmal aufbauen:      {build:10.3f} ms")
    print(f"Faktor list/dict:          {linear / indexed:10.0f} x")
    print(f"load_movies ohne Cache (10000x): {uncached:8.3f} ms")
    print(f"load_movies mit Cache (10000x):  {cached:8.3f} ms")


if __name__ == "__main__":
    main()
