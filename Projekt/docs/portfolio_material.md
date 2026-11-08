# Material pro Feld (kein Fliesstext)

Stand: 08.11.2026, Python 3.14.3. `pytest`: 60 Tests grün. `pylint app.py movies.py variants.py bench.py`: 10.00/10.
Zeilennummern beziehen sich auf den aktuellen Stand der Dateien.

---

### A1B  (B, Mindestzeichen: 600, Ziel 660)
- Feature im Projekt: Zusammenfassung der Filmliste ("12 Filme, Durchschnitt 8.36"), benutzt in `/stats/total`
- Fundort: `movies.py`, `print_summary` Zeilen 41–45, `summary` Zeilen 49–51; `app.py`, `get_total` Zeilen 122–131
- Pflicht-Artefakt laut Moodle: Eine Prozedur und eine pure function aus dem Projekt nebeneinander
- Codeauszug: `print_summary` und `summary` (siehe `movies.py`)
- Testfälle:
  - `summary(load_movies())` -> `"12 Filme, Durchschnitt 8.36"` (zweimal aufgerufen, gleiches Resultat)
  - `summary(())` -> `"0 Filme, Durchschnitt 0.00"`
  - `print_summary(load_movies())` -> Rückgabe `None`, Konsole `"12 Filme, Durchschnitt 8.36\n"` (`capsys`)
- Git: –
- Leitfragen: Was ist ein Seiteneffekt? Warum kann man `summary` in der Route benutzen, `print_summary` aber nicht? Was heisst referentielle Transparenz an diesem Beispiel?
- Typische Fallen: "pure = ohne print" ist zu wenig (auch keine globalen Daten lesen/ändern); Vergleich zu OO/prozedural vergessen.

### A1I  (I, Mindestzeichen: 1000, Ziel 1100)
- Feature im Projekt: Film hinzufügen (`POST /movies`) und Bewertung ändern
- Fundort: `movies.py`, `add_movie_mutating` Zeilen 124–126, `add_movie` Zeilen 130–134, `rate_movie` Zeilen 138–140; `app.py`, Zeile 14 und `post_movie` Zeilen 49–60
- Pflicht-Artefakt laut Moodle: Ein Codebeispiel mit Mutation und die immutable Variante davon
- Codeauszug: `add_movie_mutating` neben `add_movie`, dazu `app.config["MOVIES"] = add_movie(movies, movie)`
- Testfälle:
  - `add_movie_mutating(liste, dune)` -> `len(liste) == 13` (Eingabe verändert)
  - `add_movie(MOVIES, dune)` -> neues Tuple mit 13, `len(MOVIES) == 12` (Eingabe unverändert)
  - Edge Case: `add_movie(MOVIES, Movie(1, ...))` -> `ValueError` (doppelte Id)
  - `rate_movie(inception, 9.5)` -> neuer Film 9.5, Original bleibt 8.8
  - `MOVIES[0].rating = 1.0` -> `FrozenInstanceError` (Unterklasse von `AttributeError`)
  - Route: `POST /movies` -> 201, danach `GET /movies` 13 Filme, `load_movies()` weiterhin 12
- Git: Vorschlag: zuerst nur `add_movie_mutating` committen ("A1I: Mutation"), dann `add_movie`/`rate_movie` ("A1I: immutable Variante")
- Leitfragen: Was genau ändert sich im Speicher bei `append`? Warum bleibt `load_movies()` trotz Cache sicher? Wer könnte sonst noch die Liste in der Hand haben?
- Typische Fallen: "immutable = schneller" behaupten (nicht immer wahr); vergessen, dass die Route trotzdem einen Zustand hat (er wird neu zugewiesen).

### A1A  (A, Mindestzeichen: 1400, Ziel 1550)
- Feature im Projekt: Durchschnittsbewertung pro Genre
- Fundort: `variants.py`, `average_per_genre_procedural` Zeilen 6–19, `MovieStats` Zeilen 23–36, `average_per_genre_oo` Zeilen 39–44, `average_per_genre_functional` Zeilen 48–54
- Pflicht-Artefakt laut Moodle: Dieselbe Aufgabe in OO, prozedural und funktional, mit Bewertung
- Codeauszug: die drei Funktionen (je 5–14 Zeilen)
- Testfälle:
  - alle drei mit `load_movies()` -> `{"Action": 8.3, "Animation": 8.1, "Drama": 8.37, "Sci-Fi": 8.53}`
  - Edge Case: alle drei mit `()` -> `{}`
