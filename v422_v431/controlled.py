"""Exact finite-dimensional calculations for v4.22–v4.24."""
from collections import deque
from itertools import product

import sympy as sp


def instrument():
    """States are (persistent bit, environment bit). Rows act before readout."""
    matrix = sp.Matrix
    r = sp.Rational
    initial = matrix([[r(42, 100), r(18, 100), r(28, 100), r(12, 100)]])
    normal = sp.diag(matrix([[9, 1], [2, 8]]) / 10,
                     matrix([[6, 4], [5, 5]]) / 10)
    reset = sp.diag(*([matrix([[3, 7], [3, 7]]) / 10] * 2))
    mixed = (2 * normal + reset) / 3
    emission = (sp.diag(9, 1, 9, 1) / 10, sp.diag(1, 9, 1, 9) / 10)
    transitions = {"normal": normal, "reset": reset, "mixed": mixed}
    operators = {(action, y): transition * emission[y]
                 for action, transition in transitions.items() for y in range(2)}
    return initial, operators, emission, transitions


def probability(initial, operators, word):
    row = initial
    for letter in word:
        row = row * operators[letter]
    return (row * sp.ones(row.cols, 1))[0]


def closure(initial, operators, final):
    """Breadth-first exact spanning basis and shortest distinguishing word."""
    basis = []
    queue = deque([(initial, ())])
    witness = None
    while queue:
        row, word = queue.popleft()
        if sp.Matrix.vstack(*basis, row).rank() == len(basis):
            continue
        basis.append(row)
        difference = (row * final)[0]
        if difference and witness is None:
            witness = {"word": word, "difference": str(difference)}
        queue.extend((row * op, word + (letter,)) for letter, op in operators.items())
    return {"basis_dimension": len(basis), "witness": witness}


def equivalence():
    initial, operators, emission, transitions = instrument()
    # A different device ordering: (E,C) instead of (L,E).
    perm = sp.eye(4)[:, [0, 2, 1, 3]]
    device_initial = initial * perm
    device = {letter: perm.T * op * perm for letter, op in operators.items()}
    paired = sp.Matrix.hstack(initial, device_initial)
    final = sp.Matrix([1, 1, 1, 1, -1, -1, -1, -1])

    def compare(device_operators):
        return closure(paired, {letter: sp.diag(op, device_operators[letter])
                                for letter, op in operators.items()}, final)

    # Replace the reset on C by C=0 while keeping the same E preparation.
    clear_bit = sp.Matrix([[1, 0, 0, 0], [0, 1, 0, 0],
                           [1, 0, 0, 0], [0, 1, 0, 0]])
    positive = dict(device)
    for y in range(2):
        positive["reset", y] = perm.T * transitions["reset"] * clear_bit * emission[y] * perm

    # Randomized policy conditional on the entire observed record so far.
    def follow(device_operators):
        leaves = []
        for outcomes in product(range(2), repeat=4):
            value = 0
            for actions in product(("normal", "reset", "mixed"), repeat=4):
                weight = sp.S.One
                for tick, action in enumerate(actions):
                    weights = (2, 1, 1) if sum(outcomes[:tick]) % 2 == 0 else (1, 2, 1)
                    weight *= sp.Rational(weights[("normal", "reset", "mixed").index(action)], 4)
                value += weight * probability(
                    device_initial, device_operators, tuple(zip(actions, outcomes)))
            leaves.append(value)
        return leaves

    reference = follow(device)
    modified = follow(positive)
    return {
        "equivalent": compare(device),
        "changed_reset": compare(positive),
        "adaptive_total_mass": str(sum(reference)),
        "adaptive_changed_total_variation": str(sum(abs(a - b) for a, b in zip(reference, modified)) / 2),
    }


def hankel():
    initial, operators, _, _ = instrument()

    def first_minor(alphabet, max_depth=2):
        words = [()]
        ranks = []
        for depth in range(max_depth + 1):
            if depth:
                words.extend(product(alphabet, repeat=depth))
            values = sp.Matrix([[probability(initial, operators, u + v) for v in words]
                                for u in words])
            # Factorization through four states bounds rank by 4.
            columns = values.rref()[1]
            ranks.append(len(columns))
            if len(columns) == 4:
                rows = values[:, list(columns)].T.rref()[1]
                minor = values.extract(rows, columns).det()
                return {"depth": depth, "ranks_by_depth": ranks, "determinant": str(minor),
                        "rows": [words[j] for j in rows], "columns": [words[j] for j in columns]}
        return {"ranks_by_depth": ranks}

    return {"controlled": first_minor(tuple(operators)),
            "passive": first_minor(tuple(key for key in operators if key[0] == "normal"))}


def positive_realization():
    # Each context chooses one of two readouts and asks for one of its two outcomes.
    table = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 0, 0, 1]])
    simpler = sp.Matrix([[1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 1, 1], [1, 1, 0, 0]])
    assert all(m[i, 0] + m[i, 2] == m[i, 1] + m[i, 3] == 1
               for m in (table, simpler) for i in range(4))
    # A nonnegative rank-one term has rectangular support. All maximal
    # rectangles here have two entries, while the table has eight positives.
    largest = 0
    for bits in product((False, True), repeat=4):
        rows = [i for i, included in enumerate(bits) if included]
        if rows:
            columns = [j for j in range(4) if all(table[i, j] for i in rows)]
            largest = max(largest, len(rows) * len(columns))
    unique_rows = {tuple(simpler.row(i)) for i in range(4)}
    return {"square_rank": table.rank(), "simpler_rank": simpler.rank(),
            "largest_positive_rectangle": largest,
            "square_nonnegative_lower": sum(bool(value > 0) for value in list(table)) // largest,
            "square_nonnegative_upper": table.rows, "simpler_nonnegative_upper": len(unique_rows),
            "square_table": [[int(x) for x in row] for row in table.tolist()], "simpler_table": [[int(x) for x in row] for row in simpler.tolist()]}
