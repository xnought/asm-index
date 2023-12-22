class Node:
    def __init__(self, data, parent=None, is_atom=False, depth=0, children=None):
        self.data = data
        self.parent = parent
        self.is_atom = is_atom
        self.depth = depth
        if children is None:
            self.children = []
        self.merger = (None, None)  # tells which nodes merged to make this node

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


def node_asm_combos(parent: Node, asmed: list[Node]) -> list[Node]:
    """str_asm_combos: possible left and right side concatenations of string assembly"""
    res = []
    for a in asmed:
        rhs = parent.data + a.data
        lhs = a.data + parent.data

        res.append(Node(data=lhs, parent=parent, depth=parent.depth + 1))

        if rhs != lhs:
            res.append(Node(data=rhs, parent=parent, depth=parent.depth + 1))

    return res


def already_asmed(node: Node):
    # recur backwards up till we hit parent of None
    if node.is_atom:
        return []

    return already_asmed(node.parent) + [node.data]


def already_asmed_to_depth(root_node: Node, depth: int = 0) -> list[Node]:
    asmed = []

    def _compile(node: Node):
        for c in node.children:
            if c.depth <= depth:
                asmed.append(c)
                _compile(c)

    _compile(root_node)
    return asmed


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
    uber_root = Node(data=None, parent=None, depth=0)
    uber_root.children = [
        Node(data=a, parent=uber_root, is_atom=True, depth=uber_root.depth + 1)
        for a in atoms
    ]
    q = [c for c in uber_root.children]

    while len(q) > 0:
        cur = q.pop(0)
        asmed = already_asmed_to_depth(uber_root, depth=cur.depth)
        print(cur, asmed)
        for new_asm in node_asm_combos(cur, asmed):
            if new_asm.data == s:
                return backtrack_asm_index(new_asm)
            elif (
                len(new_asm.data) <= len(s)
                and new_asm.data in s
                and new_asm.data not in [c.data for c in q]
                and new_asm.data not in asmed
                and new_asm.data != cur.data
            ):
                cur.children.append(new_asm)
                q.append(new_asm)

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

    # res = str_asm_index(s1)
    # assert len(res) == 1

    # res = str_asm_index(s2)
    # assert len(res) == 2

    # res = str_asm_index(s3)
    # assert len(res) == 3

    res = str_asm_index(s4)
    print(res)
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
    # md_example("AB")
    # md_example("ABAB")
    # md_example("ABRACADABRA")
