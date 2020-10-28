import re
from io import TextIOBase
from collections import defaultdict
from typing import Dict, Tuple, List
from html import escape

RE_WORD = re.compile(r"\w+")
POS_TYPE = Tuple[int, int]
INDEX_TYPE = Dict[str, List[POS_TYPE]]


def do_it(stream: TextIOBase, format: str = "text"):
    print_index = FORMATS[format]
    index = create_index(stream)
    print_index(index)


def create_index(stream: TextIOBase) -> INDEX_TYPE:
    index: INDEX_TYPE = defaultdict(list)
    for row, line in enumerate(stream, start=1):
        line_index = create_index_from_line(line.strip())
        for word, col in line_index.items():
            index[word].append((row, col))

    return index


def create_index_from_line(line: str) -> Dict[str, int]:
    return {
        match.group(0).lower(): match.start() + 1 for match in RE_WORD.finditer(line)
    }


def print_text_index(index: INDEX_TYPE):
    for word, positions in _sort_and_yield_index(index):
        print(
            f"{word.capitalize():<40}",
            "; ".join(f"{row:>3},{col:>2}" for row, col in positions),
        )


def print_html_index(index: INDEX_TYPE):
    # IS NOT A GOOD EXAMPLE!
    # FOR HTML YOU SHOULD USE TEMPLATE ENGINE
    # LIKE JINJA2!
    print("<style>")
    print("div { margin: auto; }")
    print("dt { font-weight: bold; }")
    print("span { width: 20px; }")
    print("</style>")
    print("<div>")
    print("<h1>INDEX</h2>")

    print("<dl>")
    for word, positions in _sort_and_yield_index(index):
        print(f"<dt>{escape(word.capitalize())}</dt>")
        print("<dd><ul>")
        for row, col in positions:
            print(f"<li><span>{row}</span>, <span>{col}</span></li>")
        print("</ul></dd>")
    print("</dl>")
    print("</div>")


def _sort_and_yield_index(index: INDEX_TYPE):
    sort_indexes = list(index.items())
    sort_indexes.sort(key=lambda o: o[0])
    for word, positions in sort_indexes:
        yield word, positions


FORMATS = {
    "text": print_text_index,
    "html": print_html_index,
}
