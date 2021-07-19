import pytest

from n2t.compiler import get_tokens_as_xml, compile_as_xml

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
def test_it_compiles_correct_xml_for_tokens(base_folder):
    with open(f"n2t/{base_folder}.jack") as f:
        jack_file = f.read()

    with open(f"n2t/{base_folder}T.xml") as f:
        token_xml_file = f.read()

    assert get_tokens_as_xml(jack_file) == token_xml_file


# TODO: temp, obviously...
@pytest.mark.parametrize("base_folder",
                         [f for f in base_folders if ("ExpressionLessSquare" in f) or ("ArrayTest" in f)])
def test_it_compiles_correct_xml(base_folder):
    with open(f"n2t/{base_folder}.jack") as f:
        jack_file = f.read()

    with open(f"n2t/{base_folder}.xml") as f:
        token_xml_file = f.read()

    assert compile_as_xml(jack_file) == token_xml_file
