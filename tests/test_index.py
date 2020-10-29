from io import StringIO

from book_index.index import do_it, create_index, print_text_index
from unittest.mock import patch


def test_create_index_one_line():
    stream = StringIO("foo bar\n")
    assert create_index(stream) == {
        "foo": [(1, 1)],
        "bar": [(1, 5)],
    }


def test_create_index_one_line_repeated_words():
    stream = StringIO("foo bar bar\n")
    assert create_index(stream) == {
        "foo": [(1, 1)],
        "bar": [(1, 5), (1, 9)],
    }


def test_create_index_two_lines():
    stream = StringIO("foo bar\nbar foo\n")
    assert create_index(stream) == {
        "foo": [(1, 1), (2, 5)],
        "bar": [(1, 5), (2, 1)],
    }


def test_create_index_two_lines_insensitive():
    stream = StringIO("Foo bAr\nbaR fOo\n")
    assert create_index(stream) == {
        "foo": [(1, 1), (2, 5)],
        "bar": [(1, 5), (2, 1)],
    }


def test_create_index_special_characters():
    stream = StringIO("Foo-bar. Lorem, ipsum\n")
    assert create_index(stream) == {
        "foo": [(1, 1)],
        "bar": [(1, 5)],
        "lorem": [(1, 10)],
        "ipsum": [(1, 17)],
    }


def test_print_index():
    index = {
        "foo": [(1, 1)],
    }

    with patch('sys.stdout', new=StringIO()) as stdout:
        print_text_index(index)

    assert stdout.getvalue() == (
        "Foo                                        1, 1\n"
    )


def test_print_index_two_positions():
    index = {
        "foo": [(1, 1), (1, 5)],
    }

    with patch('sys.stdout', new=StringIO()) as stdout:
        print_text_index(index)

    assert stdout.getvalue() == (
        "Foo                                        1, 1;   1, 5\n"
    )


def test_print_index_two_words():
    index = {
        "foo": [(1, 1)],
        "bar": [(1, 5)],
    }

    with patch("sys.stdout", new=StringIO()) as stdout:
        print_text_index(index)

    assert stdout.getvalue() == (
        "Bar                                        1, 5\n"
        "Foo                                        1, 1\n"
    )


def test_do_it():
    stream = StringIO("foo bar\n")

    with patch("sys.stdout", new=StringIO()) as stdout:
        do_it(stream, format='text')

    assert stdout.getvalue() == (
        "Bar                                        1, 5\n"
        "Foo                                        1, 1\n"
    )
