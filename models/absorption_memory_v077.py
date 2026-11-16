"""v0.77: coherent a<->e excitation swap, controlled storage phase and
operational equivalence with a relabeled environmental memory.
Not a photon-identity theorem or a full QED model.
"""
import numpy as np
I3=np.eye(3,dtype=complex)
I2=np.eye(2,dtype=complex)
EA=np.array([1,0,0],complex)
EB=np.array([0,1,0],complex)
EE=np.array([0,0,1],complex)
H0=np.array([1,0],complex)
H1=np.array([0,1],complex)
PA=np.outer(EA,EA.conj())
PB=np.outer(EB,EB.conj())
PE=np.outer(EE,EE.conj())
P1=np.outer(H1,H1.conj())

def ket_dm(psi):
    psi=np.asarray(psi,complex)
    if psi.ndim!=1 or not np.isclose(np.vdot(psi,psi),1):
        raise ValueError('ket must be normalized')
    return np.outer(psi,psi.conj())

def absorber(theta=np.pi/2):
    c,s=np.cos(theta),np.sin(theta)
    return np.array([[c,0,-1j*s],[0,1,0],[-1j*s,0,c]],complex)

def storage_phase(phi):
    return np.eye(6,dtype=complex)+(np.exp(1j*phi)-1)*np.kron(PE,P1)

def protocol(phi,theta=np.pi/2):
    a=np.kron(absorber(theta),I2)
    return a.conj().T@storage_phase(phi)@a

def optical_input():
    return (EA+EB)/np.sqrt(2)

def output(phi,label_bit,theta=np.pi/2):
    if label_bit not in (0,1):raise ValueError('label_bit must be 0 or 1')
    return protocol(phi,theta)@np.kron(optical_input(),H0 if label_bit==0 else H1)

def reduced_optical(rho):
    rho=np.asarray(rho,complex)
    if rho.shape!=(6,6):raise ValueError('joint density must be 6x6')
    return np.einsum('ihjh->ij',rho.reshape(3,2,3,2))

def optical_detection(phi,label_bit,theta=np.pi/2):
    rho=reduced_optical(ket_dm(output(phi,label_bit,theta)))
    plus=ket_dm(optical_input())
    minus=ket_dm((EA-EB)/np.sqrt(2))
    return {'plus':float(np.trace(rho@plus).real),
        'minus':float(np.trace(rho@minus).real),
        'material_excitation':float(np.trace(rho@PE).real),
        'optical_a':float(np.trace(rho@PA).real),
        'optical_b':float(np.trace(rho@PB).real)}

def trace_distance(a,b):
    return float(np.abs(np.linalg.eigvalsh(a-b)).sum()/2)

def optical_distinguishability(phi,theta=np.pi/2):
    r0=reduced_optical(ket_dm(output(phi,0,theta)))
    r1=reduced_optical(ket_dm(output(phi,1,theta)))
    return trace_distance(r0,r1)

def swapped_ancilla_protocol(phi,theta=np.pi/2):
    x=np.array([[0,1],[1,0]],complex)
    j=np.kron(I3,x)
    return j@protocol(phi,theta)@j

def memory_equivalent_output(phi,identity_bit,theta=np.pi/2):
    m=H1 if identity_bit==0 else H0
    return swapped_ancilla_protocol(phi,theta)@np.kron(optical_input(),m)

def analytic_full_absorption(phi,label_bit):
    return (np.exp(1j*phi*label_bit)*EA+EB)/np.sqrt(2)

def occupied_e_during_storage(label_bit):
    h=H0 if label_bit==0 else H1
    psi=np.kron(absorber(np.pi/2),I2)@np.kron(optical_input(),h)
    rho=ket_dm(psi)
    return {'e':float(np.trace(rho@np.kron(PE,I2)).real),
       'a':float(np.trace(rho@np.kron(PA,I2)).real),
       'b':float(np.trace(rho@np.kron(PB,I2)).real)}

def summary():
    p=np.pi
    return {'phase_pi_label0':optical_detection(p,0),
      'phase_pi_label1':optical_detection(p,1),
      'optical_trace_distance_phase_pi':optical_distinguishability(p),
      'optical_trace_distance_phase_half_pi':optical_distinguishability(p/2),
      'storage_at_full_absorption':occupied_e_during_storage(0),
      'max_system_memory_equivalence_error':max(
        float(np.linalg.norm(
          reduced_optical(ket_dm(output(phi,bit)))-
          reduced_optical(ket_dm(memory_equivalent_output(phi,bit)))))
        for phi in [0.,.2,.6,p/2,p] for bit in [0,1])}
