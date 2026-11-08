# Kompetenzfeld: D1I

**Feature im Flask-Projekt:** Highlights (`/movies/highlights`)

## Kontext und Ziel
Die Route zeigt gute Filme (ab 8.5, ab 1990) als Text wie "INCEPTION (Sci-Fi)", der älteste zuerst. Die erste Version `process` hat funktioniert, war aber schwer zu lesen. Ich habe sie in drei Schritten aufgeräumt. Jeder Schritt ist ein eigener Commit.

## Konzept in eigenen Worten
Beim Refactoring ändere ich, wie der Code aussieht, aber nicht, was er macht. Das beweise ich mit einem Test. Er muss vor und nach dem Umbau grün sein. In Git sieht man dann genau, was sich geändert hat.

## Umsetzung im Projekt
Zuerst habe ich einen Test für die alte Funktion geschrieben. Dann habe ich in kleinen Schritten umgebaut: Funktionen herausziehen, bessere Namen geben, Schleifen ersetzen. Nach jedem Schritt habe ich `pytest` laufen lassen und committet. Wenn ein Test rot geworden wäre, hätte ich genau gewusst, welcher Schritt schuld ist.

Commits:
- Vorher (`process`): `47791a6`
- Extract Function: `ec4bb36`
- Rename: `5a1bcef`
- Nachher (Pipeline): `85c0c6d`

Den ganzen Unterschied sieht man mit `git diff 47791a6 85c0c6d -- Projekt/movies.py`.

## Code-Beispiel und Einordnung
Vorher (Commit `47791a6`):
```python
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
Nachher:
```python
def highlights(movies: Movies) -> tuple[str, ...]:
    """Highlights als Text, aelteste zuerst."""
    return tuple(map(highlight_label, sorted(filter(is_highlight, movies), key=year_of)))
```
Die neue Funktion steht in `movies.py` (Zeilen 235–237). Die zwei `if` sind jetzt in `is_highlight`, der Text ist in `highlight_label`.

## Pflicht-Artefakt
Vorher und nachher aus Git (Hashes oben). Der gleiche Test ist in allen Commits grün.

## Test und Überprüfung
- Test 1: `highlights(MOVIES)` -> FORREST GUMP (Drama), THE MATRIX (Sci-Fi), GLADIATOR (Action), ... (-> grün in allen Commits)
- Test 2 (Edge Case): leere Liste -> `()`, Film von 1985 -> `()` (-> grün in allen Commits)

## Reflexion und Transfer
Am schwierigsten war, wirklich nur das Aussehen zu ändern und nicht aus Versehen auch das Resultat. Kleine Schritte haben dabei geholfen. So kann ich auch alten Code in anderen Projekten sicher aufräumen.
