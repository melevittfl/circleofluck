import pytest
from circleofluck import *
from io import StringIO


def test_fill_letters():
    word = list("test")
    guess = "t"
    state = list("****")
    result = list("t**t")
    assert fill_letters(word, guess, state) == result
    state = result
    guess = "e"
    result = list("te*t")
    assert fill_letters(word, guess, state) == result


def test_guess_in_word():
    word = list("test")
    guess = "t"
    assert guess_in_word(word, guess)
    guess = "x"
    assert not guess_in_word(word, guess)


def test_get_word(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO("scooby"))
    assert get_word() == "scooby"


def test_get_guess(monkeypatch):
    monkeypatch.setattr('sys.stdin', StringIO("m"))
    assert get_guess() == "m"


def test_hangman():
    h = CircleOfLuck("test test")
    assert h.state == ['*', '*', '*', '*', '_', '*', '*', '*', '*']
    # assert h.guesses == []

    # Test making a correct guess
    h.state = "t"
    assert h.state == ['t', '*', '*', 't', '_', 't', '*', '*', 't']
    # assert h.guesses == ['t']

    # Test making an incorrect guess
    h.state = "a"
    assert h.state == ['t', '*', '*', 't', '_', 't', '*', '*', 't']
    # assert h.guesses == ['ta']

