from circuit.flip_flop import flip_flop


def test_or_gate():
    # reset state of flip_flop, initial state should be off
    q = flip_flop(None, 0, 1)
    assert not q

    # calling set should flip it to on
    q = flip_flop(q, 1, 0)
    assert q

    # should still be turned on
    q = flip_flop(q, 0, 0)
    assert q

    # but resetting it should turn it off
    q = flip_flop(q, 0, 1)
    assert not q
