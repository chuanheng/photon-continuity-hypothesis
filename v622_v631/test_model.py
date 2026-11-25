import json
import unittest
from pathlib import Path
import numpy as np
from scipy.special import ndtr
from v622_v631.bounds import calculate
from v622_v631.paths import chord,score
from v612_v621.model import rate
from scipy.stats import qmc

ROOT=Path(__file__).parent

class TransportChecks(unittest.TestCase):
    def test_chords(self):
        p=np.tile([0.,0.,.025],(3,1))
        np.testing.assert_allclose(chord(p,np.eye(3),.1,.5),[.5,.5,.075])

    def test_bound(self):
        b=calculate()
        self.assertLess(b['selected_order_ge3'],.00016)
        self.assertAlmostEqual(b['selected_order_ge4']/b['selected_order_ge3'],b['continuation'])

    def test_zero_aperture(self):
        w,e=score('CCC',qmc.Sobol(9,seed=622).random_base2(8),angle=0.)
        self.assertEqual(w.sum(),0.)
        self.assertGreater(e.min(),35.)

    def test_independent_paths(self):
        data=json.loads((ROOT/'paths.json').read_text())
        for p in ['CC','CR','RC']:
            self.assertLess(abs(data['2']['paths'][p]/rate(p)-1),.002)
        self.assertEqual(data['3']['paths']['RRR'],0.)
        self.assertTrue(0<data['3']['total']<calculate()['selected_order_ge3'])

    def test_detector(self):
        joint=json.loads((ROOT/'detector.json').read_text())
        a=joint[0]
        self.assertAlmostEqual(a['order_rows'][0][1],np.exp(-2.70*.277810274566*.1)*ndtr(-4),12)
        self.assertEqual(a['order_rows'][1][0],0.)
        self.assertLess(joint[1]['total'][0],a['total'][0])
        self.assertLess(a['total'][0],joint[2]['total'][0])

    def test_rayleigh_conserves_energy(self):
        w,e=score('RRR',qmc.Sobol(9,seed=17).random_base2(9))
        np.testing.assert_equal(e,60.)
        self.assertGreater(w.sum(),0.)

    def test_recoil_floor(self):
        from v612_v621.model import REST
        self.assertGreater(1/(1/60+6/REST),35)
        self.assertLess(1/(1/60+8/REST),35)

    def test_power(self):
        from scipy.stats import poisson
        d=json.loads((ROOT/'inference.json').read_text())
        n=d['exposure']
        self.assertAlmostEqual(poisson.sf(d['critical_count']-1,n*d['power90_total_rate']),.9,7)
        self.assertLessEqual(poisson.sf(d['critical_count']-1,n*d['conditional_total_cap']),.025)

    def test_blank(self):
        d=json.loads((ROOT/'inference.json').read_text())
        self.assertAlmostEqual(d['blank_expected_counts']/2700000,ndtr(-4),14)

    def test_single_scatter(self):
        w,e=score('C',qmc.Sobol(3,seed=23).random_base2(8))
        self.assertGreater(e.min(),59.99)
        self.assertGreater(w.sum(),0.)
