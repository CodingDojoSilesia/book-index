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
    print("<style>table, th, td")
    print("{ border: 1px solid black; border-collapse: collapse; }")
    print("</style>")
    print("<table>")
    print("<tr><th>Word</th><th>Positions</th></tr>")
    for word, positions in _sort_and_yield_index(index):
        print("<tr>")
        print(f"<th>{escape(word.capitalize())}</th>")
        for row, col in positions:
            print(f"<td>{row}, {col}</td>")
        print("</tr>")
    print("</table>")


def _sort_and_yield_index(index: INDEX_TYPE):
    sort_indexes = list(index.items())
    sort_indexes.sort(key=lambda o: o[0])
    for word, positions in sort_indexes:
        yield word, positions


FORMATS = {
    "text": print_text_index,
    "html": print_html_index,
}
