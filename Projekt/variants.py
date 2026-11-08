"""A1A: Dieselbe Aufgabe (Durchschnittsbewertung pro Genre) in drei Stilen."""
from functools import reduce


# A1A: prozedural (Schleifen und Hilfsvariablen)
def average_per_genre_procedural(movies):
    """Durchschnitt pro Genre mit Schleife und Hilfs-dicts."""
    totals = {}
    counts = {}
    for movie in movies:
        if movie.genre not in totals:
            totals[movie.genre] = 0.0
            counts[movie.genre] = 0
        totals[movie.genre] += movie.rating
        counts[movie.genre] += 1
    result = {}
    for genre in sorted(totals):
        result[genre] = round(totals[genre] / counts[genre], 2)
    return result


# A1A: objektorientiert (Klasse mit Zustand und Methoden)
class MovieStats:
    """Sammelt Bewertungen pro Genre und berechnet den Durchschnitt."""

    def __init__(self):
        self._ratings = {}

    def add(self, movie):
        """Nimmt einen Film in die Statistik auf (veraendert den Zustand)."""
        self._ratings.setdefault(movie.genre, []).append(movie.rating)

    def averages(self):
        """Gibt den Durchschnitt pro Genre zurueck."""
        return {genre: round(sum(values) / len(values), 2)
                for genre, values in sorted(self._ratings.items())}


def average_per_genre_oo(movies):
    """Durchschnitt pro Genre mit der Klasse MovieStats."""
    stats = MovieStats()
    for movie in movies:
        stats.add(movie)
    return stats.averages()


# A1A: funktional (reduce und Comprehension, keine Mutation)
def average_per_genre_functional(movies):
    """Durchschnitt pro Genre mit reduce, ohne Mutation."""
    def step(acc, movie):
        count, total = acc.get(movie.genre, (0, 0.0))
        return {**acc, movie.genre: (count + 1, total + movie.rating)}
    grouped = reduce(step, movies, {})
    return {genre: round(total / count, 2) for genre, (count, total) in sorted(grouped.items())}
