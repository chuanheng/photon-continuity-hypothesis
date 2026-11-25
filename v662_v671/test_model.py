import unittest
import numpy as np
from .model import run

class MaterialControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_markers(self):
        for f in self.r['v6.62']:
            self.assertLess(abs(f['marker_minus_complement_keV']),.1)
        self.assertGreater(self.r['v6.62'][0]['marker_keV']-self.r['v6.62'][1]['marker_keV'],1)

    def test_kinematics(self):
        v=self.r['v6.63'];self.assertEqual(v['free'][2]['backscatter_degeneracy_error'],0)
        for f in v['free']:
            self.assertGreaterEqual(f['sample_range'][0],f['double_support_keV'][0]-1e-12)
            self.assertLessEqual(f['sample_range'][1],f['double_support_keV'][1]+1e-12)
        self.assertGreater(np.ptp(v['conditional_doppler_keV']),4.)

    def test_material(self):
        a,_,g,equal=self.r['v6.64']
        self.assertGreater(g['photo_fraction'],a['photo_fraction'])
        self.assertAlmostEqual(a['areal_density'],equal['areal_density'])
        self.assertGreater(a['first_compton'],equal['first_compton'])

    def test_escape(self):
        for row in self.r['v6.65']:
            self.assertAlmostEqual(row['analytic'],row['escape_probability'])
            self.assertAlmostEqual(row['analytic']/2,row['external_half_energy'])

    def test_fluorescence(self):
        a,_,b=self.r['v6.66']
        self.assertEqual(a['alpha_over_continuum'],1.)
        self.assertLess(b['alpha_over_continuum'],b['beta_over_continuum'])
        self.assertLess(b['beta_over_continuum'],.28)

    def test_depth(self):
        v=self.r['v6.67']
        self.assertGreater(v['external_tag'],v['science_tag'])
        self.assertLess(v['reversed_science'],v['science_tag'])

    def test_prompt(self):
        v=self.r['v6.68']
        np.testing.assert_allclose(v['recovered'],[.7,1.8,2.5])
        self.assertAlmostEqual(v['heldout_residual'],.4)

    def test_transfer(self):
        v=self.r['v6.69'];lo,hi=v['missing_third_stratum_interval']
        self.assertAlmostEqual(hi-lo,.45)
        self.assertAlmostEqual(v['science'],.55)

    def test_full_joint(self):
        v=self.r['v6.70']
        self.assertAlmostEqual(v['record_sum'],1.)
        self.assertLess(v['joint_record_max_error'],1e-14)
        self.assertGreater(v['ordinary_phase_drift_error'],.001)

    def test_detuning(self):
        v=self.r['v6.71']
        self.assertEqual(v['max_error'],0)
        self.assertGreater(v['max_complex_distance_if_detuning_fixed'],.8)
