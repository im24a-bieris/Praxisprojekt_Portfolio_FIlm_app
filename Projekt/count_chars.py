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
