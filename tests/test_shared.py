import pytest

from n2t.shared import BaseParser, WhiteSpaceStrategy


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
def test_line_cleanser_works_with_eliminate_all_whitespace_strategy(input_str, expected_output):
    parser = BaseParser(input_str, WhiteSpaceStrategy.MAX_ONE_IN_BETWEEN_WORDS)
    assert parser.clean_line(input_str) == expected_output
