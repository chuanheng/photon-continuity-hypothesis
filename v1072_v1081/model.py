"""Control and target statistics of two orders of optical operations."""
import json
import numpy as np

I=np.eye(2);X=np.array([[0,1],[1,0]]);Z=np.diag([1,-1]);Y=1j*X@Z
PAULI=[I,X,Y,Z]
def turn(P,t):return np.cos(t/2)*I-1j*np.sin(t/2)*P
def blocks(A,B,rho):
    diag=np.zeros((2,2),complex);cross=diag.copy()
    for a in A:
        for b in B:
            c,d=b@a,a@b
            diag+=(c@rho@c.conj().T+d@rho@d.conj().T)/2
            cross+=c@rho@d.conj().T
    return diag,cross

def run():
    rho=(I+Z)/2;mixed=I/2
    traced=lambda a,b,r: np.trace(blocks([a],[b],r)[1])
    angles=.84,1.12
    A,B=turn(X,angles[0]),turn(Z,angles[1])
    val=traced(A,B,mixed)
    unitary=(A@B).conj().T@B@A
    eig,vectors=np.linalg.eig(unitary)
    # One material probe with nuisance (partly distinguishable) order records.
    eta0,eta1=.2,.8
    # Memoryless independent Pauli errors vs shared random Pauli.
    ops=np.array(PAULI)/2
    d,c=blocks(ops,ops,rho)
    pplus=(d+(c+c.conj().T)/2)/2
    had=np.array([[1,1,1,1],[1,-1,1,-1],[1,1,-1,-1],[1,-1,-1,1]])/2
    changed=np.einsum('ij,jab->iab',had,ops)
    dm,cm=blocks(changed,ops,rho)
    # Encoded target is physically stored in a material doublet in a rotated basis.
    V=turn(Y,.63);enc=lambda m:V@m@V.conj().T
    encd,encc=blocks([enc(A)],[enc(B)],enc(rho))
    dg,cg=blocks([A],[B],rho)
    return dict(order_sign=dict(anticommuting=float(traced(X,Z,rho).real),same_channel_error=float(np.linalg.norm((Z@X)@rho@(Z@X).conj().T-(X@Z)@rho@(X@Z).conj().T))),
                finite_rotation=dict(pminus=float((1-val.real)/2),trace_imag=float(val.imag)),
                quadrature=dict(eigen_imag=sorted(eig.imag.tolist()),real=float(eig.real[0])),
                order_record=dict(overlap=.38,pminus=(1+.38)/2),
                unequal_loss=dict(unconditional_dark=(np.sqrt(eta0)-np.sqrt(eta1))**2/4,
                                  conditional_visibility=2*np.sqrt(eta0*eta1)/(eta0+eta1)),
                channel_memory=dict(independent=float(np.trace(c).real),shared=float(np.mean([traced(p,p,rho).real for p in PAULI]))),
                noisy_pair=dict(plus_probability=float(pplus.trace().real),conditional_fidelity=float(pplus[0,0].real/pplus.trace().real)),
                kraus_gauge=dict(diagonal_error=float(np.linalg.norm(dm-d)),cross_error=float(np.linalg.norm(cm-c))),
                device_phase=dict(commuting_with_offset=float((1+np.cos(np.pi))/2),anti_without_offset=float((1+traced(X,Z,rho).real)/2)),
                material=dict(diagonal=float(np.linalg.norm(V.conj().T@encd@V-dg)),cross=float(np.linalg.norm(V.conj().T@encc@V-cg))))
if __name__=='__main__':print(json.dumps(run(),indent=2))
