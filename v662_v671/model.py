"""Measurements transcribed from published Ge figures, kinematics and controls."""
import json
from pathlib import Path
import numpy as np
from scipy.integrate import quad
from scipy.linalg import expm

ROOT=Path(__file__).parent
REST=510.99895

def data(name):
    return json.loads((ROOT/name).read_text())

def spectral_markers():
    rows=[]
    for f in data('figure_points.json')['figures']:
        (x0,a),(x1,b)=f['axis_anchors_px_keV']
        scale=(b-a)/(x1-x0)
        e=a+(f['peak_marker_px']-x0)*scale
        rows.append(dict(figure=f['figure'],marker_keV=e,
                         complementary_Kalpha_keV=f['incident_keV']-9.876,
                         marker_minus_complement_keV=e-f['incident_keV']+9.876,
                         four_pixel_sensitivity_keV=4*scale))
    return rows

def angular_support():
    e=59.537
    out=[]
    rng=np.random.default_rng(66301)
    n=rng.normal(size=(30000,3));n/=np.linalg.norm(n,axis=1)[:,None]
    for deg in (3.,170.,180.):
        th=np.deg2rad(deg)
        v=np.array([np.sin(th),0.,1+np.cos(th)])
        width=np.linalg.norm(v)
        center=1/e+2/REST
        low,high=1/(center+width/REST),1/(center-width/REST)
        two=1/(center-(n@v)/REST)
        single=1/(1/e+(1-np.cos(th))/REST)
        out.append(dict(theta_deg=deg,single_keV=single,double_support_keV=[low,high],
                        sample_range=[two.min(),two.max()],backscatter_degeneracy_error=float(np.max(abs(two-single))) if deg==180 else None))
    # Backscatter only: marginal atomic momentum density, truncated to |pz|<=5 au.
    # Collinear moving on-shell electron: E' = E*(H-pz)/(H+pz+2E).
    # This is a Doppler surrogate, neglecting binding thresholds and transverse p.
    grid=np.array(data('atomic.json')['Ge']['profile_au'])
    p=np.r_[-grid[:0:-1,0],grid[:,0]]
    weights=np.r_[grid[:0:-1,1],grid[:,1]]
    cdf=np.r_[0,np.cumsum(np.diff(p)*(weights[1:]+weights[:-1])/2)]
    quant=np.interp([.05,.5,.95],cdf/cdf[-1],p)*REST/137.035999
    en=np.hypot(REST,quant)
    scattered=e*(en-quant)/(en+quant+2*e)
    return dict(free=out,conditional_doppler_keV=scattered[::-1].tolist(),pz_truncation_au=5.)

def target_substitution():
    result=[]
    for name,m in data('atomic.json').items():
        total,compt,photo,ray=m['cross_sections']['60.0']
        for h in (.1,.27/m['density']):
            p=-np.expm1(-m['density']*h*total)
            result.append(dict(material=name,thickness_cm=h,areal_density=h*m['density'],
                               first_interaction=p,first_compton=p*compt/total,
                               photo_fraction=photo/total,rayleigh_fraction=ray/total))
    return result

def recoil_collection():
    # Uniform isotropic fixed-range tracks in a slab. Outside tag counts escaping tracks.
    # Analytic for R<=h; no microscopic range prediction is made here.
    h=.10
    result=[]
    for R in (.002,.01,.04):
        prob=quad(lambda z:.5*(max(0.,1-z/R)+max(0.,1-(h-z)/R)),0,h,points=[R,h-R])[0]/h
        # Track exits with enough remaining length to carry at least half the energy.
        half=R/(4*h)
        result.append(dict(range_cm=R,escape_probability=prob,analytic=R/(2*h),
                           external_half_energy=half,full_containment=1-prob))
    return result

def fluorescence_filter():
    m=data('atomic.json')['Ge'];rho=m['density']
    rows=[]
    for um in (0.,10.,100.):
        vals={e:np.exp(-rho*(um/10000)*m['cross_sections'][e][0]) for e in ('9.876','10.98','45.0')}
        rows.append(dict(thickness_um=um,transmission=vals,
                         alpha_over_continuum=vals['9.876']/vals['45.0'],
                         beta_over_continuum=vals['10.98']/vals['45.0']))
    return rows

