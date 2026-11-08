"""Flask-App der Filmdatenbank. Hier stehen nur die Routen, die Logik ist in movies.py."""
from dataclasses import asdict

from flask import Flask, jsonify, request

from movies import (
    SORT_KEYS, Movie, add_movie, average_rating, best_rating, filter_by_genre, filter_by_years,
    process, load_movies, movie_index, next_id, rank_movies, ranked_genre_stats, recommend,
    search_title, sort_by, summary, titles, top_movies, total_rating,
)

app = Flask(__name__)
# A1I: der Zustand ist ein Tuple. POST /movies weist ein neues Tuple zu (keine Mutation).
app.config["MOVIES"] = load_movies()

TODAY_YEAR = 2026


def current_movies():

    """Gibt den aktuellen Zustand (Tuple von Filmen) zurueck."""
    return app.config["MOVIES"]


def to_json(movies):
    """Wandelt Filme in eine JSON-Antwort um."""
    return jsonify([asdict(m) for m in movies])



# C2B: alle Filter sind kombinierbar
@app.route("/movies")
def get_movies():
    """Alle Filme, optional gefiltert mit q, genre, year_from, year_to und sortiert mit sort."""
    movies = current_movies()
    q = request.args.get("q")
    genre = request.args.get("genre")
    year_from = request.args.get("year_from", default=0, type=int)
    year_to = request.args.get("year_to", default=9999, type=int)
    if q:
        movies = search_title(movies, q)
    if genre:
        movies = filter_by_genre(movies, genre)
    movies = filter_by_years(movies, year_from, year_to)
    scorer = SORT_KEYS.get(request.args.get("sort", ""))
    if scorer:
        movies = sort_by(movies, scorer)
    return to_json(movies)


@app.route("/movies", methods=["POST"])
def post_movie():
    """Fuegt einen Film hinzu (immutable: neues Tuple wird zugewiesen)."""
    data = request.get_json(silent=True)
    error = validate_movie_data(data)
    if error:
        return jsonify({"error": error}), 400
    movies = current_movies()
    movie = Movie(next_id(movies), data["title"].strip(), data["genre"].strip(),
                  data["year"], float(data["rating"]))
    app.config["MOVIES"] = add_movie(movies, movie)
    return jsonify(asdict(movie)), 201


def validate_movie_data(data):
    """Prueft die Eingabe fuer POST /movies. Gibt eine Fehlermeldung oder None zurueck."""
    if not isinstance(data, dict):
        return "JSON-Objekt erwartet"
    for field in ("title", "genre"):
        if not isinstance(data.get(field), str) or not data[field].strip():
            return f"{field} fehlt oder ist leer"
    if not isinstance(data.get("year"), int) or isinstance(data["year"], bool):
        return "year muss eine ganze Zahl sein"
    rating = data.get("rating")
    if isinstance(rating, bool) or not isinstance(rating, (int, float)) or not 0 <= rating <= 10:
        return "rating muss eine Zahl zwischen 0 und 10 sein"
    return None


@app.route("/movies/<int:movie_id>")
def get_movie(movie_id):
    """Ein Film nach Id (Suche ueber den dict-Index)."""
    movie = movie_index(current_movies()).get(movie_id)
    if movie is None:
        return jsonify({"error": "Film nicht gefunden"}), 404
    return jsonify(asdict(movie))


@app.route("/movies/titles")
def get_titles():
    """Nur die Titel."""
    return jsonify(titles(current_movies()))


# B1A: die Route benutzt die deklarative Variante
@app.route("/movies/top")
def get_top():
    """Die n besten Filme."""
    n = request.args.get("n", default=5, type=int)
    return to_json(top_movies(current_movies(), n))


# C1A
@app.route("/movies/ranking")
def get_ranking():
    """Rangliste nach Gesamt-Score."""
    year = request.args.get("year", default=TODAY_YEAR, type=int)
    return to_json(rank_movies(current_movies(), year))




# C2I
@app.route("/movies/recommend")
def get_recommend():
    """Empfehlungen: gut bewertet und ab 2000."""
    return jsonify(recommend(current_movies()))


@app.route("/movies/highlights")
def get_highlights():
    """Highlights (Ergebnis des Refactorings)."""
    return jsonify(process(current_movies()))



@app.route("/stats/total")
def get_total():
    """Summe, Durchschnitt und beste Bewertung."""
    movies = current_movies()
    return jsonify({
        "total": round(total_rating(movies), 2),
        "average": round(average_rating(movies), 3),
        "best": best_rating(movies),
        "summary": summary(movies),
    })


# C2A
@app.route("/stats/genres")
def get_genre_stats():
    """Anzahl und Durchschnitt pro Genre, beste zuerst."""
    return jsonify(ranked_genre_stats(current_movies()))


if __name__ == "__main__":
    app.run(debug=True)
