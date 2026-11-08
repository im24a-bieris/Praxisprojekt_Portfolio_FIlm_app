# Praxisprojekt_Portfolio_FIlm_app
# PLAN_6.md: Vollständiger Auftrag für Claude Code (M323 LB02, Ziel: Note 6.0)

Lies zuerst `CLAUDE.md`, dann diese Datei ganz. Arbeite danach **Schritt für Schritt**.
Nach jedem Schritt: kurz sagen, was du getan hast, Tests laufen lassen, committen, auf mein "weiter" warten.

---

## 0. Rollen (sehr wichtig)

| Wer | Was |
|---|---|
| **Claude Code** | Baut die Flask-App mit Tests. Liefert pro Lernfeld das Material (Fundort, Codeauszug, Testfälle, Messwerte, Commits). Stellt Leitfragen. Prüft meine Texte streng nach der Checkliste. |
| **Samuel (ich)** | lese **alle Lernnachweis-Texte selbst, und ändere sie in eigenen Worten um falls nötig**

Warum so: Die Note 6.0 braucht in jedem Feld 3 Punkte ("tiefes Verständnis, begründete Entscheidungen, Reflexion").
Das zeigt nur, wer es selbst erklären kann. Bei Rückfragen des Lehrers muss ich es verstehen.


---

## 1. Rahmendaten (aus Moodle, LB02 "Portfolio")

- Einzelarbeit, Openbook. Gewichtung 55 %.
- **Praxisprojekt:** Flask-App, die möglichst viele funktionale Komponenten enthält. **Keine Todo- und keine Einkaufsliste.** Wert: 10 Punkte.
- **Portfolio:** 15 Lernnachweise (A1, B1, C1, C2, D1 je B, I, A). Je max. 3 Punkte = 45 Punkte.
- **Note = 1 + 5 × Punkte / 55.** Für eine 6.0 braucht es **55 von 55 Punkten**.
- Textumfang pro Lernnachweis (ohne Leerzeichen, Code zählt nicht):
  - B: mindestens 600 Zeichen
  - I: mindestens 1000 Zeichen
  - A: mindestens 1400 Zeichen
- Jeder Nachweis braucht ein **Code-Beispiel aus der Flask-App**.
- Sammelnachweis pro Band erlaubt (z.B. A1B+A1I+A1A in einem Dokument, 3000 Zeichen, 3 Code-Beispiele), **ausser C2**: dort B, I und A einzeln an **drei verschiedenen Features**. Derselbe Codeauszug in zwei Niveaus gibt maximal 1 Punkt.
- Reihenfolge in Moodle: I erst nach B, A erst nach I abgeschlossen.
- Fristen:
  - Moodle zeigt für "Abgabe Praxisprojekt" und alle B-Felder: **Fr 30.10.2026, 22:59** (heute ist der 04.11., also schon vorbei).
  - Stundenplan sagt: **Abgabe Portfolio Fr 06.11.2026**.
  - **Offen:** Ob die Moodle-Aufgaben noch offen sind und ob die Frist verlängert ist, muss ich beim Lehrer klären. Das Abgabeformat (PDF, Word, Link, ZIP) steht in den Moodle-Aufgaben selbst. Dazu frage ich dich nach dem Text der Aufgabe, bevor wir Teil 8 machen.

### Was 3 Punkte bringt (Checkliste, gilt für jedes Feld)
1. Begründete Entscheidung: warum diese Lösung, welche Alternative gab es?
2. Konkrete Nachweise: mindestens 2 Testfälle (Input → erwarteter Output), bei A auch Edge Case.
3. Sauberer, passender Codeauszug (5 bis 25 Zeilen) mit 2 bis 5 Sätzen Einordnung. Nicht einfach hineinkopiert. Sage, wo er im Projekt hingehört (Route, Service, Helper, Template).
4. Reflexion und Transfer: Was war schwierig? Was gelernt? Wie würde ich es nächstes Mal besser machen? Wo kann ich es wiederverwenden?
5. Das **Pflicht-Artefakt** ist vollständig da.
6. Klarer Bezug zur Kompetenz: Es wird deutlich, was genau am Beispiel die Kompetenz belegt.
7. Das Niveau-Verb stimmt: B beschreiben/erklären/anwenden, I erläutern/entwerfen/kombinieren/umsetzen, **A vergleichen/bewerten/analysieren/auswählen** (zwei Varianten gegenübergestellt und begründet entschieden).