def depth_selection():
    # Hypothetical two-sided charge collection gradient measured by independent probes.
    h=.1;mu=.75;loss=.32;threshold=.85
    def probability(rate):
        cut=h*(1-threshold)/loss
        return -np.expm1(-rate*cut)/(-np.expm1(-rate*h))
    a,b=probability(mu),probability(18.)
    return dict(science_tag=a,external_tag=b,relative_bias=b/a-1,
                reversed_science=(np.exp(-mu*(h-h*(1-threshold)/loss))-np.exp(-mu*h))/-np.expm1(-mu*h))

def prompt_control():
    # Off-time plus two prompt configurations (transmitting and attenuated).
    M=np.array([[1.,0,0],[1,1,1],[1,1,.2]])
    truth=np.array([.7,1.8,2.5]);y=M@truth
    alt=np.array([.7,2.3,2.]);error=M@alt-y
    return dict(count_rates=y.tolist(),recovered=np.linalg.solve(M,y).tolist(),
                normal_and_off_residual=error[:2].tolist(),heldout_residual=error[2],
                min_singular=np.linalg.svd(M,compute_uv=False)[-1],
                crosstalk_offset_needed=-error[2])

def efficiency_transfer():
    # Finite support; common conditional tag efficiency under transport.
    ps=np.array([.15,.40,.45]);pc=np.array([.7,.25,.05]);eff=np.array([.9,.7,.3])
    nominal=pc@eff;weighted=np.sum(pc*(ps/pc)*eff)
    return dict(reference=nominal,science=weighted,unweighted_bias=nominal-weighted,
                max_density_ratio=max(ps/pc),missing_third_stratum_interval=[ps[:2]@eff[:2],ps[:2]@eff[:2]+ps[2]])

def coherent_storage():
    # Excitation-preserving transfer between a photonic mode and an ordinary material oscillator.
    # A pulse at one frequency vs a broadband pulse: compare joint frequency/time-bin records.
    x=np.arange(16);psi=np.exp(-((x-6)/2.4)**2 + .14j*x*x);psi=psi/np.linalg.norm(psi)
    transfer=expm(-.5j*np.pi*np.array([[0,1],[1,0]]))
    phase=np.exp(.19j*x+.012j*x*x)
    ordinary=transfer[0,1]*phase*transfer[1,0]*psi
    ideal=-phase*psi
    # Two output arms with a frequency-bin analyzer then a Fourier time measurement.
    P=np.array([np.cos(x/6),np.sin(x/6)])
    bands=(x[None,:]//4 == np.arange(4)[:,None])
    def record(a):
        amplitudes=bands[:,None,:]*P[None,:,:]*a
        return abs(np.fft.fft(amplitudes,axis=-1,norm='ortho'))**2
    return dict(stored_optical_fraction=abs(transfer[0,0])**2,record_sum=record(ordinary).sum(),
                joint_record_max_error=np.max(abs(record(ordinary)-record(ideal))),
                ordinary_phase_drift_error=np.max(abs(record(ordinary*np.exp(.18j*x))-record(ideal))))

def dimensional_coupling():
    # Candidate phase lambda*tau, ordinary unknown detuning Delta*tau in Ramsey readout.
    lam=2*np.pi*1.2e3
    tau=np.array([0.,20.,60.,110.])*1e-6
    delta=2*np.pi*.4e3
    def quadratures(omega):return np.c_[np.cos(omega*tau),np.sin(omega*tau)]
    measured=quadratures(lam+delta)
    refit=quadratures(delta+lam)
    return dict(candidate_rad_s=lam,ordinary_detuning_rad_s=delta,refitted_rad_s=delta+lam,
                delays_us=(tau*1e6).tolist(),max_error=np.max(abs(measured-refit)),
                max_complex_distance_if_detuning_fixed=np.max(abs(np.exp(1j*(lam+delta)*tau)-np.exp(1j*delta*tau))))

def run():
    fns=[spectral_markers,angular_support,target_substitution,recoil_collection,fluorescence_filter,
         depth_selection,prompt_control,efficiency_transfer,coherent_storage,dimensional_coupling]
    return {f'v6.{n}':fn() for n,fn in enumerate(fns,62)}
if __name__=='__main__':
    print(json.dumps(run(),indent=2))
