"""Three-state photon-number commutator; a conditional mathematical result.

Basis photon counts (1,1,0); H is a real symmetric toy Hamiltonian.
No physical interaction strength is derived.
"""
import math

def commutator_with_photon_number(hamiltonian):
    if len(hamiltonian)!=3 or any(len(row)!=3 for row in hamiltonian):
        raise ValueError("Hamiltonian must be 3x3")
    if any(not math.isfinite(v) for row in hamiltonian for v in row):
        raise ValueError("Hamiltonian entries must be finite")
    if any(abs(hamiltonian[i][j]-hamiltonian[j][i])>1e-12 for i in range(3) for j in range(3)):
        raise ValueError("Hamiltonian must be real symmetric")
    n=(1,1,0)
    return [[hamiltonian[i][j]*(n[j]-n[i]) for j in range(3)] for i in range(3)]

def is_photon_number_conserved(hamiltonian, tolerance=1e-12):
    if not math.isfinite(tolerance) or tolerance<0:
        raise ValueError("tolerance must be finite and nonnegative")
    return all(abs(v)<=tolerance for row in commutator_with_photon_number(hamiltonian) for v in row)

if __name__=="__main__":
    h_survival=[[0,1,0],[1,2,0],[0,0,3]]
    h_absorption=[[0,1,.2],[1,2,0],[.2,0,3]]
    print("Survival-only commutes:",is_photon_number_conserved(h_survival))
    print("Absorption coupling commutes:",is_photon_number_conserved(h_absorption))