Typische Fehler: zu viel Theorie, Snippet ohne Erklärung, "hat funktioniert" ohne Testfälle, Fülltext für die Zeichenzahl, auf A nur beschreiben, in C2 dreimal dasselbe Feature.

---

## 2. Schritt 0: Zustand prüfen (zuerst, ohne etwas zu ändern)

1. Lies `app.py` und alle anderen Dateien im Ordner. Führe `git status` und `git log --oneline` aus.
2. Erstelle eine Tabelle: Was aus Teil 3 und 4 existiert schon? Was fehlt?
3. Prüfe, ob `.venv` aktiv ist (Git Bash: `source .venv/Scripts/activate`) und `pytest` installiert ist.
4. Schlage mir den Weg vor und warte auf mein "weiter".

Stand vom 28.10.: `app.py` enthält Movie (frozen dataclass), `load_movies()`, `/movies`, `/movies?genre=...`, `/movies/titles`.
Es ist möglich, dass inzwischen mehr da ist. Verlasse dich nicht darauf.

---

## 3. Projektstruktur (Ziel)

```
film_app/
  app.py                  # nur Routen (dünn)
  movies.py               # Daten und pure Funktionen
  variants.py             # A1A: drei Stile für dieselbe Aufgabe
  bench.py                # D1A: Messung
  count_chars.py          # Hilfsskript: Zeichen im Textteil zählen
  tests/
    test_movies.py        # Tests der pure Funktionen
    test_routes.py        # Tests der Routen (Flask test_client)
  docs/
    design_ranking.md     # B1I Design-Blatt
    functional_design.md  # B1B Elemente mit Fundort
    portfolio_material.md # Material pro Feld (kein Fliesstext)
  portfolio/              # meine Texte (Markdown), je Feld eine Datei
  requirements.txt
  README.md
  .gitignore
```

`.gitignore`: `.venv/`, `__pycache__/`, `*.pyc`, `.pytest_cache/`.

Lint: Die Schule nutzt Pylint. Halte den Code frei von: Trailing Whitespace, Zeilen über 120 Zeichen,
fehlenden Docstrings (Modul, Funktion, Klasse), fehlendem Zeilenumbruch am Dateiende.
Prüfe mit `pylint app.py movies.py variants.py bench.py`.

---

## 4. Bauplan (jeder Schritt = eigener Commit, kleine Commit-Messages auf Deutsch oder Englisch, klar)

### Schritt 1: Setup
- `git init`, `.gitignore`, erster Commit "Projekt-Setup".
- `pip install pytest pylint`, `pip freeze > requirements.txt`.

### Schritt 2: Daten und Grundfunktionen nach `movies.py`
- Verschiebe `Movie`, `load_movies`, `filter_by_genre` aus `app.py` nach `movies.py`.
- `app.py` importiert daraus. Teste im Browser: `/movies`, `/movies?genre=Action`, `/movies/titles`.
- Commit "Daten und Filter nach movies.py".

### Schritt 3: Prozedur vs. pure function (Feld A1B)
- Füge in `movies.py` zwei Funktionen hinzu, die **dasselbe Ziel** haben, aber verschieden sind:
  - **Prozedur** `print_summary(movies)`: gibt mit `print` aus, hat **keinen Return**, Seiteneffekt.
  - **Pure function** `summary(movies)`: gibt einen String zurück, kein Seiteneffekt, gleiches Input gibt gleiches Output.
- Marker `# A1B` im Code. Commit "A1B: Prozedur und pure function".

### Schritt 4: Filter, Suche, Titel, Summe (Feld C2B, Feature "Suche und Basis-Operationen")
- Funktionen: `search_title`, `filter_by_years`, `titles` (map), `total_rating` (reduce), `filter_by_genre` (filter).
- Routen: `/movies?q=...&genre=...&year_from=...&year_to=...` (alle Filter kombinierbar),
  `/movies/titles`, `/stats/total`.
- Zusätzlich: eine Funktion in einer Variable speichern und weitergeben (für C2B Pflichtartefakt),
  z.B. `scorer = rating_of` und `sort_by(movies, scorer)`.
