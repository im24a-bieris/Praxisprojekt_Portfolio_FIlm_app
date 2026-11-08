# Kompetenzfeld: A1A

**Feature im Flask-Projekt:** Durchschnittsbewertung pro Genre in drei Stilen (`variants.py`)

## Kontext und Ziel
Ich wollte für jedes Genre den Durchschnitt der Bewertungen berechnen. Das Resultat ist zum Beispiel `{"Action": 8.3, "Drama": 8.37, "Sci-Fi": 8.53}`. Ich habe die gleiche Aufgabe dreimal gelöst, um die Stile zu vergleichen.

## Konzept in eigenen Worten
- Prozedural: Ich sage dem Computer Schritt für Schritt, was er tun soll, mit Schleifen und Hilfsvariablen.
- Objektorientiert (OO): Daten und Funktionen sind zusammen in einem Objekt. Das Objekt hat einen Zustand, der sich ändert.
- Funktional: Ich verbinde Funktionen, die nichts verändern, sondern immer etwas Neues zurückgeben.

## Umsetzung im Projekt
Prozedural benutze ich zwei dicts (`totals`, `counts`) und eine Schleife. In OO sammelt die Klasse `MovieStats` die Bewertungen, `add` ändert den Zustand und `averages` rechnet. Funktional baue ich mit `reduce` für jeden Film ein neues dict, ohne etwas zu verändern.

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
Beide stehen in `variants.py` (Zeilen 5–19 und 47–54), die Klasse `MovieStats` in Zeilen 23–44. Alle drei geben genau das gleiche Resultat, darum ist der Vergleich fair.

## Pflicht-Artefakt
Die gleiche Aufgabe in drei Stilen, mit Bewertung:

- Prozedural: 13 Zeilen, sehr einfach zu lesen und gut testbar. Aber die zwei dicts müssen immer zusammenpassen.
- OO: 13 Zeilen, der Name der Klasse hilft beim Lesen. Aber der Zustand kann sich ändern, das macht das Testen schwerer.
- Funktional: 6 Zeilen, sehr gut testbar und ohne Mutation. Aber man muss `reduce` kennen.

## Test und Überprüfung
- Test 1: alle drei mit `load_movies()` -> gleiches dict, z.B. Sci-Fi 8.53 (-> grün)
- Test 2 (Edge Case): alle drei mit leerem Tuple -> `{}` (-> grün)

## Bewertung und Entscheidung
Ich nehme die funktionale Variante. Sie ist am kürzesten, verändert nichts und ist leicht zu testen. Sie passt auch zum Rest von `movies.py`. Die prozedurale Variante ist am einfachsten zu lesen und bei sehr vielen Filmen schneller, weil die funktionale das dict bei jedem Film kopiert. OO lohnt sich erst, wenn man einen Zustand über längere Zeit braucht.

## Reflexion und Transfer
Schwierig war, dass alle drei genau gleich runden und sortieren. Gelernt habe ich, dass der beste Stil von der Aufgabe und der Datenmenge abhängt. Nächstes Mal würde ich die Geschwindigkeit auch messen. Die Tabelle mit Kriterien kann ich bei anderen Entscheidungen wieder brauchen.
