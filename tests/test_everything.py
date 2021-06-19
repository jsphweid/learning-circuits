import pytest

from circuit.logic_gates.basic import nand_gate, and_gate, or_gate, nor_gate


@pytest.mark.parametrize('left, right, result', [
    (1, 1, False),
    (1, 0, True),
    (0, 1, True),
    (0, 0, True)])
def test_nand_gate(left, right, result):
    assert nand_gate(left, right) == result


@pytest.mark.parametrize('left, right, result', [
    (1, 1, True),
    (1, 0, False),
    (0, 1, False),
    (0, 0, False)])
def test_and_gate(left, right, result):
    assert and_gate(left, right) == result


@pytest.mark.parametrize('left, right, result', [
    (1, 1, True),
    (1, 0, True),
    (0, 1, True),
    (0, 0, False)])
def test_or_gate(left, right, result):
    assert or_gate(left, right) == result


@pytest.mark.parametrize('left, right, result', [
    (1, 1, False),
    (1, 0, False),
    (0, 1, False),
    (0, 0, True)])
def test_nor_gate(left, right, result):
    assert nor_gate(left, right) == result
