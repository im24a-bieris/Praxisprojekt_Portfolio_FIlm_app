# Kompetenzfeld: A1I

**Feature im Flask-Projekt:** Film hinzufügen (`POST /movies`)

## Kontext und Ziel
Mit `POST /movies` kann man einen Film hinzufügen. Ich musste entscheiden, ob ich die bestehende Filmliste ändere oder eine neue mache.

## Konzept in eigenen Worten
Bei Mutation wird etwas verändert, das schon existiert, z.B. eine Liste mit `append`. Das Problem ist, dass alle anderen Stellen, die die gleiche Liste benutzen, die Änderung auch sehen. Bei immutable ändert man das Alte nie, sondern macht eine neue Version.

## Umsetzung im Projekt
Zuerst habe ich `add_movie_mutating` geschrieben, die den Film einfach mit `append` anhängt. Danach kam `add_movie`, die ein neues Tuple zurückgibt. Die Route benutzt `add_movie` und speichert das neue Tuple in `app.config["MOVIES"]`. Das ist hier wichtig, weil `load_movies` gecacht ist und immer das gleiche Objekt zurückgibt. Wäre das eine Liste und ich würde sie mit `append` ändern, wäre der Cache auch verändert. Wenn eine Id schon existiert, gibt `add_movie` einen `ValueError`.

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
Beide sind in `movies.py` (Zeilen 123–134). Bei der ersten wird die Liste selbst verändert. Bei der zweiten gibt es ein neues Tuple und das alte bleibt.

## Pflicht-Artefakt
Mutation und immutable Variante nebeneinander (oben). Nach `add_movie_mutating` hat die Liste 13 Filme, das Original ist also verändert. Nach `add_movie` hat das Original weiter 12 Filme.

## Test und Überprüfung
- Test 1: `add_movie_mutating(liste, dune)` -> Liste hat danach 13 Filme (-> grün)
- Test 2: `add_movie(MOVIES, dune)` -> neues Tuple mit 13, `MOVIES` hat weiter 12 (-> grün)
- Test 3 (Edge Case): `add_movie` mit Id 1 -> `ValueError` (-> grün)

## Reflexion und Transfer
Zuerst dachte ich, unveränderliche Daten sind zu kompliziert. Beim Cache habe ich gemerkt, dass Datenänderungen nicht so optimal sind, weil so ein Fehler erst beim nächsten Request auffallen würde. Es ist besser, neue Werte zurückzugeben, als alte zu überschreiben. Das mache ich in Zukunft auch in anderen Projekten so.
