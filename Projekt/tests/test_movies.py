"""Tests der pure Funktionen in movies.py und variants.py."""
import pytest

from movies import (
    Movie, add_movie, add_movie_mutating, average_rating, base_score, best_rating, filter_by_genre,
    filter_by_years, final_score, find_by_id, genre_stats, process, load_movies, movie_index,
    next_id, print_summary, rank_movies, ranked_genre_stats, rate_movie, rating_of, recency_bonus,
    recommend, search_title, sort_by, summary, titles, top_movies, top_movies_imperative, total_rating,
)
from variants import average_per_genre_functional, average_per_genre_oo, average_per_genre_procedural

MOVIES = load_movies()


# A1B
def test_summary_is_pure():
    assert summary(MOVIES) == "12 Filme, Durchschnitt 8.36"
    assert summary(MOVIES) == summary(MOVIES)


def test_summary_empty():
    assert summary(()) == "0 Filme, Durchschnitt 0.00"


def test_print_summary_has_side_effect_and_no_return(capsys):
    assert print_summary(MOVIES) is None
    assert capsys.readouterr().out == "12 Filme, Durchschnitt 8.36\n"


# C2B
def test_filter_by_genre():
    assert len(filter_by_genre(MOVIES, "Action")) == 3


def test_filter_by_genre_edge_cases():
    assert len(filter_by_genre(MOVIES, "sci-fi")) == 4
    assert filter_by_genre(MOVIES, "Unbekannt") == ()


def test_search_title():
    assert titles(search_title(MOVIES, "the")) == ("The Dark Knight", "The Matrix")


def test_search_title_empty_text_finds_all():
    assert search_title(MOVIES, "") == MOVIES


def test_filter_by_years():
    assert len(filter_by_years(MOVIES, 2000, 2010)) == 5


def test_filter_by_years_reversed_is_empty():
    assert filter_by_years(MOVIES, 2010, 2000) == ()


def test_titles():
    assert titles(MOVIES)[:2] == ("Inception", "The Dark Knight")
    assert titles(()) == ()


def test_total_and_average_rating():
    assert total_rating(MOVIES) == pytest.approx(100.3)
    assert average_rating(MOVIES) == pytest.approx(8.358, abs=0.001)


def test_total_and_average_empty():
    assert total_rating(()) == 0.0
    assert average_rating(()) == 0.0


def test_function_in_variable():
    scorer = rating_of
    ordered = sort_by(MOVIES, scorer)
    assert ordered[0].title == "John Wick"
    assert ordered[-1].title == "The Dark Knight"


def test_best_rating():
    assert best_rating(MOVIES) == 9.0
    assert best_rating(()) == 0.0


# A1I
NEW = Movie(13, "Dune", "Sci-Fi", 2021, 8.0)


def test_mutating_changes_input():
    movies_list = list(MOVIES)
    add_movie_mutating(movies_list, NEW)
    assert len(movies_list) == 13


def test_add_movie_keeps_original():
    result = add_movie(MOVIES, NEW)
    assert len(result) == 13
    assert len(MOVIES) == 12
    assert result[-1] == NEW


def test_add_movie_duplicate_id():
    with pytest.raises(ValueError):
        add_movie(MOVIES, Movie(1, "Kopie", "Drama", 2020, 5.0))


def test_rate_movie():
    original = MOVIES[0]
    rated = rate_movie(original, 9.5)
    assert rated.rating == 9.5
    assert original.rating == 8.8
    assert rated.title == original.title


def test_movie_is_frozen():
    with pytest.raises(AttributeError):
        MOVIES[0].rating = 1.0  # type: ignore[misc]


def test_next_id():
    assert next_id(MOVIES) == 13
    assert next_id(()) == 1


# B1A: derselbe Test fuer beide Varianten
@pytest.mark.parametrize("top", [top_movies_imperative, top_movies])
def test_top_movies(top):
    assert titles(top(MOVIES, 3)) == ("The Dark Knight", "Inception", "Forrest Gump")


@pytest.mark.parametrize("top", [top_movies_imperative, top_movies])
def test_top_movies_edge_cases(top):
    assert top(MOVIES, 0) == ()
    assert top(MOVIES, -1) == ()
    assert len(top(MOVIES, 50)) == 12
    assert top((), 3) == ()


