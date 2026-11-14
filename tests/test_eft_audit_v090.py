"""39 executable tests of v0.90 dimensional, Ward, Lorentz and EFT checks."""
import unittest
import numpy as np
from models.eft_audit_v090 import *
class GaugeTests(unittest.TestCase):
    def setUp(self):
        self.k1,self.k2=null_momenta(np.pi/3,2.)
        self.p1,self.p2=physical_polarizations(np.pi/3)
    def test_null_k1(self):self.assertAlmostEqual(dot(self.k1,self.k1),0)
    def test_null_k2(self):self.assertAlmostEqual(dot(self.k2,self.k2),0)
    def test_ward_first(self):self.assertLess(np.linalg.norm(ward_residuals(self.k1,self.k2)[0]),1e-12)
    def test_ward_second(self):self.assertLess(np.linalg.norm(ward_residuals(self.k1,self.k2)[1]),1e-12)
    def test_ward_off_shell(self):
        k=np.array([2.,1.,3.,4.]);p=np.array([4.,2.,1.,-.3])
        a,b=ward_residuals(k,p)
        self.assertTrue(np.allclose(a,0,atol=1e-12))
        self.assertTrue(np.allclose(b,0,atol=1e-12))
    def test_symbolic_ward(self):
        o=sympy_ward_identity()
        self.assertEqual(o['left'],[0]*4)
        self.assertEqual(o['right'],[0]*4)
    def test_polarization_transverse_first(self):
        for e in self.p1:self.assertAlmostEqual(dot(self.k1,e),0)
    def test_polarization_transverse_second(self):
        for e in self.p2:self.assertAlmostEqual(dot(self.k2,e),0)
    def test_gauge_shift_both(self):
        self.assertAlmostEqual(gauge_shift_invariance(self.k1,self.k2,self.p1[0],self.p2[0]),0,places=12)
    def test_gauge_shift_random(self):
        rng=np.random.default_rng(42)
        for _ in range(40):
            a,b=rng.uniform(-2,2,size=2)
            self.assertAlmostEqual(gauge_shift_invariance(self.k1,self.k2,self.p1[1],self.p2[0],a,b),0,places=10)
    def test_boost_minkowski(self):
        B=boost_z(.41)
        self.assertTrue(np.allclose(B.T@METRIC@B,METRIC))
    def test_boost_amplitude(self):
        B=boost_z(.41)
        self.assertAlmostEqual(amplitude(self.k1,self.k2,self.p1[0],self.p2[0]),
            amplitude(B@self.k1,B@self.k2,B@self.p1[0],B@self.p2[0]))
    def test_zero_coupling_zero_vertex(self):
        self.assertEqual(amplitude(self.k1,self.k2,self.p1[0],self.p2[0],c=0),0)
    def test_cutoff_scaling(self):
        a=amplitude(self.k1,self.k2,self.p1[0],self.p2[0],cutoff=10)
        b=amplitude(self.k1,self.k2,self.p1[0],self.p2[0],cutoff=20)
        self.assertAlmostEqual(a/b,4)
    def test_bad_cutoff(self):
        with self.assertRaises(ValueError):amplitude(self.k1,self.k2,self.p1[0],self.p2[0],cutoff=0)
    def test_bad_vertex(self):
        with self.assertRaises(ValueError):vertex([1,2],self.k2)
    def test_bad_dot(self):
        with self.assertRaises(ValueError):dot([1],self.k2)
    def test_invalid_energy(self):
        with self.assertRaises(ValueError):null_momenta(.2,0)
class EFTTests(unittest.TestCase):
    def test_operator_dimension(self):self.assertEqual(operator_dimensions()['operator_dim'],6)
    def test_coupling_dimension(self):self.assertEqual(operator_dimensions()['coupling_dim'],-2)
    def test_global_phase_invariant(self):self.assertLess(global_charge_invariance(1+2j,.867),1e-12)
    def test_global_phase_random(self):
        for p in np.linspace(-8,8,20):self.assertLess(global_charge_invariance(.3+1.4j,p),1e-12)
    def test_noether_current(self):self.assertAlmostEqual(noether_current_plane_wave(1+2j,3),30)
    def test_const_Z(self):self.assertAlmostEqual(kinetic_coefficient(1,.2,10),.992)
    def test_zero_condensate_Z_one(self):self.assertEqual(kinetic_coefficient(1,0,10),1)
    def test_constant_background_lightcone(self):self.assertAlmostEqual(eom_const_background_dispersion(2,[0,0,2]),0)
    def test_bad_kinetic_sign(self):
        with self.assertRaises(ValueError):eom_const_background_dispersion(1,[0,0,1],1,1,1)
    def test_bad_modulus(self):
        with self.assertRaises(ValueError):kinetic_coefficient(1,-1,10)
    def test_wilson_reparam(self):self.assertAlmostEqual(wilson_parameter(1,10),wilson_parameter(4,20))
    def test_wilson_bad_cutoff(self):
        with self.assertRaises(ValueError):wilson_parameter(1,0)
    def test_fisher_rank_one(self):self.assertEqual(np.linalg.matrix_rank(fisher_c_cutoff(1,10)),1)
    def test_fisher_null_direction(self):
        f=fisher_c_cutoff(1,10)
        self.assertTrue(np.allclose(f@np.array([.2,1.]),0))
    def test_offshell_tensor_contraction(self):
        k1=np.array([4.,1.,2.,1.]);k2=np.array([2.,.5,1.,-2.])
        self.assertAlmostEqual(unpolarized_tensor_norm(k1,k2),tensor_norm_identity(k1,k2))
    def test_onshell_tensor_contraction(self):
        k1,k2=null_momenta(.8,2)
        self.assertAlmostEqual(unpolarized_tensor_norm(k1,k2),2*dot(k1,k2)**2)
    def test_collinear_zero(self):
        k1,k2=null_momenta(0,2)
        p1,p2=physical_polarizations(0)
        self.assertAlmostEqual(amplitude(k1,k2,p1[0],p2[0]),0)
    def test_antiparallel_positive(self):
        k1,k2=null_momenta(np.pi,2)
        self.assertGreater(dot(k1,k2),0)
    def test_polarization_sum(self):
        for angle in [.1,.5,1.,2.,3.]:
            k1,k2=null_momenta(angle,1.7)
            e1,e2=physical_polarizations(angle)
            s=sum(amplitude(k1,k2,a,b,c=2,cutoff=7)**2 for a in e1 for b in e2)
            self.assertAlmostEqual(s,(4*2/49)**2*2*dot(k1,k2)**2,places=10)
    def test_summary(self):
        d=summary()
        self.assertEqual(d['version'],'v0.90')
        self.assertFalse(d['novel_identity_prediction'])
    def test_tensor_symmetric_exchange(self):
        k1,k2=null_momenta(.9)
        self.assertTrue(np.allclose(vertex(k1,k2),vertex(k2,k1).T))
if __name__=='__main__':unittest.main()