- map, filter, reduce **je einzeln** und gut sichtbar in je einer kleinen Funktion.
- Marker `# C2B`. Commit "C2B: Suche, map, filter, reduce".

### Schritt 5: Mutation vs. immutable (Feld A1I)
- Erst die **mutierende** Variante bauen und committen: `add_movie_mutating(movies_list, movie)`,
  die eine Liste mit `append` verändert (Commit "A1I: Mutation").
- Danach die **immutable** Variante: `add_movie(movies, movie)` gibt `movies + (movie,)` zurück und
  `rate_movie(movie, rating)` nutzt `dataclasses.replace`. Commit "A1I: immutable Variante".
- Zeige per Test, dass die Eingabe bei der immutablen Variante **unverändert** bleibt und bei der mutierenden verändert wird.
- Route `POST /movies` benutzt die immutable Variante (Zustand wird in einer Variablen neu zugewiesen).

### Schritt 6: Top-Liste imperativ, dann deklarativ (Feld B1A, ergibt auch echtes Vorher/Nachher)
- **Erst imperativ:** `/movies/top?n=5` mit `for`-Schleife, Hilfsliste und `if`. Commit "B1A: Top imperativ".
- Test schreiben, der grün ist.
- **Dann deklarativ:** dieselbe Route mit `sorted(movies, key=lambda m: m.rating, reverse=True)[:n]`.
  Derselbe Test muss weiter grün sein. Commit "B1A: Top deklarativ".
- Die imperative Variante bleibt im Git-Verlauf (und als kurzer Auszug in `docs/portfolio_material.md`).

### Schritt 7: Design-Blatt **bevor** der Algorithmus gebaut wird (Feld B1I)
- `docs/design_ranking.md` schreiben und **committen, bevor** Schritt 8 beginnt. Inhalt:
  - Deklarative Anforderungen: "Gib die Filme geordnet nach Gesamt-Score zurück. Der Score ist die Bewertung plus ein Bonus für neuere Filme."
  - Datenfluss als Pfeile: `load_movies → filter → map(score) → sorted → top n → jsonify`.
  - Geplante Operatoren: filter, map, sorted, reduce, mit Signaturen.
  - Entscheidungen und Alternativen.
- Commit "B1I: Design-Blatt Ranking". (Das Design-Blatt ist ein Entwurf **vor** der Umsetzung, nicht nachträglich.)

### Schritt 8: Algorithmus Ranking (Felder C1B, C1I, C1A)
- Teilfunktionen mit klaren Signaturen: `base_score(movie)`, `recency_bonus(movie, today_year)`, `final_score(movie, today_year)`.
- Komposition: `rank_movies(movies, today_year)` sortiert nach Score, bei Gleichstand nach Titel.
- Route `/movies/ranking`. `today_year` wird als Parameter übergeben (nicht `datetime.now()` in der Funktion, sonst nicht pure).
- Edge Cases testen: leere Liste, Gleichstand, Film aus der Zukunft, Bewertung 0.
- Beispieldurchlauf für C1B: ein Film von Hand durchrechnen (Input → base_score → bonus → final) und als Test festhalten.
- Marker `# C1B`, `# C1I`, `# C1A`. Commit "C1: Ranking-Algorithmus".

### Schritt 9: Empfehlung mit Lambda und Verkettung (Feld C2I, **anderes Feature**)
- `/movies/recommend`: `filter` (Bewertung >= 8.0 und Jahr >= 2000), dann `map` auf "Titel (Jahr)", dann `sorted` mit Lambda.
- Das ist **nicht** dasselbe Feature wie Schritt 4 und nicht wie Schritt 10.
- Marker `# C2I`. Commit "C2I: Empfehlung".

### Schritt 10: Genre-Statistik / Aggregation (Feld C2A, **drittes Feature**)
- `/stats/genres`: Anzahl und Durchschnitt pro Genre mit `reduce` (siehe Referenz `genre_stats`).
- Zusätzlich eine **benutzerdefinierte Sortierung** mit `key=` und mehreren Kriterien (z.B. Genre-Statistik nach Durchschnitt absteigend, dann nach Name).
- Beschreibe schriftlich eine Alternative (z.B. `itertools.groupby` oder `collections.defaultdict`) und vergleiche. Das braucht Niveau A.
- Marker `# C2A`. Commit "C2A: Genre-Statistik".