# C1B: Beispieldurchlauf von Hand (Inception, 2010, 8.8)
def test_manual_example_inception():
    inception = MOVIES[0]
    assert base_score(inception) == 8.8
    assert recency_bonus(inception, 2026) == pytest.approx(0.4)
    assert final_score(inception, 2026) == 9.2


def test_recency_bonus_edge_cases():
    old = Movie(99, "Alt", "Drama", 1980, 7.0)
    future = Movie(98, "Zukunft", "Drama", 2030, 7.0)
    assert recency_bonus(old, 2026) == 0.0
    assert recency_bonus(future, 2026) == 0.0


# C1A
def test_rank_movies_best_first():
    ranked = titles(rank_movies(MOVIES, 2026))
    assert ranked[:4] == ("The Dark Knight", "Inception", "Interstellar", "Joker")
    assert ranked[-1] == "John Wick"


def test_rank_movies_tie_by_title():
    ranked = titles(rank_movies(MOVIES, 2026))
    assert final_score(MOVIES[6], 2026) == final_score(MOVIES[5], 2026) == 8.88
    assert ranked.index("Forrest Gump") < ranked.index("The Matrix")


def test_rank_movies_edge_cases():
    assert rank_movies((), 2026) == ()
    zero = Movie(97, "Null", "Drama", 2020, 0.0)
    future = Movie(96, "Zukunft", "Drama", 2030, 9.1)
    assert final_score(zero, 2026) == 0.6
    assert titles(rank_movies((future, MOVIES[1]), 2026)) == ("The Dark Knight", "Zukunft")


# C2I
def test_recommend():
    assert recommend(MOVIES) == (
        "The Dark Knight (2008)", "Inception (2010)", "Interstellar (2014)", "Gladiator (2000)", "Joker (2019)",
    )


def test_recommend_edge_cases():
    assert recommend(()) == ()
    assert recommend(MOVIES, min_rating=9.5) == ()


# C2A
def test_genre_stats():
    stats = genre_stats(MOVIES)
    assert stats["Sci-Fi"] == {"count": 4, "average": 8.53}
    assert stats["Action"] == {"count": 3, "average": 8.3}


def test_genre_stats_empty():
    assert genre_stats(()) == {}


def test_ranked_genre_stats_order():
    names = [row["genre"] for row in ranked_genre_stats(MOVIES)]
    assert names == ["Sci-Fi", "Drama", "Action", "Animation"]


def test_ranked_genre_stats_tie_by_name():
    movies = (Movie(1, "A", "Western", 2000, 8.0), Movie(2, "B", "Comedy", 2000, 8.0))
    assert [row["genre"] for row in ranked_genre_stats(movies)] == ["Comedy", "Western"]


# A1A: alle drei Stile liefern dasselbe
def test_three_styles_same_result():
    expected = {"Action": 8.3, "Animation": 8.1, "Drama": 8.37, "Sci-Fi": 8.53}
    assert average_per_genre_procedural(MOVIES) == expected
    assert average_per_genre_oo(MOVIES) == expected
    assert average_per_genre_functional(MOVIES) == expected


def test_three_styles_empty():
    assert average_per_genre_procedural(()) == average_per_genre_oo(()) == average_per_genre_functional(()) == {}


# D1I: Verhalten des refaktorierten Codes (derselbe Test lief schon gegen process)
def test_highlights():
    assert process(MOVIES) == (
        "FORREST GUMP (Drama)", "THE MATRIX (Sci-Fi)", "GLADIATOR (Action)",
        "THE DARK KNIGHT (Action)", "INCEPTION (Sci-Fi)", "INTERSTELLAR (Sci-Fi)",
    )


def test_highlights_edge_cases():
    assert process(()) == ()
    assert process((Movie(1, "Alt", "Drama", 1985, 9.5),)) == ()


# D1A
def test_find_by_id_and_index_agree():
    index = movie_index(MOVIES)
    assert find_by_id(MOVIES, 7) == index[7]
    assert find_by_id(MOVIES, 99) is None
    assert index.get(99) is None


def test_load_movies_is_cached():
    assert load_movies() is load_movies()
