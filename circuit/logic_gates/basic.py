def nand_gate(left, right):
    return not (left and right)


def and_gate(left, right):
    return nand_gate(nand_gate(left, right), nand_gate(left, right))


def or_gate(left, right):
    return nand_gate(nand_gate(left, left), nand_gate(right, right))


def nor_gate(left, right):
    return not or_gate(left, right)