- Material für die Bewertung:

  - Prozedural: 13 Zeilen, Schritt für Schritt mit 2 Hilfs-dicts, gut testbar. `totals` und `counts` können auseinanderlaufen. Schlecht parallelisierbar, aber schnell.
  - OO: 13 Zeilen (Klasse + Funktion), der Name `MovieStats` erklärt viel. Die Reihenfolge der `add`-Aufrufe zählt, und `_ratings` kann von aussen verändert werden. Schlecht parallelisierbar, speichert alle Werte in Listen.
  - Funktional: 6 Zeilen, kurz, aber `reduce` muss man kennen. Sehr gut testbar, keine Mutation, gut parallelisierbar. Nachteil: `{**acc, ...}` kopiert das dict bei jedem Film.

- Leitfragen: Welchen Stil würde ich bei 1 Million Filmen nehmen? Wann ist OO trotzdem besser (z.B. Statistik wächst über viele Requests)?
- Typische Fallen: nur beschreiben statt bewerten; kein klares Urteil.

### B1B  (B, Mindestzeichen: 600, Ziel 660)
- Feature im Projekt: ganze Datenschicht `movies.py`
- Fundort: siehe `docs/functional_design.md` (Tabelle mit Datei, Funktion, Zeilen)
- Pflicht-Artefakt laut Moodle: Die Elemente des Functional Design im Projekt benannt, je mit Fundort
- Codeauszug: `Movie` (Zeilen 7–14), `filter_by_genre` (55–57), Verkettung `top_movies(filter_by_genre(load_movies(), "Action"), 3)`
- Testfälle:
  - `top_movies(filter_by_genre(load_movies(), "Action"), 3)` -> The Dark Knight, Gladiator, John Wick
  - `MOVIES[0].rating = 1.0` -> Fehler (frozen)
- Leitfragen: Warum geben alle Operatoren wieder ein Tuple zurück? Was ist der Unterschied zwischen Constructor und Operator?
- Typische Fallen: Fundort fehlt; nur Begriffe ohne Projektbezug.

### B1I  (I, Mindestzeichen: 1000, Ziel 1100)
- Feature im Projekt: Ranking `/movies/ranking`
- Fundort: `docs/design_ranking.md` (Entwurf), Umsetzung `movies.py` Zeilen 170–190
- Pflicht-Artefakt laut Moodle: Ein Design-Blatt: deklarative Anforderungen, Datenfluss, geplante Operatoren
- Codeauszug: Datenfluss-Zeile und Signaturen aus dem Design-Blatt, dazu `rank_movies`
- Soll/Ist-Vergleich:
  - Soll: `load_movies → filter → map(score) → sorted → top n → jsonify`
  - Ist: `current_movies() → sorted(key=(-final_score, title)) → jsonify`. Kein eigener `map`-Schritt: der Score wird im `key` von `sorted` berechnet. Kein `filter` und kein `top n` in der Route (die bestehenden Operatoren könnten davor gehängt werden).
  - Neu dazugekommen: Runden auf 3 Stellen (wegen Gleichstand Forrest Gump / The Matrix 8.88), Zukunftsfilme ohne Bonus.
- Testfälle:
  - `rank_movies(load_movies(), 2026)` -> beginnt mit The Dark Knight, Inception, Interstellar, Joker
  - `rank_movies((), 2026)` -> `()`
- Git: Design-Blatt **vor** dem Ranking-Code committen (eigener Commit "B1I: Design-Blatt Ranking")
- Leitfragen: Was hat das Design-Blatt beim Programmieren geholfen? Was habe ich im Entwurf nicht vorhergesehen?
- Typische Fallen: Design nachträglich schreiben; kein Soll/Ist-Vergleich.

