def atomize(s: str) -> list[str]:
    return [c for c in s]


def str_asm_index(s: str) -> int:
    """a_i: assembly index with smallest assembly path

    Returns:
        int: the asm index of the string
    """
    atoms = atomize(s)

    # can't assemble nothing or a single atom (one atom is already assembled)
    if len(atoms) <= 1:
        return 0

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
