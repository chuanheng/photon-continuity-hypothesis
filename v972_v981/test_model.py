import unittest
import numpy as np
from numpy.testing import assert_allclose
from .model import B,I,SINGLET,T,accidentals,confusion,run,score,table

class QuantumInputs(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_bell_projection(self):
        assert_allclose(table(SINGLET),(1-T@T.T)/16,atol=1e-14)
        self.assertLess(self.r['tetra']['operator_error'],1e-13)

    def test_separable(self):
        self.assertLess(self.r['product_error'],1e-14)
        u=T[0]
        self.assertAlmostEqual(score(np.outer((1+T@u)/2,(1-T@u)/2)),0)

    def test_loss(self):
        self.assertAlmostEqual(self.r['uniform_loss'],-.093/8)

    def test_renormalization(self):
        self.assertLess(self.r['postselection']['conditional'],0)
        self.assertGreater(self.r['postselection']['raw'],0)

    def test_depolarized_inputs(self):
        p=self.r['noisy_probe']['threshold']
        self.assertAlmostEqual(score(table(p*SINGLET+(1-p)*np.eye(4)/4,.8*T,.7*T)),0)

    def test_rotation(self):
        self.assertAlmostEqual(self.r['rotation']['score'],(1-self.r['rotation']['trace'])/16)

    def test_confusion(self):
        self.assertAlmostEqual(self.r['confusion']['corrected'],-.125)
        self.assertAlmostEqual(self.r['confusion']['amplification'],1/.82**2)

    def test_false_click(self):
        self.assertAlmostEqual(score(accidentals(self.r['dark_threshold'])),0)
        assert_allclose(accidentals(1),1)

    def test_sideband(self):
        a=np.array([1,0,0,0]);b=np.array([0,1,0,0])
        self.assertAlmostEqual(score(.03*np.outer(a,b)),self.r['label_sideband'])

    def test_pair_sampling(self):
        r=self.r['pair_sampling']
        self.assertAlmostEqual(r['uniform_var'],12*16*(1/8)**2*(1/12)-1/64)
        self.assertGreater(r['weighted_var'],r['uniform_var'])
