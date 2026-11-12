"""Idealized atomic angular momentum and parity selection rules.

Necessary conditions for E1/M1/E2 transitions; not sufficient for a
nonzero matrix element and not a photon-survival theorem.
Twice-J integers support half-integer angular momenta.
"""

def multipole_allowed(j2_initial, j2_final, parity_initial, parity_final, kind):
    for j in (j2_initial, j2_final):
        if type(j) is not int or j < 0:
            raise ValueError('twice-J must be a nonnegative integer')
    if parity_initial not in (-1, 1) or parity_final not in (-1, 1):
        raise ValueError('parity must be +1 or -1')
    if kind not in ('E1', 'M1', 'E2'):
        raise ValueError('kind must be E1, M1 or E2')
    rank = 2 if kind == 'E2' else 1
    triangle = abs(j2_initial-j2_final) <= 2*rank <= j2_initial+j2_final
    sector = (j2_initial-j2_final) % 2 == 0
    expected_parity_ratio = -1 if kind == 'E1' else 1
    return triangle and sector and parity_initial*parity_final == expected_parity_ratio
