"""First consistency audits for candidate identity couplings."""
import json
import numpy as np
from .ring import solve

def run():
    z=np.diag([1.,-1.]); eye=np.eye(2)
    swap=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],float)
    slot=np.kron(z,eye); collective=np.kron(z,eye)+np.kron(eye,z)
    # Rank of the swap twirl on the full Hermitian Pauli product basis.
    pauli = [eye, np.array([[0,1],[1,0]]), np.array([[0,-1j],[1j,0]]), z]
    products = [np.kron(a,b) for a in pauli for b in pauli]
    projected = [(h + swap@h@swap)/2 for h in products]
    invariant_dimension = int(np.linalg.matrix_rank(np.stack(projected).reshape(16,16)))
    slot_comm=np.linalg.norm(slot@swap-swap@slot)
    collective_comm=np.linalg.norm(collective@swap-swap@collective)
    # Two-mode Fock truncation |00>,|10>,|01>,|11>.
    number=np.diag([0.,1.,1.,2.])
    exchange=np.array([[0,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,0]],float)
    pair=np.array([[0,0,0,1],[0,0,0,0],[0,0,0,0],[1,0,0,0]],float)
    return {**solve(), 'exchange_symmetry':{'invariant_dimension':invariant_dimension,'slot_commutator':float(slot_comm),'collective_commutator':float(collective_comm)},
            'number_conservation':{'exchange_commutator':float(np.linalg.norm(number@exchange-exchange@number)),
                                   'pair_commutator':float(np.linalg.norm(number@pair-pair@number))}}

if __name__=='__main__': print(json.dumps(run(),indent=2))
