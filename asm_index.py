class Node:
    def __init__(self, data, parent=None, children=[]):
        self.data = data
        self.parent = parent
        self.children = children

    def __repr__(self):
        return f"{self.data}"


def str_atomize(s: str) -> list[str]:
    """atomize: break a string into its atoms, for us this means characters (bytes)
    for more complicated objects, will need more complicated atomize functions
    """
    return [c for c in s]


def str_asm_combos(a: str, others: list[str]) -> list[str]:
    """str_asm_combos: possible left and right side concatenations of string assembly"""
    return list(set([a + o for o in others] + [o + a for o in others]))


def possible_children(node: Node, pool: list[str]) -> list[Node]:
    """possible_children: given a node, return all possible children"""
    return [Node(data=p, parent=node) for p in str_asm_combos(node.data, pool)]


def str_asm_index(s: str) -> int:
    """a_i: assembly index with smallest assembly path

    Returns:
        int: the asm index of the string
    """
    atoms = str_atomize(s)

    # can't assemble nothing or a single atom (one atom is already assembled)
    if len(atoms) <= 1:
        return 0
    # two objects can be assembled in one step
    elif len(atoms) == 2:
        return 1
    # three objects can be assembled in two step
    elif len(atoms) == 3:
        return 2

    # but anything over three is not clear what the assembly index is
    # so we have to combinatorially try stuff
    pool = [] + atoms
    root = Node(data=atoms[0])
    potentials = possible_children(root, pool)
    print(potentials)

    return float("inf")


if __name__ == "__main__":
    s1 = "A"
    s2 = "AB"
    s3 = "ABAB"
    s4 = "ABRACADABRA"

    assert str_asm_index(s1) == 0
    print("PASSED TEST 1")

    assert str_asm_index(s2) == 1
    print("PASSED TEST 2")

    assert str_asm_index(s3) == 2
    print("PASSED TEST 3")

    assert str_asm_index(s4) == 7
    print("PASSED TEST 4")
