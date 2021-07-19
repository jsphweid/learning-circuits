import pytest

from n2t.shared import BaseParser, WhiteSpaceStrategy


@pytest.fixture
def tokens_for_test():
    return ["zero", "one", "two"]


@pytest.fixture
def tokens_for_test_input(tokens_for_test):
    return "\n".join(tokens_for_test), WhiteSpaceStrategy.ELIMINATE_ALL


@pytest.mark.parametrize("input_str, expected_output", [
    ("test something", "testsomething"),
    ("", ""),
    ("// a comment", ""),
    ("something // then a comment", "something"),
    ("something / nop /a/ little/more//nop//", "something/nop/a/little/more")
])
def test_line_cleanser_works_with_eliminate_all_whitespace_strategy(input_str, expected_output):
    parser = BaseParser(input_str, WhiteSpaceStrategy.ELIMINATE_ALL)
    assert parser.clean_line(input_str) == expected_output


@pytest.mark.parametrize("input_str, expected_output", [
    ("test something", "test something"),
    ("", ""),
    ("// a comment", ""),
    ("something // then  a comment", "something"),
    ("test  this    simple case  ", "test this simple case")
])
def test_line_cleanser_works_with_max_one_between_whitespace_strategy(input_str, expected_output):
    parser = BaseParser(input_str, WhiteSpaceStrategy.MAX_ONE_IN_BETWEEN_WORDS)
    assert parser.clean_line(input_str) == expected_output


def test_parser_can_get_all_tokens(tokens_for_test, tokens_for_test_input):
    raw, strat = tokens_for_test_input
    parser = BaseParser(raw, strat)
    assert tokens_for_test == parser.get_all()
    assert parser.has_more()


def test_parser_can_advance_retreat(tokens_for_test, tokens_for_test_input):
    raw, strat = tokens_for_test_input
    parser = BaseParser(raw, strat)
    assert not parser.current()
    assert parser.advance() == "zero"
    assert parser.advance() == "one"
    assert parser.advance() == "two"
    assert not parser.has_more()
    assert parser.retreat() == "one"
    assert parser.retreat() == "zero"
    assert not parser.retreat()


def test_reset_parser_works(tokens_for_test, tokens_for_test_input):
    raw, strat = tokens_for_test_input
    parser = BaseParser(raw, strat)
    parser.advance()
    parser.advance()
    parser.advance()
    assert parser.current() == "two"
    parser.reset()
    assert not parser.current()
    assert parser.advance() == "zero"


def test_peak_parser_works(tokens_for_test, tokens_for_test_input):
    raw, strat = tokens_for_test_input
    parser = BaseParser(raw, strat)
    assert parser.peak() == "zero"
    parser.advance()
    assert parser.peak() == "one"
    parser.retreat()
    assert parser.peak() == "zero"

    # TODO: test when nothing left to peak...
