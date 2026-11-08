"""Tests der Routen mit dem Flask test_client."""
import pytest

from app import app
from movies import load_movies


@pytest.fixture(name="client")
def fixture_client():
    """Frischer Client mit Ausgangszustand fuer jeden Test."""
    app.config["MOVIES"] = load_movies()
    return app.test_client()


def test_movies(client):
    response = client.get("/movies")
    assert response.status_code == 200
    assert len(response.get_json()) == 12


def test_movies_genre(client):
    assert len(client.get("/movies?genre=Action").get_json()) == 3


def test_movies_filters_combined(client):
    data = client.get("/movies?q=the&genre=action&year_from=2000&year_to=2010").get_json()
    assert [m["title"] for m in data] == ["The Dark Knight"]


def test_movies_sorted_by_year(client):
    data = client.get("/movies?sort=year").get_json()
    assert data[0]["title"] == "Forrest Gump"


def test_movie_by_id(client):
    assert client.get("/movies/7").get_json()["title"] == "Forrest Gump"
    assert client.get("/movies/99").status_code == 404


def test_titles(client):
    assert client.get("/movies/titles").get_json()[0] == "Inception"


def test_top(client):
    data = client.get("/movies/top?n=3").get_json()
    assert len(data) == 3
    assert data[0]["title"] == "The Dark Knight"


def test_post_movie(client):
    response = client.post("/movies", json={"title": "Dune", "genre": "Sci-Fi", "year": 2021, "rating": 8.0})
    assert response.status_code == 201
    assert response.get_json()["id"] == 13
    assert len(client.get("/movies").get_json()) == 13
    assert len(load_movies()) == 12


@pytest.mark.parametrize("payload", [
    None,
    {"genre": "Sci-Fi", "year": 2021, "rating": 8.0},
    {"title": "  ", "genre": "Sci-Fi", "year": 2021, "rating": 8.0},
    {"title": "Dune", "genre": "Sci-Fi", "year": "2021", "rating": 8.0},
    {"title": "Dune", "genre": "Sci-Fi", "year": 2021, "rating": 11},
])
def test_post_movie_invalid(client, payload):
    assert client.post("/movies", json=payload).status_code == 400


def test_ranking(client):
    assert client.get("/movies/ranking").get_json()[0]["title"] == "The Dark Knight"


def test_recommend(client):
    assert client.get("/movies/recommend").get_json()[0] == "The Dark Knight (2008)"


def test_highlights(client):
    assert client.get("/movies/highlights").get_json()[0] == "FORREST GUMP (Drama)"


def test_stats_total(client):
    data = client.get("/stats/total").get_json()
    assert data == {"total": 100.3, "average": 8.358, "best": 9.0, "summary": "12 Filme, Durchschnitt 8.36"}


def test_stats_genres(client):
    data = client.get("/stats/genres").get_json()
    assert data[0] == {"genre": "Sci-Fi", "count": 4, "average": 8.53}


def test_unknown_route(client):
    assert client.get("/gibtsnicht").status_code == 404
