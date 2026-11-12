"""Parity selection rules in a finite Rabi Fock basis (hbar=1)."""
import math

def parity(atom, n):
    if atom not in (0, 1) or not isinstance(n, int) or n < 0:
        raise ValueError('invalid basis state')
    return (-1 if atom == 0 else 1) * (-1 if n % 2 else 1)

def operator_parity(name):
    if name in ('field_x', 'sigma_x'): return -1
    if name in ('number', 'sigma_z', 'identity'): return 1
    raise ValueError('unknown operator')

def symmetry_allows(p_initial, p_final, op_parity):
    if any(p not in (-1, 1) for p in (p_initial, p_final, op_parity)):
        raise ValueError('parities must be +/-1')
    return p_final == op_parity * p_initial

def bare_matrix_element(name, initial, final):
    """<final|O|initial> for atom 0=g, 1=e, n>=0."""
    ai, ni = initial
    af, nf = final
    parity(ai, ni); parity(af, nf)
    operator_parity(name)
    if name == 'identity': return float(initial == final)
    if name == 'number': return float(ni) if initial == final else 0.
    if name == 'sigma_z': return float(2*ai-1) if initial == final else 0.
    if name == 'sigma_x': return 1. if ni == nf and ai != af else 0.
    if ai != af: return 0.
    if nf == ni+1: return math.sqrt(ni+1)
    if nf == ni-1: return math.sqrt(ni)
    return 0.

def rabi_coupling(initial, final, g):
    if not math.isfinite(g): raise ValueError('nonfinite coupling')
    ai,ni=initial; af,nf=final
    parity(ai,ni); parity(af,nf)
    if ai == af: return 0.
    return g*bare_matrix_element('field_x',(ai,ni),(ai,nf))