### B1A  (A, Mindestzeichen: 1400, Ziel 1550)
- Feature im Projekt: Top-Liste `/movies/top?n=5`
- Fundort: `movies.py`, `top_movies_imperative` Zeilen 149–160, `top_movies` Zeilen 164–166; `app.py`, `get_top` Zeilen 94–98
- Pflicht-Artefakt laut Moodle: Eine imperative Route deklarativ umgesetzt, Vor- und Nachteile begründet
- Codeauszug: beide Funktionen nebeneinander
- Testfälle (derselbe Test für beide, `@pytest.mark.parametrize`):
  - `n=3` -> The Dark Knight, Inception, Forrest Gump (Gleichstand 8.8: Reihenfolge der Daten bleibt)
  - Edge Cases: `n=0` -> `()`, `n=-1` -> `()`, `n=50` -> alle 12, leere Liste -> `()`
- Vor- und Nachteile:
  - imperativ: 12 Zeilen, Ablauf sichtbar, kann früh abbrechen; aber O(n·k), viele Hilfsvariablen, `remove` entfernt das erste gleiche Element
  - deklarativ: 1 Zeile, O(n log n), stabil, liest sich wie die Anforderung; aber `[:n]` mit negativem n würde Elemente abschneiden (darum `max(n, 0)`), sortiert immer alles
- Git: Vorschlag: zuerst nur `top_movies_imperative` + Route committen ("B1A: Top imperativ"), dann `top_movies` ("B1A: Top deklarativ")
- Leitfragen: Wann würde ich `heapq.nlargest` nehmen? Was war der Fehler mit negativem n?
- Typische Fallen: nur zeigen statt abwägen; keine Entscheidung.

### C1B  (B, Mindestzeichen: 600, Ziel 660)
- Feature im Projekt: Ranking-Score
- Fundort: `movies.py`, `base_score` 170–172, `recency_bonus` 175–179, `final_score` 182–184
- Pflicht-Artefakt laut Moodle: Ein Algorithmus des Projekts mit Beispieldurchlauf Input → Output
- Beispieldurchlauf (Inception, 2010, Bewertung 8.8, today_year 2026):

  - Input: `Movie(1, "Inception", "Sci-Fi", 2010, 8.8)`
  - `base_score`: Bewertung = 8.8
  - `recency_bonus`: 2010 ≤ 2026, also (2010 − 1990) × 0.02 = 0.4
  - `final_score`: round(8.8 + 0.4, 3) = 9.2

- Testfälle: `test_manual_example_inception` (8.8 / 0.4 / 9.2), `test_recency_bonus_edge_cases` (1980 -> 0.0, 2030 -> 0.0)
- Leitfragen: Warum `pytest.approx` beim Bonus? Was passiert bei einem Film von 1980?
- Typische Fallen: Rechnung im Text stimmt nicht mit dem Code überein.

### C1I  (I, Mindestzeichen: 1000, Ziel 1100)
- Feature im Projekt: Ranking-Score
- Fundort: `movies.py`, Zeilen 170–184
- Pflicht-Artefakt laut Moodle: Derselbe Algorithmus in Teilfunktionen zerlegt, mit Signaturen
- Signaturen:
  - `base_score(movie: Movie) -> float`
  - `recency_bonus(movie: Movie, today_year: int) -> float`
  - `final_score(movie: Movie, today_year: int) -> float`
- Warum diese Zerlegung: Basis und Bonus ändern sich aus verschiedenen Gründen; Bonus einzeln testbar (Zukunft, alt); `today_year` als Parameter statt `datetime.now()`
- Testfälle: Bonus 2030 -> 0.0, Bonus 1980 -> 0.0, `final_score(zero_film_2020, 2026)` -> 0.6
- Leitfragen: Warum ist `base_score` eine eigene Funktion, obwohl sie nur `movie.rating` zurückgibt?
- Typische Fallen: Signaturen ohne Typen; Zerlegung ohne Begründung.

### C1A  (A, Mindestzeichen: 1400, Ziel 1550)
- Feature im Projekt: Rangliste `/movies/ranking`
- Fundort: `movies.py`, `rank_movies` Zeilen 188–190; `app.py`, `get_ranking` Zeilen 102–106
- Pflicht-Artefakt laut Moodle: Komposition zu einem Ablauf, mit Testfällen inkl. Edge Case
- Rangliste 2026 (echte Werte): The Dark Knight 9.36, Inception 9.2, Interstellar 9.18, Joker 8.98, Forrest Gump 8.88, The Matrix 8.88, Gladiator 8.7, Toy Story 8.4, Avatar 8.28, Shrek 8.12, Titanic 8.04, John Wick 7.88
- Testfälle: bester zuerst; Gleichstand 8.88 -> Forrest Gump vor The Matrix; leere Liste -> `()`; Bewertung 0 -> Score 0.6; Zukunftsfilm 9.1 (2030) hinter The Dark Knight
- Varianten zum Vergleichen:
  - A: `sorted(key=lambda m: (-final_score(m, y), m.title))` (gewählt)
  - B: zwei Sortierungen (`sorted` nach Titel, dann stabil nach Score `reverse=True`)
  - C: vorher `map` auf (Score, Film)-Paare, sortieren, wieder auspacken (wie im Design-Blatt)
