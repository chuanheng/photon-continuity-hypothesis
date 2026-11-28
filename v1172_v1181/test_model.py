import unittest
import numpy as np
from .model import run, count_probabilities


class AnalyzerTests(unittest.TestCase):
    def test_orbit(self):
        r=run()['orbit']
        self.assertAlmostEqual(r['double_max'],(2+np.sqrt(3))/4)
        self.assertAlmostEqual(r['split_max'],.75)

    def test_balanced(self):
        a,b=np.array(run()['balanced'])
        np.testing.assert_allclose(a,b[::-1])
        self.assertGreater(abs(a[0]-b[0]),.1)
        self.assertAlmostEqual(a.sum(),1.)

    def test_phase_refit(self):
        self.assertLess(run()['phase_refit'],1e-13)

    def test_harmonic(self):
        self.assertLess(run()['second_harmonic'][2],1e-13)
        phase=np.pi*np.arange(8)/4
        signal=[count_probabilities([1/np.sqrt(2),0,1/np.sqrt(2)],np.pi/4,p)[0] for p in phase]
        self.assertAlmostEqual(np.mean(signal*np.exp(-2j*phase)).real,1/8)

    def test_balanced_rank(self):
        self.assertEqual(run()['balanced_rank'],5)

    def test_tomography(self):
        rank,holdout,state_error=run()['tomography']
        self.assertEqual(rank,9)
        self.assertLess(max(holdout,state_error),1e-13)

    def test_threshold_loss(self):
        click,both,inferred=run()['threshold_loss']
        self.assertAlmostEqual(inferred,run()['balanced'][0][0])
        self.assertAlmostEqual(both,.5*.76**2)

    def test_dark_clicks(self):
        noisy,ideal,condition=run()['dark_clicks']
        self.assertAlmostEqual(noisy,ideal+(1-ideal)*.025)
        self.assertGreater(condition,1)

    def test_jitter(self):
        self.assertAlmostEqual(run()['jitter'],np.exp(-2*.35**2))

    def test_reference(self):
        a=.33
        self.assertAlmostEqual(run()['reference'],2*np.sqrt(2)*np.cos(a)**3*np.sin(a))
