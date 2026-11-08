# Kompetenzfeld: A1A

**Feature im Flask-Projekt:** Durchschnittsbewertung pro Genre in drei Stilen (`variants.py`)

## Kontext und Ziel
Ich wollte für jedes Genre den Durchschnitt der Bewertungen ausrechnen, damit man einen besseren Überblick hat. Bei Sci-Fi kommt zum Beispiel 8.53 heraus. Die gleiche Aufgabe habe ich dreimal programmiert: prozedural, objektorientiert (OO) und funktional.

## Konzept in eigenen Worten
- Prozedural: Ich sage dem Computer Schritt für Schritt, was er tun soll, mit Schleifen und Hilfsvariablen.
- OO: Daten und Verhalten sind zusammen in einem Objekt, das einen Zustand hat und sich mit Methoden verändert.
- Funktional: Ich beschreibe das Resultat mit Funktionen, die nichts verändern.

## Umsetzung im Projekt
In der prozeduralen Version habe ich zwei dicts, eines für die Summe und eines für die Anzahl. In der OO-Version gibt es die Klasse `MovieStats`. Mit `add` kommt ein Film dazu und `averages` rechnet am Ende den Durchschnitt aus. In der funktionalen Version benutze ich `reduce`. Dort wird für jeden Film ein neues dict gemacht und das alte bleibt gleich.

## Code-Beispiel und Einordnung
```python
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
```
```python
# A1A: funktional (reduce und Comprehension, keine Mutation)
def average_per_genre_functional(movies):
    """Durchschnitt pro Genre mit reduce, ohne Mutation."""
    def step(acc, movie):
        count, total = acc.get(movie.genre, (0, 0.0))
        return {**acc, movie.genre: (count + 1, total + movie.rating)}
    grouped = reduce(step, movies, {})
    return {genre: round(total / count, 2) for genre, (count, total) in sorted(grouped.items())}
```
Beide sind in `variants.py` (Zeilen 5–19 und 47–54), die Klasse `MovieStats` ist in den Zeilen 23–44. Alle drei geben das gleiche Resultat, das prüft ein Test.

## Pflicht-Artefakt
Die gleiche Aufgabe in drei Stilen, mit Bewertung:

- Prozedural: 13 Zeilen. Gut zu lesen und zu testen. Man muss aber aufpassen, dass die zwei dicts immer zusammenpassen.
- OO: 13 Zeilen. Der Name der Klasse sagt gut, was passiert. Weil das Objekt einen Zustand hat, ist das Testen etwas mühsamer.
- Funktional: 6 Zeilen. Keine Mutation und am einfachsten zu testen. Man muss aber wissen, wie `reduce` funktioniert.

## Test und Überprüfung
- Test 1: alle drei mit `load_movies()` -> gleiches dict, z.B. Sci-Fi 8.53 (-> grün)
- Test 2 (Edge Case): alle drei mit leerem Tuple -> `{}` (-> grün)

## Bewertung und Entscheidung
Ich nehme die funktionale Version. Sie ist am kürzesten, ändert nichts und passt zum restlichen Code in `movies.py`. Bei sehr vielen Filmen würde ich aber die prozedurale nehmen. Die funktionale kopiert bei jedem Film das dict und wird dadurch langsamer. OO würde ich nur nehmen, wenn die Statistik länger bestehen und immer wieder neue Filme bekommen soll.

## Reflexion und Transfer
Am meisten Zeit hat gebraucht, dass alle drei genau gleich runden und sortieren, sonst wäre der Test rot. Ich habe gemerkt, dass es nicht einfach einen besten Stil gibt, es kommt auf die Aufgabe an. Beim nächsten Mal würde ich auch messen, wie schnell die drei sind.