- Leitfragen: Was wäre ohne `round(..., 3)` passiert? Wie oft wird `final_score` pro Film aufgerufen (einmal, `key` wird gecacht)?
- Typische Fallen: nur Normalfall testen; keine zweite Variante.

### C2B  (B, Mindestzeichen: 600, Ziel 660)  Feature 1: Suche und Basis-Operationen
- Fundort: `movies.py`, Zeilen 55–120 (`filter_by_genre`, `search_title`, `filter_by_years`, `titles`, `total_rating`, `rating_of`, `SORT_KEYS`, `sort_by`); `app.py`, `get_movies` Zeilen 30–46
- Pflicht-Artefakt laut Moodle: Funktion in einer Variable gespeichert, Map/Filter/Reduce je einzeln
- Beispiele mit Ausgabe:
  - Variable: `scorer = rating_of`; `sort_by(MOVIES, scorer)[0].title` -> `"John Wick"`
  - filter: `filter_by_genre(MOVIES, "Action")` -> 3 Filme
  - map: `titles(MOVIES)[:2]` -> `("Inception", "The Dark Knight")`
  - reduce: `total_rating(MOVIES)` -> 100.3 (`pytest.approx`)
- Route: `/movies?q=the&genre=action&year_from=2000&year_to=2010` -> nur The Dark Knight; `/movies?sort=year` -> Forrest Gump zuerst
- Leitfragen: Was ist der Unterschied zwischen `rating_of` und `rating_of()`?
- Typische Fallen: dasselbe Feature wie C2I/C2A verwenden.

### C2I  (I, Mindestzeichen: 1000, Ziel 1100)  Feature 2: Empfehlung
- Fundort: `movies.py`, `recommend` Zeilen 194–198; `app.py`, `get_recommend` Zeilen 110–113
- Pflicht-Artefakt laut Moodle: Lambda-Ausdruck und verkettetes Map/Filter/Reduce
- Kette: `filter (rating >= 8.0 und year >= 2000) -> sorted (lambda: (-rating, title)) -> map (lambda: "Titel (Jahr)")`
- Abweichung vom Plan: `sorted` vor `map`, weil nach `map` nur noch Strings da sind und man nicht mehr nach Bewertung sortieren kann.
- Testfälle: `recommend(MOVIES)` -> The Dark Knight (2008), Inception (2010), Interstellar (2014), Gladiator (2000), Joker (2019); `recommend(())` -> `()`; `recommend(MOVIES, min_rating=9.5)` -> `()`
- Leitfragen: Wann wäre eine benannte Funktion statt Lambda besser (z.B. `is_highlight` beim Refactoring)?
- Typische Fallen: Codeauszug aus C2B wiederverwenden.

### C2A  (A, Mindestzeichen: 1400, Ziel 1550)  Feature 3: Genre-Statistik
- Fundort: `movies.py`, `genre_stats` Zeilen 202–209, `ranked_genre_stats` Zeilen 213–217; `app.py`, `get_genre_stats` Zeilen 135–138
- Pflicht-Artefakt laut Moodle: Aggregation oder benutzerdefinierte Sortierung (hier beides)
- Testfälle: Sci-Fi `{"count": 4, "average": 8.53}`, Action `{"count": 3, "average": 8.3}`; leer -> `{}`; Reihenfolge Sci-Fi, Drama, Action, Animation; Gleichstand 8.0 -> Comedy vor Western
- Alternativen zum Vergleichen:

```python
# defaultdict (mutierend)
from collections import defaultdict
totals = defaultdict(lambda: [0, 0.0])
for m in movies:
    totals[m.genre][0] += 1
    totals[m.genre][1] += m.rating

# itertools.groupby (braucht vorher Sortierung nach Genre!)
from itertools import groupby
by_genre = sorted(movies, key=lambda m: m.genre)
stats = {g: list(group) for g, group in groupby(by_genre, key=lambda m: m.genre)}
```