### Schritt 11: Drei Stile für dieselbe Aufgabe (Feld A1A)
- In `variants.py`: "Durchschnittsbewertung pro Genre" **dreimal**:
  - **prozedural:** Funktion mit Schleifen und Hilfsvariablen,
  - **OO:** Klasse `MovieStats` mit Zustand und Methoden,
  - **funktional:** `reduce` / Comprehension, keine Mutation.
- Ein Test prüft, dass alle drei **dasselbe Ergebnis** liefern.
- Sammle Material für die Bewertung: Lesbarkeit, Testbarkeit, Fehleranfälligkeit, Parallelisierbarkeit, Länge.
- Marker `# A1A`. Commit "A1A: drei Stile".

### Schritt 12: Functional-Design-Elemente benennen (Feld B1B)
- `docs/functional_design.md`: Liste der Elemente **mit Fundort** (Datei, Funktion, Zeilen):
  - **Immutable Datentypen:** `Movie` (frozen dataclass), Tuples statt Listen.
  - **Constructors:** `Movie(...)`, `load_movies()`.
  - **Composable Operators:** `filter_by_genre`, `search_title`, `filter_by_years`, `top_movies`, `rank_movies`.
  - Wie sie sich verketten lassen (Beispiel: `top_movies(filter_by_genre(load_movies(), "Action"), 3)`).
- Commit "B1B: Functional-Design-Elemente".

### Schritt 13: Tests vollständig machen
- Siehe Teil 5. `pytest` muss grün sein. `pylint` muss sauber sein (Ziel: 10/10).

### Schritt 14: Refactoring und Performance (Felder D1B, D1I)
- **Mindestens 3 Refactoring-Techniken**, jede als eigener Commit mit Vorher/Nachher, **Tests bleiben grün** (gleiches Verhalten):
  1. **Extract Function** (lange Funktion in Teilfunktionen zerlegen),
  2. **Rename** (unklare Namen durch klare ersetzen),
  3. **Replace Loop with Pipeline** (Schleife durch map/filter/sorted ersetzen).
  Falls im bisherigen Code kein Anlass besteht, baue bewusst eine unschöne Stelle (z.B. eine `process(movies)`-Funktion mit Schleife und verschachtelten `if`) **als ehrlichen Zwischenstand**, committe sie und refaktoriere sie dann.
- **Zwei Performance-Massnahmen**, z.B.
  - `functools.lru_cache` auf `load_movies` (oder auf eine teure pure Funktion),
  - Generator-Ausdruck statt Liste bei grossen Daten (`sum(m.rating for m in movies)`).
  Jede mit Zweck (Was wird schneller? Warum?).
- Für D1I: Commit-Hashes von Vorher und Nachher notieren und zeigen, dass derselbe Test beides besteht.

### Schritt 15: Messung (Feld D1A)
- `bench.py`: erzeuge 100'000 Filme (mit festem Seed `random.seed(42)`).
- Vergleiche **Suche nach id** in `list` (lineare Suche) und `dict` (Index) mit `timeit`. Mindestens 5 Wiederholungen, Median.
- Optional: zweite Messung mit `lru_cache` vorher/nachher.
- Speichere die **echten** Zahlen in `docs/portfolio_material.md` (inkl. Python-Version und Datum).
- Ich begründe die Wahl der Datenstruktur selbst (Zeitkomplexität O(n) vs. O(1), Speicher, Reihenfolge).

### Schritt 16: Material fürs Portfolio
- `docs/portfolio_material.md` für alle 15 Felder erstellen (Format siehe Teil 7). **Keine Fliesstexte.**

### Schritt 17: Abgabe vorbereiten
- `requirements.txt` aktualisieren (`pip freeze > requirements.txt`).
- `README.md` mit 3 Zeilen: venv aktivieren, `pip install -r requirements.txt`, `flask run --debug`.
- ZIP vom Projektordner **ohne** `.venv`, `__pycache__`, `.pytest_cache`.
- Prüfe auf einem frischen Ordner: ZIP entpacken, venv anlegen, `pip install -r requirements.txt`, `pytest` und `flask run`.

---

## 5. Tests (Pflicht)

`tests/test_movies.py` (pure Funktionen), `tests/test_routes.py` (Routen mit `app.test_client()`).
Mindestens 2 Testfälle pro Funktion, wo sinnvoll mit Edge Case:

