"""v1.10 regression tests: execute with python -m unittest discover -s tests -p 'test_three_photon_v110.py'."""
import math,unittest
from models.three_photon_v110 import unitary,output_probabilities,detected_probabilities,coarse,tv,fit_grid
class V110Tests(unittest.TestCase):
    def test_unitarity(self):
        for eps in [0,.08,-.13]:
            u=unitary(eps)
            for i in range(3):
                for j in range(3):
                    z=sum(u[i][k]*u[j][k].conjugate() for k in range(3))
                    self.assertAlmostEqual(z.real,float(i==j),places=12)
                    self.assertAlmostEqual(z.imag,0,places=12)
    def test_normalization(self):
        for eps in [0,.08]:
            for phase in [0,math.pi/3,-math.pi/3,math.pi]:
                p=output_probabilities(.3,phase,eps)
                self.assertAlmostEqual(sum(p.values()),1,places=12)
                self.assertTrue(all(v>=0 for v in p.values()))
                d=detected_probabilities(p,(.86,.82,.9))
                self.assertAlmostEqual(sum(d.values()),1,places=12)
                self.assertEqual(len(d),20)
    def test_classical_limit(self):
        p=output_probabilities(0,0)
        self.assertAlmostEqual(p[(3,0,0)],1/27)
        self.assertAlmostEqual(p[(1,1,1)],2/9)
    def test_symmetric_loss_preserves_coarse_degeneracy(self):
        for eps in [0,.08]:
            p=coarse(detected_probabilities(output_probabilities(.3,math.pi/3,eps),(.85,)*3))
            q=coarse(detected_probabilities(output_probabilities(.3,-math.pi/3,eps),(.85,)*3))
            self.assertLess(tv(p,q),1e-12)
    def test_asymmetric_loss_weakly_breaks_degeneracy(self):
        p=coarse(detected_probabilities(output_probabilities(.3,math.pi/3,.08),(.86,.82,.9)))
        q=coarse(detected_probabilities(output_probabilities(.3,-math.pi/3,.08),(.86,.82,.9)))
        self.assertGreater(tv(p,q),1e-7)
        self.assertLess(tv(p,q),1e-4)
    def test_loss_reduces_full_tv(self):
        p=output_probabilities(.3,math.pi/3,.08)
        q=output_probabilities(.3,-math.pi/3,.08)
        eta=(.86,.82,.9)
        self.assertLess(tv(detected_probabilities(p,eta),detected_probabilities(q,eta)),tv(p,q))
    def test_calibration_mismatch_bias(self):
        eta=(.86,.82,.9)
        actual=detected_probabilities(output_probabilities(.3,math.pi/3,.08),eta)
        grid=[math.pi/3+.002*i for i in range(-80,81)]
        true=fit_grid(actual,.3,grid,.08,eta)
        wrong=fit_grid(actual,.27,grid,.08,eta)
        self.assertAlmostEqual(true[0],math.pi/3,places=12)
        self.assertGreater(wrong[0],true[0]+.04)
if __name__=='__main__':unittest.main()
