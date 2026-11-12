import math,pathlib,sys,unittest
sys.path.insert(0,str(pathlib.Path(__file__).resolve().parents[1]/'models'))
from relativistic_successor import *
class Tests(unittest.TestCase):
    def test_threshold(self): self.assertAlmostEqual(threshold_incident_ev(),IONIZATION_EV,delta=.001)
    def test_below(self): self.assertFalse(allowed(10,0,0))
    def test_above(self): self.assertTrue(allowed(20,2,0))
    def test_too_large(self): self.assertFalse(allowed(20,7,0))
    def test_angle_bound(self): self.assertLess(max_successor_ev(20,math.pi),max_successor_ev(20,0))
    def test_max_positive(self): self.assertGreater(max_successor_ev(20,0),0)
    def test_max_below(self): self.assertEqual(max_successor_ev(10,0),0)
    def test_zero_successor(self): self.assertTrue(allowed(20,0,math.pi))
    def test_negative_successor(self):
        with self.assertRaises(ValueError): allowed(20,-1,0)
    def test_negative_incident(self):
        with self.assertRaises(ValueError): max_successor_ev(-1,0)
    def test_bad_angle(self):
        with self.assertRaises(ValueError): max_successor_ev(20,4)
    def test_nan(self):
        with self.assertRaises(ValueError): invariant_ep_sq(float('nan'),1,0)
    def test_invalid_cm(self):
        with self.assertRaises(ValueError): final_pair_four_vectors(20,2,0,2)
    def test_forbidden_reconstruction(self):
        with self.assertRaises(ValueError): final_pair_four_vectors(20,8,0)
    def test_invariant_successor(self): self.assertLess(invariant_ep_sq(20,2,0),invariant_ep_sq(20,1,0))
    def test_invariant_angle(self): self.assertLess(invariant_ep_sq(20,2,math.pi),invariant_ep_sq(20,2,0))
    def test_forward(self): self.check(20,2,0,0,0)
    def test_oblique(self): self.check(40,3,math.pi/3,.4,1.2)
    def test_backward(self): self.check(50,5,math.pi,-.5,2)
    def test_on_shell(self):
        e,p,k=final_pair_four_vectors(40,3,.4,.3,1)
        for v,m in ((e,ELECTRON_MASS_EV),(p,PROTON_MASS_EV)):
            self.assertAlmostEqual(v[0]**2-sum(x*x for x in v[1:]),m*m,delta=1024)
    def check(self,E,eps,theta,mu,phi):
        e,p,k=final_pair_four_vectors(E,eps,theta,mu,phi)
        initial=(HYDROGEN_MASS_EV+E,0,0,E)
        for j in range(4): self.assertAlmostEqual(e[j]+p[j]+k[j],initial[j],delta=2e-5)
if __name__=='__main__': unittest.main()
