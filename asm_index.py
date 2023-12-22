class Node:
    def __init__(self, data, parent=None, is_atom=False):
        self.data = data
        self.parent = parent
        self.is_atom = is_atom

    def __repr__(self):
        return f"{self.data}"


def str_unique(strs: list[str]) -> list[str]:
    """unique: return a list of unique strings"""
    unique = []
    for s in strs:
        if s not in unique:
            unique.append(s)
    return unique


def str_atomize(s: str) -> list[str]:
    """atomize: break a string into its atoms, for us this means characters (bytes)
    for more complicated objects, will need more complicated atomize functions
    """
    return str_unique([c for c in s])


def str_asm_combos(a: str, others: list[str]) -> list[str]:
    """str_asm_combos: possible left and right side concatenations of string assembly"""
    return str_unique([a + o for o in others] + [o + a for o in others])


def already_asmed(node: Node):
    # recur backwards up till we hit parent of None
    if node.is_atom:
        return []

    return already_asmed(node.parent) + [node.data]


def backtrack_asm_index(node: Node, print_path=False):
    solution = []

    def _backtrack(node: Node):
        solution.append(node.data)
        if node.is_atom:
            return
        _backtrack(node.parent)

    _backtrack(node)
    return list(reversed(solution))


def str_asm_index(s: str) -> int:
    """a_i: assembly index with smallest assembly path

    Returns:
        int: the asm index of the string
    """
    # can't assemble nothing or a single atom (one atom is already assembled)
    if len(s) <= 1:
        return [s]

    atoms = str_atomize(s)

    # but anything over three is not clear what the assembly index is
    # so we have to combinatorially try stuff
    uber_root = Node(data=None, parent=None)
    q = [Node(data=a, parent=uber_root, is_atom=True) for a in atoms]
    while len(q) > 0:
        cur = q.pop(0)

        # otherwise, continue to look for solutions
        pool = atoms + already_asmed(cur)  # can use already assembled for cost of 1
        for new_asm in str_asm_combos(cur.data, pool):
            if new_asm == s:
                res = backtrack_asm_index(Node(data=new_asm, parent=cur))
                return res
            elif len(new_asm) <= len(s) and new_asm in s:
                q.append(Node(data=new_asm, parent=cur))

    return []


def asm_diff(a: str, b: str):
    if b.index(a) == 0:
        return b[b.index(a) + len(a) :]
    else:
        return b[: b.index(a)]


def format_graph_md(solution: list[str]):
    output = ""
    output += "```mermaid\n"
    output += "graph LR;\n"
    first, *rest = solution
    for s in rest:
        diff = asm_diff(first, s)
        output += f"{first}-->{s};\n"
        output += f"{diff}-->{s};\n"
        first = s
    output += "```"
    return output


def simple_tests():
    s1 = "A"
    s2 = "AB"
    s3 = "ABAB"
    s4 = "ABRACADABRA"

    res = str_asm_index(s1)
    assert len(res) == 1

    res = str_asm_index(s2)
    assert len(res) == 2

    res = str_asm_index(s3)
    assert len(res) == 3

    res = str_asm_index(s4)
    assert len(res) == 8

    print("ALL TESTS PASSED")


def md_example(a: str):
    res = str_asm_index(a)
    print(f"### `{a}`")
    print()
    print(f"Assembly index of `{len(res) - 1}`")
    print()
    print(format_graph_md(res))


if __name__ == "__main__":
    simple_tests()
    md_example("AB")
    md_example("ABAB")
    md_example("ABRACADABRA")
