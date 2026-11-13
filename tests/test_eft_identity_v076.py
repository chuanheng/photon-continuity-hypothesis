"""v0.76 reproducible 27 unit tests (numpy required)."""
import unittest
import numpy as np
from models.eft_identity_v076 import *

class FiniteModeTests(unittest.TestCase):
    def test_ladder_shape(self): self.assertEqual(ladder(4).shape,(4,4))
    def test_ladder_entries(self): self.assertAlmostEqual(ladder(4)[1,2].real,np.sqrt(2))
    def test_invalid_dimension(self):
        with self.assertRaises(ValueError):ladder(1)
    def test_hermiticity(self):
        h,_,_=model();self.assertTrue(np.allclose(h,h.conj().T))
    def test_charge_conserved(self):
        h,q,_=model();self.assertLess(np.linalg.norm(commutator(h,q)),1e-12)
    def test_photon_number_not_conserved(self):
        h,_,n=model();self.assertGreater(np.linalg.norm(commutator(h,n)),1e-4)
    def test_decoupled_photon_number(self):
        h,_,n=model(g=0);self.assertLess(np.linalg.norm(commutator(h,n)),1e-12)
    def test_decoupled_charge(self):
        h,q,_=model(g=0);self.assertLess(np.linalg.norm(commutator(h,q)),1e-12)
    def test_unitary_evolution_norm(self):
        h,_,_=model();v=np.zeros(h.shape[0],complex);v[5]=1
        self.assertAlmostEqual(np.linalg.norm(propagate(h,v,1.7)),1)
    def test_carrier_charge_expectation(self):
        h,q,_=model();v=np.zeros(h.shape[0],complex);v[5]=1
        out=propagate(h,v,2.1)
        self.assertAlmostEqual(np.vdot(out,q@out).real,np.vdot(v,q@v).real)
    def test_carrier_sectors_do_not_mix(self):
        h,_,_=model();v=np.zeros(h.shape[0],complex);v[1]=1
        out=propagate(h,v,2)
        self.assertAlmostEqual(sum(abs(out[i])**2 for i in range(1,h.shape[0],3)),1)
    def test_no_carrier_no_interaction(self):
        h,_,_=model();v=np.zeros(h.shape[0],complex);v[3]=1
        out=propagate(h,v,1)
        self.assertAlmostEqual(abs(out[3]),1)

class CovarianceTests(unittest.TestCase):
    def setUp(self):
        self.k=np.array([2.,.2,.3,1.5]);self.e=np.array([.1,.3,-.4,.2])
    def test_antisymmetric(self):
        f=field_strength(self.k,self.e);self.assertTrue(np.allclose(f,-f.T))
    def test_gauge_shift(self):
        f=field_strength(self.k,self.e)
        self.assertTrue(np.allclose(f,field_strength(self.k,self.e+2.34*self.k)))
    def test_f2_lorentz_invariant(self):
        f=field_strength(self.k,self.e)
        for r in [-2,-.7,0,.4,2]:
            l=boost_z(r)
            self.assertAlmostEqual(contract_f_squared(l@f@l.T),contract_f_squared(f),places=9)
    def test_lorentz_metric(self):
        for r in [-1,0,1]:
            l=boost_z(r);self.assertTrue(np.allclose(l.T@ETA@l,ETA))
    def test_f2_gauge_invariant(self):
        a=contract_f_squared(field_strength(self.k,self.e))
        b=contract_f_squared(field_strength(self.k,self.e-3*self.k))
        self.assertAlmostEqual(a,b)
    def test_f_zero_parallel(self):
        self.assertTrue(np.allclose(field_strength(self.k,2*self.k),0))
    def test_bad_vector(self):
        with self.assertRaises(ValueError):field_strength(np.array([1,2]),self.e)
    def test_bad_tensor(self):
        with self.assertRaises(ValueError):contract_f_squared(np.eye(2))

class GlobalChargeTests(unittest.TestCase):
    def test_positive_density(self):self.assertAlmostEqual(noether_density(1+1j,2),8)
    def test_global_phase_invariance(self):
        a=1+.3j
        self.assertAlmostEqual(noether_density(a,1.2),noether_density(a*np.exp(1j*1.4),1.2))
    def test_neutral_operator(self):self.assertEqual(charge_balance('SdagS_F2'),0)
    def test_linear_operator_charged(self):self.assertNotEqual(charge_balance('S_F2'),0)
    def test_operator_dimension(self):self.assertEqual(dimension('SdagS_F2'),6)
    def test_wrong_operator_dimension(self):self.assertEqual(dimension('S_F2'),5)
    def test_summary(self):
        x=summary()
        self.assertAlmostEqual(x['carrier_charge_commutator'],0)
        self.assertGreater(x['photon_number_commutator'],0)
        self.assertAlmostEqual(x['f2'],x['f2_boosted'])
        self.assertEqual(x['operator_dimension'],6)

if __name__=='__main__':unittest.main()