| Funktion | Normalfall | Edge Case |
|---|---|---|
| `filter_by_genre` | "Action" ergibt 3 Filme | "sci-fi" (klein) ergibt 4, "Unbekannt" ergibt leeres Tuple |
| `search_title` | "the" findet mehrere | leerer Text findet alle |
| `filter_by_years` | 2000 bis 2010 ergibt 5 | year_from > year_to ergibt leer |
| `titles` | erste zwei Titel stimmen | leere Eingabe ergibt `()` |
| `total_rating` / `average_rating` | Durchschnitt aller Filme ca. 8.358 (`pytest.approx`) | leere Liste ergibt 0.0 |
| `add_movie` | Länge + 1, Original unverändert | Duplikat-Id: Verhalten festlegen und testen |
| `rate_movie` | neuer Film hat neue Bewertung | Original bleibt gleich (frozen) |
| `top_movies` | n=3 ergibt Dark Knight, Inception, Forrest Gump | n=0 ergibt leer, n grösser als Anzahl ergibt alle |
| `genre_stats` | Sci-Fi: count 4, average 8.53 | leere Liste ergibt `{}` |
| `rank_movies` | bester Film zuerst (2026) | Gleichstand nach Titel, leere Liste, Zukunftsjahr |

Hinweis: `total_rating` summiert Fliesskommazahlen (z.B. 100.30000000000001). Immer `pytest.approx(...)` benutzen.

Routen-Tests: `/movies` (Status 200, 12 Elemente), `/movies?genre=Action` (3 Elemente), `/movies/top?n=3` (3 Elemente, erster ist "The Dark Knight"),
`POST /movies` mit JSON (Status 201), unbekannte Route (Status 404).

---

## 6. Referenzcode `movies.py` (geprüft, läuft; Ausgangspunkt, nicht auswendig kopieren)

Du darfst ihn anpassen. Er ist so gebaut, dass er zu den Schritten passt.

```python
"""Pure Funktionen und Daten der Filmdatenbank."""
from dataclasses import dataclass, replace
from functools import reduce


@dataclass(frozen=True)
class Movie:
    """Ein Film (unveraenderlich)."""
    id: int
    title: str
    genre: str
    year: int
    rating: float


def load_movies():
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


def filter_by_genre(movies, genre):
    """Behaelt nur Filme des Genres (gross/klein egal)."""
    return tuple(filter(lambda m: m.genre.lower() == genre.lower(), movies))


def search_title(movies, text):
    """Behaelt Filme, deren Titel den Text enthaelt."""
    return tuple(filter(lambda m: text.lower() in m.title.lower(), movies))


def filter_by_years(movies, year_from, year_to):
    """Behaelt Filme zwischen year_from und year_to (inklusive)."""
    return tuple(filter(lambda m: year_from <= m.year <= year_to, movies))


def titles(movies):
    """Gibt nur die Titel zurueck."""
    return tuple(map(lambda m: m.title, movies))


def total_rating(movies):
    """Summe aller Bewertungen (reduce)."""
    return reduce(lambda acc, m: acc + m.rating, movies, 0.0)


def average_rating(movies):
    """Durchschnittsbewertung, 0.0 bei leerer Liste."""
    if not movies:
        return 0.0
    return total_rating(movies) / len(movies)


def add_movie(movies, movie):
    """Immutable: gibt ein neues Tuple zurueck."""
    return movies + (movie,)


def rate_movie(movie, rating):
    """Immutable: gibt einen neuen Film mit neuer Bewertung zurueck."""
    return replace(movie, rating=rating)


def top_movies(movies, n):
    """Die n besten Filme, deklarativ."""
    return tuple(sorted(movies, key=lambda m: m.rating, reverse=True)[:n])


def genre_stats(movies):
    """Anzahl und Durchschnitt pro Genre (Aggregation mit reduce)."""
    def add(acc, m):
        count, total = acc.get(m.genre, (0, 0.0))
        return {**acc, m.genre: (count + 1, total + m.rating)}
    grouped = reduce(add, movies, {})
    return {g: {"count": c, "average": round(t / c, 2)}
            for g, (c, t) in sorted(grouped.items())}


def base_score(movie):
    """Basis-Score = Bewertung."""
    return movie.rating


def recency_bonus(movie, today_year):
    """Bonus fuer neuere Filme: 0.02 pro Jahr seit 1990, nie negativ."""
    return max(0.0, (movie.year - 1990) * 0.02) if movie.year <= today_year else 0.0


def final_score(movie, today_year):
    """Gesamt-Score."""
    return round(base_score(movie) + recency_bonus(movie, today_year), 3)


def rank_movies(movies, today_year):
    """Rangliste nach final_score, bei Gleichstand nach Titel."""
    return tuple(sorted(movies, key=lambda m: (-final_score(m, today_year), m.title)))
```

