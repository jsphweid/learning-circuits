import pytest

from fun.bin_to_dec import bin_to_dec

@pytest.mark.parametrize('bin, dec', [
    ("1011", 11),
    ("1", 1),
    ("0", 0),
    ("10010110", 150),
    ("100100", 36)])
def test_adding_two_same_length_binary_numbers(bin, dec):
    assert bin_to_dec(bin) == dec