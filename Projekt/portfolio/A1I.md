# Kompetenzfeld: A1I

**Feature im Flask-Projekt:** Film hinzufügen (`POST /movies`)

## Kontext und Ziel
Mit `POST /movies` kann man einen neuen Film hinzufügen. Die Frage war: Ändere ich die alte Filmliste, oder mache ich eine neue?

## Konzept in eigenen Worten
Mutation heisst: Man ändert etwas, das schon existiert, zum Beispiel eine Liste mit `append`. Alle, die diese Liste benutzen, sehen die Änderung plötzlich auch. Immutable heisst: Man ändert das Alte nie. Man macht stattdessen etwas Neues mit der Änderung.

## Umsetzung im Projekt
Zuerst habe ich `add_movie_mutating` gebaut. Sie hängt den Film an die Liste an. Danach habe ich `add_movie` gebaut. Sie gibt ein neues Tuple zurück, das alte bleibt gleich. Die Route benutzt `add_movie` und speichert das neue Tuple in `app.config["MOVIES"]`. Das ist wichtig, weil `load_movies` einen Cache hat. Mit Mutation würde ich aus Versehen auch den Cache ändern. Bei einer doppelten Id gibt `add_movie` einen Fehler (`ValueError`).

## Code-Beispiel und Einordnung
```python
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
```
Beide stehen in `movies.py` (Zeilen 123–134). Bei der ersten wird die Liste verändert. Bei der zweiten entsteht ein neues Tuple.

## Pflicht-Artefakt
Mutation und immutable Variante nebeneinander (oben). Nach `add_movie_mutating` hat die Liste 13 Filme, das Original ist also verändert. Nach `add_movie` hat das Original weiter 12 Filme.

## Test und Überprüfung
- Test 1: `add_movie_mutating(liste, dune)` -> Liste hat danach 13 Filme (-> grün)
- Test 2: `add_movie(MOVIES, dune)` -> neues Tuple mit 13, `MOVIES` hat weiter 12 (-> grün)
- Test 3 (Edge Case): `add_movie` mit Id 1 -> `ValueError` (-> grün)

## Reflexion und Transfer
Zuerst dachte ich, unveränderliche Daten sind zu kompliziert. Beim Cache habe ich gemerkt, dass Mutation gefährlich ist: Der Fehler würde erst beim nächsten Request auffallen. Es ist besser, neue Werte zurückzugeben, als alte zu überschreiben. Das kann ich auch in anderen Projekten brauchen, zum Beispiel bei einem Warenkorb.
