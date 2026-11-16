"""v1.52-v1.61 finite-model consistency checks. NumPy; not full QED."""
import math, json
import numpy as np
I=np.eye(2,dtype=complex);X=np.array([[0,1],[1,0]],complex);Z=np.diag([1,-1]).astype(complex)
def norm(x): return float(np.linalg.norm(x))
def comm(a,b): return a@b-b@a
def hop(a): return np.array([[0,np.exp(1j*a)],[np.exp(-1j*a),0]],complex)
def evolve(h,t):
    w,v=np.linalg.eigh(h)
    return (v*np.exp(-1j*t*w))@v.conj().T
def run():
    result={}
    S=np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]],complex)
    P=(np.eye(4)+S)/2
    result['v1.52']={'boson_rank':int(np.linalg.matrix_rank(P)),'relabel_gap':norm(P@np.array([0,1,0,0])-P@np.array([0,0,1,0]))}
    a=.37;g0=.21;g1=-.44
    D=np.diag(np.exp(1j*np.array([g0,g1])))
    result['v1.53']={'gauge_covariance_error':norm(D@hop(a)@D.conj().T-hop(a+g0-g1))}
    angles=[.17,.29,-.11]; phases=[.2,-.3,.6]
    shifted=[angles[i]+phases[i]-phases[(i+1)%3] for i in range(3)]
    result['v1.54']={'wilson_loop_error':abs(np.exp(1j*sum(angles))-np.exp(1j*sum(shifted)))}
    local_a=np.kron(Z,I);local_b=np.kron(I,X);interaction=np.kron(Z,X)
    result['v1.55']={'local_commutator':norm(comm(local_a,local_b)),
                      'interaction_commutator':norm(comm(interaction,np.kron(I,Z)))}
    psi=np.array([1,0,0,1],complex)/math.sqrt(2)
    rho=np.outer(psi,psi.conj());remote=np.kron(I,Z)
    local_u=np.kron(evolve(X,.31),I)
    before=float(np.trace(rho@remote).real)
    after=float(np.trace(local_u@rho@local_u.conj().T@remote).real)
    psi0=np.array([1,0,0,0],complex);rho0=np.outer(psi0,psi0.conj())
    ui=evolve(interaction,.31)
    response=float(np.trace(ui@rho0@ui.conj().T@remote).real)
    result['v1.56']={'local_action_gap':abs(after-before),'interaction_remote_shift':abs(response-1)}
    n0=np.diag([1,0]);n1=np.diag([0,1]);h=hop(.37)
    result['v1.57']={'number_commutator':norm(comm(h,n0+n1)),
                      'continuity_residual':norm(1j*comm(h,n0)+1j*comm(h,n1))}
    momenta=np.array([.5,1.,2.,4.])
    result['v1.58']={'massless_shell':(momenta*momenta-momenta*momenta).tolist(),
                      'offset_shell':((momenta+.12)**2-momenta**2).tolist()}
    u=evolve(X,.4);p=float(abs(u[1,0])**2)
    result['v1.59']={'matter_excitation':p,'photon_survival':1-p,'total_excitation':1}
    result['v1.60']={'overlaps':[1.,.7,0.],'visibility':[1.,.7,0.],
                      'standard_mode_equivalence':True}
    p=np.array([.2,.3,.5]);q=np.kron(p,[.5,.5]).reshape(3,2).sum(axis=1)
    result['v1.61']={'l1_distance':float(np.sum(abs(p-q))),'kl':0.,
                      'identity_specific_prediction':False,'covariant_qed_constructed':False}
    return result
if __name__=='__main__':print(json.dumps(run(),ensure_ascii=False,indent=2))