Routen in `app.py` bleiben dünn, z.B.:

```python
@app.route("/movies/top")
def get_top():
    """Die n besten Filme."""
    n = request.args.get("n", default=5, type=int)
    return jsonify([asdict(m) for m in top_movies(load_movies(), n)])
```

---

## 7. Material pro Feld (Format für `docs/portfolio_material.md`)

Für jedes Feld genau diesen Block ausfüllen:

```
### <Feld>  (<Niveau>, Mindestzeichen: ...)
- Feature im Projekt:
- Fundort: Datei, Funktion, Zeilen
- Pflicht-Artefakt laut Moodle: ...
- Codeauszug (5 bis 25 Zeilen):
- Testfälle (Input -> erwarteter Output), mind. 2:
- Git: Commit-Hashes (Vorher/Nachher), falls gefragt
- Leitfragen für meinen Text:
- Typische Fallen für dieses Feld:
```

### Die 15 Felder im Detail

| Feld | Feature / Schritt | Pflicht-Artefakt (Moodle) | Was der Text zeigen muss |
|---|---|---|---|
| **A1B** | Schritt 3 | Eine Prozedur und eine pure function aus dem Projekt nebeneinander | Begriffe korrekt (pure, Seiteneffekt, referentielle Transparenz), Bezug zum Projekt, Vergleich zu OO und prozedural |
| **A1I** | Schritt 5 | Ein Codebeispiel mit Mutation und die immutable Variante davon | Was ändert sich im Zustand, was bleibt gleich, warum ist es sicherer, Test dazu |
| **A1A** | Schritt 11 | Dieselbe Aufgabe in OO, prozedural und funktional, mit Bewertung | **Vergleich** nach Kriterien (Lesbarkeit, Testbarkeit, Fehleranfälligkeit, Länge), **begründete Entscheidung** |
| **B1B** | Schritt 12 | Die Elemente des Functional Design im Projekt benannt, je mit Fundort | immutable Datentypen, Constructors, composable Operators mit Datei und Funktion |
| **B1I** | Schritt 7 | Ein Design-Blatt: deklarative Anforderungen, Datenfluss, geplante Operatoren | Entwurf **vor** der Umsetzung, Datenfluss nachvollziehbar, Vergleich Soll und Ist |
| **B1A** | Schritt 6 | Eine imperative Route deklarativ umgesetzt, Vor- und Nachteile begründet | Beide Varianten nebeneinander, gleiche Tests grün, **Vor- und Nachteile**, Entscheidung |
| **C1B** | Schritt 8 | Ein Algorithmus des Projekts mit Beispieldurchlauf Input → Output | Schrittweise von Hand durchgerechnet (Tabelle), Ergebnis stimmt mit Test überein |
| **C1I** | Schritt 8 | Derselbe Algorithmus in Teilfunktionen zerlegt, mit Signaturen | Signaturen mit Typen, warum diese Zerlegung, was jede Teilfunktion tut |
| **C1A** | Schritt 8 | Komposition zu einem Ablauf, mit Testfällen inkl. Edge Case | Ablauf `rank_movies` aus den Teilen, Korrektheit und Lesbarkeit geprüft, Edge Cases |
| **C2B** | Schritt 4 | Funktion in einer Variable gespeichert, Map/Filter/Reduce je einzeln | Je ein kleines Beispiel für Variable, map, filter, reduce, mit Ausgabe |
| **C2I** | Schritt 9 | Lambda-Ausdruck und verkettetes Map/Filter/Reduce, **anderes Feature** | Warum Lambda hier lesbar ist (oder wann benannte Funktion besser wäre), Verkettung erklärt |
| **C2A** | Schritt 10 | Aggregation oder benutzerdefinierte Sortierung, **drittes Feature** | Aggregation oder Sortierung mit `key`, Alternative (groupby, defaultdict) verglichen |
| **D1B** | Schritt 14 | Drei Refactoring-Techniken und zwei Performance-Massnahmen, je mit Zweck | Jede Technik benannt, Zweck, kurzes Beispiel; Performance-Massnahmen mit Zweck |
| **D1I** | Schritt 14 | Vorher/Nachher aus der Commit-Historie, gleiches Verhalten per Test belegt | Zwei echte Commits, Diff, Test grün vor und nach dem Refactoring |
| **D1A** | Schritt 15 | Messung vorher/nachher und Begründung der gewählten Datenstruktur | Echte Zahlen, Interpretation, Begründung, Grenzen der Messung |

