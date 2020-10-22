import re
from io import TextIOBase
from collections import defaultdict

RE_WORD = re.compile(r"\w+")


def do_it(stream: TextIOBase, format: str = 'text'):
    index = create_index(stream)
    print_index(index)


def create_index(stream: TextIOBase):
    index = defaultdict(list)
    for row, line in enumerate(stream, start=1):
        line_index = create_index_from_line(line.strip())
        for word, col in line_index.items():
            index[word].append((row, col))

    return index


def create_index_from_line(line: str):
    return {
        match.group(0).lower(): match.start() + 1
        for match in RE_WORD.finditer(line)
    }


def print_index(index):
    sort_indexes = list(index.items())
    sort_indexes.sort(key=lambda o: o[0])
    for word, positions in sort_indexes:
        print(
            f'{word.capitalize():<40}',
            '; '.join(f'{row:>3},{col:>2}' for row, col in positions),
        )
