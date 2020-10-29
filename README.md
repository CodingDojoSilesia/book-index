# Book Index Kata

[[_TOC_]]

## Goal

Your goal is to create an index of words in proposed format:

```
Word             Row,Col
AnotherWord      Row,Col; Row,Col
```

## Example

Following text:

```
Foo bar
bar test
```

Should produce output like this:

```
Foo     1,1
bar     1,5; 2,1
test    2,5
```

## What we have

### CLI

We have a very easy CLI for you:

```
python3 -m book_index FILE
```

or:

```
python3 -m book_index FILE --format html
```

this CLI executes `do_it(stream, format)` function from `book_index/index.py`

### Tests

we have a pytest environment (you need a [pytest installed](https://docs.pytest.org/en/stable/getting-started.html#install-pytest)):

```
python3 -m pytest
```

## How to start

You may use either `poetry` or `venv`.

### VENV

It is preinstalled with Python3.

```shell
> python3 -m venv book_index_venv
> source book_index_venv/bin/activate
> pip install -r requirements.txt
> python setup.py install
> pytest
```

### Poetry

Needs to be installed, isntructions here https://python-poetry.org/docs/#installation

Then you can
```
> poetry install
> poetry shell
> pytest
```


## Proposed steps to achieve the goal

1. Make a list of words from text
2. Make a list of tuples, which each tuple has (word, row, col)
3. Use these tuples to aggregate words with list of positions
4. Think about non-words characters, and [conjunction](https://en.wikipedia.org/wiki/Conjunction_%28grammar%29) words
5. Think about another formats like html, CSV or latex (default is a text format)
