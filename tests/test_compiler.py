import pytest

from n2t.compiler import tokenize, tokens_to_xml

base_folders = [
    "10_tests/ArrayTest/Main",
    "10_tests/ExpressionLessSquare/Main",
    "10_tests/ExpressionLessSquare/Square",
    "10_tests/ExpressionLessSquare/SquareGame",
    "10_tests/Square/Main",
    "10_tests/Square/Square",
    "10_tests/Square/SquareGame",
]


@pytest.mark.parametrize("base_folder", base_folders)
def test_it_compiles_correct_xml(base_folder):
    with open(f"n2t/{base_folder}.jack") as f:
        jack_file = f.read()

    with open(f"n2t/{base_folder}T.xml") as f:
        token_xml_file = f.read()

    tokens = tokenize(jack_file)
    assert tokens_to_xml(tokens) == token_xml_file