Wichtig bei C2: B, I und A müssen **an drei verschiedenen Features** gezeigt werden und dürfen **nicht** dieselben Codeauszüge enthalten.
Vorgesehen: C2B = Suche/Basis (Schritt 4), C2I = Empfehlung (Schritt 9), C2A = Genre-Statistik (Schritt 10).

### Leitfragen, die Claude Code mir pro Feld stellen soll (ich antworte in eigenen Worten)

- Was ist das Konzept, in einem Satz, ohne Definition abzuschreiben?
- Wo steckt es in meinem Projekt (Datei, Funktion)? Zeig mir die Zeile.
- Warum habe ich es so gelöst? Welche Alternative gab es? Warum nicht diese?
- Welches Problem gab es beim Bauen? Wie habe ich es gelöst?
- Welche 2 Testfälle belegen, dass es stimmt? Was passiert im Edge Case?
- Was würde ich beim nächsten Mal anders machen? Wo könnte ich es in einem anderen Projekt wieder einsetzen?
- Nur bei A: Welche zwei Varianten vergleiche ich? Nach welchen Kriterien? Was ist mein Urteil und warum?

---

## 8. Hilfsskript `count_chars.py` (Zeichen im Textteil zählen)

Moodle zählt **Zeichen ohne Leerzeichen**, der Code zählt **nicht**. Dieses Skript entfernt Codeblöcke und zählt den Rest:

```python
"""Zaehlt Zeichen ohne Leerzeichen in einer Markdown-Datei, ohne Codebloecke."""
import re
import sys


def count_chars(path):
    """Gibt die Zeichenzahl des Textteils ohne Code und ohne Leerzeichen zurueck."""
    with open(path, encoding="utf-8") as file:
        text = file.read()
    text = re.sub(r"```.*?```", "", text, flags=re.S)
    return len(re.sub(r"\s", "", text))


if __name__ == "__main__":
    for name in sys.argv[1:]:
        print(f"{name}: {count_chars(name)} Zeichen")
```

Aufruf: `python count_chars.py portfolio/A1B.md portfolio/A1I.md`.
Ziel: **mindestens 10 % über dem Minimum** (B ab 660, I ab 1100, A ab 1550), damit eine andere Zählweise nichts kippt.

---

## 9. Vorlage für jeden Lernnachweis (ich fülle sie selbst aus, eine Datei pro Feld in `portfolio/`)

```markdown
# Kompetenzfeld: <z.B. C2I>

**Feature im Flask-Projekt:** <z.B. Empfehlung (/movies/recommend)>

## Kontext und Ziel
Was soll das Feature lösen? Welche Inputs und Outputs gibt es?

## Konzept in eigenen Worten
(Nicht nur die Definition. Erkläre, wie du es einem Mitschüler erklären würdest.)

## Umsetzung im Projekt
Vorgehen, Entscheidungen, Alternativen. Warum diese Lösung?

## Code-Beispiel und Einordnung
<Codeblock aus der App>
2 bis 5 Sätze: Was genau an diesem Code zeigt die Kompetenz? Wo liegt er im Projekt?

## Pflicht-Artefakt
<laut Tabelle: z.B. Vorher/Nachher, Design-Blatt, Vergleich>

## Test und Überprüfung
- Test 1: Input -> erwarteter Output (-> tatsächlich)
- Test 2 (Edge Case): ...

## Reflexion und Transfer
Was war schwierig? Was habe ich gelernt? Was würde ich nächstes Mal besser machen? Wo kann ich es wiederverwenden?
```

---