- Vergleich: reduce = keine Mutation, aber kopiert das dict pro Film; defaultdict = schnell, kurz, aber mutiert; groupby = elegant, aber ohne Sortierung falsche Gruppen
- Leitfragen: Was passiert bei groupby ohne Sortierung? Welche Variante bei 1 Million Filmen?
- Typische Fallen: Alternative nur nennen, nicht vergleichen.

### D1B  (B, Mindestzeichen: 600, Ziel 660)
- Feature im Projekt: Highlights `/movies/highlights` (Refactoring), `load_movies` und `best_rating` (Performance)
- Fundort: `movies.py`, Zeilen 220–237 (Refactoring), Zeilen 20–22 (`lru_cache`), Zeilen 91–94 (Generator)
- Pflicht-Artefakt laut Moodle: Drei Refactoring-Techniken und zwei Performance-Massnahmen, je mit Zweck
- Refactoring-Techniken (Code der Zwischenstände siehe D1I):
  1. Extract Function: `is_highlight`, `highlight_label` aus `process` herausgelöst. Zweck: Bedingung und Format einzeln testbar und benannt.
  2. Rename: `process` -> `highlights`, `tmp` -> `selected`, `res` -> `labels`, `x`/`m` -> `movie`. Zweck: Name sagt, was zurückkommt.
  3. Replace Loop with Pipeline: zwei Schleifen -> `map(..., sorted(filter(...)))`. Zweck: keine Hilfslisten, liest sich wie die Anforderung.
- Performance-Massnahmen:
  1. `@lru_cache(maxsize=1)` auf `load_movies`. Zweck: das Tuple wird nur einmal gebaut. Messung: 10000 Aufrufe 43.677 ms -> 0.278 ms. Sicher, weil das Resultat unveränderlich ist.
  2. Generator-Ausdruck in `best_rating`: vorher `max([m.rating for m in movies])`, nachher `max((m.rating for m in movies), default=0.0)`. Zweck: keine Zwischenliste im Speicher; `default` verhindert den Absturz bei leerer Liste.
- Testfälle: `test_highlights`, `test_load_movies_is_cached`, `test_best_rating` (9.0 / leer 0.0)
- Typische Fallen: Technik nur nennen ohne Zweck.

### D1I  (I, Mindestzeichen: 1000, Ziel 1100)
- Feature im Projekt: Highlights
- Pflicht-Artefakt laut Moodle: Vorher/Nachher aus der Commit-Historie, gleiches Verhalten per Test belegt
- Git: Commit-Hashes (in Git-Historie):
  - Stand 0 (vorher): `47791a6`
  - Stand 1 Extract Function: `ec4bb36`
  - Stand 2 Rename: `5a1bcef`
  - Stand 3 Replace Loop with Pipeline: `85c0c6d` (= aktueller Code)
- Test, der alle Stände besteht (geprüft, alle 4 Stände liefern dasselbe):
  - `highlights(MOVIES)` -> FORREST GUMP (Drama), THE MATRIX (Sci-Fi), GLADIATOR (Action), THE DARK KNIGHT (Action), INCEPTION (Sci-Fi), INTERSTELLAR (Sci-Fi)
  - leer -> `()`; Film von 1985 mit 9.5 -> `()`

**Stand 0 (vorher)** – ersetzt in `movies.py` die Zeilen 220–237 (ab `# D1I` bis Ende von `highlights`):

```python
# D1I: unschoener Zwischenstand (wird refaktoriert)
def process(movies):
    """Verarbeitet die Filme."""
    tmp = []
    for m in movies:
        if m.rating >= 8.5:
            if m.year >= 1990:
                tmp.append(m)
    tmp.sort(key=lambda x: x.year)
    res = []
    for x in tmp:
        res.append(x.title.upper() + " (" + x.genre + ")")
    return tuple(res)
```

In Stand 0 und 1 heisst die Funktion `process`: in `app.py` (Import + `get_highlights`) und in `tests/test_movies.py`
(Import + `test_highlights`, `test_highlights_edge_cases`) `highlights` durch `process` ersetzen.

