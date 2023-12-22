class Node:
    def __init__(self, data, parent=None, children=[]):
        self.data = data
        self.parent = parent
        self.children = children

    def __repr__(self):
        return f"{self.data}"


def str_unique(strs: list[str]) -> list[str]:
    """unique: return a list of unique strings"""
    uniq = [strs[0]]
    for s in strs[1:]:
        if s not in uniq:
            uniq.append(s)

    return list(reversed(uniq))


def str_atomize(s: str) -> list[str]:
    """atomize: break a string into its atoms, for us this means characters (bytes)
    for more complicated objects, will need more complicated atomize functions
    """
    return str_unique([c for c in s])


def str_asm_combos(a: str, others: list[str]) -> list[str]:
    """str_asm_combos: possible left and right side concatenations of string assembly"""
    return str_unique([a + o for o in others] + [o + a for o in others])


# def plausible_asms(
#     node: Node, pool: list[str], solution: str, tried: list[str]
# ) -> list[Node]:
#     """possible_children: given a node, return all possible children"""
#     # adds all combos and if the combos are definitely wrong, (like a substring that never shows up, then we're soooo wrong and don't need to add)
#     return [
#         Node(data=p, parent=node)
#         for p in str_asm_combos(node.data, pool)
#         if p in solution
#         and len(p) <= len(solution)
#         and p != node.data
#         and p not in tried
#     ]


def already_asmed(node: Node):
    # recur backwards up till we hit parent of None
    if node.parent is None:
        return []

    return already_asmed(node.parent) + [node.data]


def backtrack_asm_index(node: Node, print_path=False):
    if print_path:
        print(node.data)
    if node.parent is None:
        return 0

    return backtrack_asm_index(node.parent) + 1


def str_asm_index(s: str) -> int:
    """a_i: assembly index with smallest assembly path

    Returns:
        int: the asm index of the string
    """
    # can't assemble nothing or a single atom (one atom is already assembled)
    if len(s) <= 1:
        return 0
    # two objects can be assembled in one step
    elif len(s) == 2:
        return 1
    # three objects can be assembled in two step
    elif len(s) == 3:
        return 2

    atoms = str_atomize(s)

    # but anything over three is not clear what the assembly index is
    # so we have to combinatorially try stuff
    root = Node(data=atoms[0])
    cur = root
    q = [root]

    while len(q) > 0:
        cur = q.pop(0)

        # otherwise, continue to look for solutions
        pool = atoms + already_asmed(cur)  # can use already assembled for cost of 1
        for new_asm in str_asm_combos(cur.data, pool):
            if new_asm == s:
                return backtrack_asm_index(Node(data=new_asm, parent=cur))
            elif (
                len(new_asm) <= len(s)
                and new_asm in s
                and new_asm not in [n.data for n in q]
            ):
                q.append(Node(data=new_asm, parent=cur))

    return float("inf")


if __name__ == "__main__":
    s1 = "A"
    s2 = "AB"
    s3 = "ABAB"
    s4 = "ABRACADABRA"

    # assert str_asm_index(s1) == 0
    # print("PASSED TEST 1")

    # assert str_asm_index(s2) == 1
    # print("PASSED TEST 2")

    # assert str_asm_index(s3) == 2
    # print("PASSED TEST 3")

    assert str_asm_index(s4) == 7
    print("PASSED TEST 4")
