import pytest

from fun.adder import add_two_binary_numbers_of_equal_size


@pytest.mark.parametrize('left, right, result', [
    ("1011", "0110", "10001"),
    ("1011", "1111", "11010"),
    ("1", "0", "1"),
    ("0", "1", "1"),
	("10010110", "11101110", "110000100"),
	("1", "101", "110"),
	("100100", "1111", "110011"),
	(2, 3, bin(5)[2:]),
	(30, 20, bin(50)[2:]),
	(333, 222, bin(555)[2:])])
def test_adding_two_same_length_binary_numbers(left, right, result):
    assert add_two_binary_numbers_of_equal_size(left, right) == result