**Stand 1 (Extract Function)** – `HIGHLIGHT_MIN_RATING`, `HIGHLIGHT_MIN_YEAR`, `is_highlight`, `highlight_label` wie im aktuellen Code, dazu:

```python
def process(movies):
    """Verarbeitet die Filme."""
    tmp = []
    for m in movies:
        if is_highlight(m):
            tmp.append(m)
    tmp.sort(key=lambda x: x.year)
    res = []
    for x in tmp:
        res.append(highlight_label(x))
    return tuple(res)
```

**Stand 2 (Rename)** – Funktion heisst jetzt `highlights`, `app.py` und Tests wieder auf `highlights` zurück:

```python
def highlights(movies):
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
```

**Stand 3 (Replace Loop with Pipeline)** – aktueller Code, `movies.py` Zeilen 235–237.

Nach jedem Stand: `pytest` (muss grün sein), dann committen.
- Leitfragen: Woran sehe ich im Diff, dass sich nur die Struktur und nicht das Verhalten geändert hat?
- Typische Fallen: Verhalten beim Refactoring ändern (z.B. andere Sortierung); Tests nachträglich anpassen.

### D1A  (A, Mindestzeichen: 1400, Ziel 1550)
- Feature im Projekt: Film nach Id `/movies/<id>`
- Fundort: `movies.py`, `find_by_id` Zeilen 241–243, `movie_index` Zeilen 247–249; `app.py`, `get_movie` Zeilen 78–84; `bench.py`
- Pflicht-Artefakt laut Moodle: Messung vorher/nachher und Begründung der gewählten Datenstruktur
- Messung (`python bench.py`, Python 3.14.3, 08.11.2026, 100000 Filme, Seed 42, 1000 Suchen, Median aus 5 Läufen):

  - list, lineare Suche (`find_by_id`), 1000 Suchen: 943.298 ms
  - dict, `index.get`, 1000 Suchen: 0.054 ms
  - dict einmal aufbauen (`movie_index`): 6.192 ms
  - Faktor list/dict: ca. 17340 x
  - `load_movies` ohne Cache, 10000 Aufrufe: 43.677 ms
  - `load_movies` mit Cache, 10000 Aufrufe: 0.278 ms

- Interpretation: list O(n) pro Suche, dict O(1) im Mittel. Der Aufbau des dict kostet einmal O(n) (6 ms = ca. 6–7 lineare Suchen). Lohnt sich ab wenigen Suchen auf denselben Daten.
- Grenzen der Messung: ein Laptop, andere Programme laufen mit; künstliche Daten; Ids 1..n zufällig gesucht; in der App sind es nur 12 Filme (dort ist der Unterschied nicht messbar); `get_movie` baut das dict pro Request neu.
- Speicher: dict braucht zusätzlich Platz für die Hash-Tabelle; Reihenfolge bleibt in Python ≥ 3.7 erhalten.
- Testfälle: `find_by_id(MOVIES, 7) == movie_index(MOVIES)[7]`; unbekannte Id -> `None`; Route `/movies/99` -> 404
- Leitfragen: Ab wie vielen Suchen lohnt sich der Index? Was müsste man ändern, damit das dict nicht bei jedem Request neu gebaut wird?
- Typische Fallen: erfundene Zahlen; nur "dict ist schneller" ohne Begründung und Grenzen.

---

## Vorschlag Commit-Reihenfolge (du committest selbst)

Nicht nötig, aber so entspricht die Historie dem Plan. Mit `git add <datei>` einzelne Dateien committen.

1. "Projekt-Setup": `.gitignore`, `requirements.txt`, `README.md`, `pytest.ini`, `count_chars.py`
2. "B1I: Design-Blatt Ranking": `docs/design_ranking.md` (Entwurf **vor** dem Ranking-Code)
3. Zuerst Stand 0 von D1I einsetzen (siehe oben), `pytest`, dann "Daten, Routen, Tests":
   `movies.py`, `app.py`, `variants.py`, `tests/`
4. D1I: Stand 1, Stand 2, Stand 3 einsetzen, jedes Mal `pytest`, je ein Commit
5. "D1A: Messung": `bench.py`
6. "Dokumentation und Portfolio": `docs/functional_design.md`, `docs/portfolio_material.md`, `portfolio/`