## 10. Review durch Claude Code (vor jeder Abgabe, pro Feld)

Prüfe meinen Text und antworte mit dieser Tabelle (✅ / ❌ und ein Satz):

| Prüfpunkt | Ergebnis |
|---|---|
| Zeichenzahl (ohne Code, ohne Leerzeichen) erreicht? (Zahl nennen) | |
| Code stammt aus der Flask-App? Fundort korrekt? Läuft er? | |
| Pflicht-Artefakt vollständig? | |
| Mindestens 2 Testfälle, Werte stimmen mit dem echten Code überein? | |
| Bezug zur Kompetenz klar (was genau belegt sie)? | |
| Niveau-Verb getroffen (bei A: zwei Varianten verglichen und entschieden)? | |
| Begründete Entscheidung und Alternative genannt? | |
| Reflexion und Transfer vorhanden und konkret (kein Fülltext)? | |
| Fachliche Fehler? (konkret zitieren und korrigieren) | |
| Bei C2: anderes Feature als bei den anderen C2-Feldern? | |

Dann: die **drei wichtigsten Verbesserungen**, ohne den Text für mich neu zu schreiben.
Ich überarbeite selbst und schicke es nochmals.

---

## 11. Zeitplan (Stand: Mittwoch 04.11.2026; Abgabe laut Stundenplan Freitag 06.11.)

Das ist sehr knapp. Priorität: erst alles, was **Punkte pro Stunde** bringt.

| Wann | Was |
|---|---|
| **Mi 04.11. (heute)** | Schritt 0 bis 6: App-Grundlage, A1B, C2B, A1I, B1A, Tests. Danach die Texte A1B, C2B (B-Felder zuerst). |
| **Do 05.11.** | Schritt 7 bis 12 (B1I, C1, C2I, C2A, A1A, B1B), Schritt 14 und 15 (D1). Texte B-Felder fertig, I-Felder beginnen. |
| **Fr 06.11.** | Texte I- und A-Felder fertig. Review (Teil 10). Schritt 17 (ZIP) und Upload in Moodle. |

Wenn die Zeit nicht reicht, **in dieser Reihenfolge** abgeben (so sichere ich die meisten Punkte):
1. Praxisprojekt, 2. alle B-Felder, 3. alle I-Felder, 4. alle A-Felder.
Sag mir **sofort**, wenn du merkst, dass ein Schritt länger dauert, und schlage vor, was ich zuerst abgebe.

Vor dem Upload klären wir: Format (PDF, Word, Link), Dateigrösse, ob die 30.10.-Frist noch gilt. Ich gebe dir dafür den Text der Moodle-Aufgabe.

---

## 12. Regeln und Fallen (immer beachten)

- Nie mehr als **eine** Route oder Funktion pro Schritt. Immer kurz sagen, warum.
- **Nicht** alles auf einmal umschreiben. Bestehenden Code nicht ohne Grund ändern.
- Jede Funktion mit Docstring, Zeilen unter 120 Zeichen, kein Trailing Whitespace, Datei endet mit Zeilenumbruch.
- Keine globalen Variablen für Daten (ausser dem bewusst gezeigten Mutationsbeispiel in A1I).
- `datetime.now()` nie in pure Funktionen. Das Jahr kommt als Parameter.
- Keine `print`-Debug-Ausgaben im fertigen Code (ausser in der bewusst gezeigten Prozedur aus A1B).
- Marker `# A1B`, `# C2I` usw. im Code lassen, damit ich die Stellen finde.
- Jeder Codeauszug im Portfolio muss **im Projekt wirklich so stehen** (Fundort angeben).
- Nach jedem Schritt: `pytest` und `pylint` ausführen, Ergebnis kurz melden.
- Wenn etwas unklar ist oder du etwas nicht weisst, frage mich oder sage es klar. Rate nicht.
- Bei Fehlern in der Umgebung (Git Bash, PowerShell, venv): Git Bash: `source .venv/Scripts/activate`, PowerShell: `.\.venv\Scripts\Activate.ps1`.

---

## 13. Start

Beginne mit **Schritt 0** (Zustand prüfen). Gib mir danach die Tabelle "vorhanden / fehlt" und schlage vor, wie wir heute (Mittwoch 04.11.) die Schritte 1 bis 6 schaffen.
Warte auf mein "weiter".