from circuit.logic_gates.basic import nor_gate


def flip_flop(prev, set_input, reset_input):
    if set_input and reset_input:
        raise Exception(
            "Both set and reset can never both be 1. But... what would happen if this wasn't there...?")

    q = nor_gate(set_input)

    def set_side(reset_side_output):
        return nor_gate(set_input, reset_side_output)

    def reset_side(set_side_output):
        return nor_gate(set_side_output, reset_input)

    return
