import unittest
from scipy.stats import binom
from . import model

class ReferenceTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=model.run()

    def test_deposits(self):
        r=self.r['v6.52']
        self.assertEqual(r['selected'],9)
        self.assertEqual(r['threshold_scan'][1]['foil_sum'],8)
        self.assertLess(r['max_abs_unaccounted_keV'],1e-9)

    def test_timing(self):
        r=self.r['v6.53']
        self.assertAlmostEqual(r['corrected'],.4)
        self.assertLess(abs(r['simulated']-r['observed']),4*r['mc_se'])
        self.assertGreater(r['ignored_accidentals'],.45)

    def test_joint_profile(self):
        r=self.r['v6.54']
        self.assertAlmostEqual(r['calibrated']['delta_interval'][0],2.6)
        self.assertAlmostEqual(r['widened']['delta_interval'][0],0.)
        for s,u,v in r['calibrated']['witnesses']:
            self.assertAlmostEqual(u+v,1.8)
            self.assertLessEqual(v,.25*(5-s)+1e-12)

    def test_calibration(self):
        r=self.r['v6.55']
        self.assertEqual(r['n'],9)
        self.assertLessEqual(r['size'],.025)
        self.assertGreater(r['power'],.9)
        self.assertLess(r['best_smaller'],.9)

    def test_threshold(self):
        r=self.r['v6.56']
        self.assertLessEqual(r['union_failure'],.05)
        self.assertGreater(r['smaller_union_bound'],.05)
        self.assertGreater(r['drifted_tail'],.025)

    def test_spectroscopy(self):
        r=self.r['v6.57']
        self.assertAlmostEqual(r['source_variance'],.36)
        self.assertAlmostEqual(r['common_detector_variance'],.25)
        for w,d,v in zip([.04,1],r['alternative_detector_variances'],r['measured_variances']):
            self.assertAlmostEqual(.16*w/(.16+w)+d,v)

    def test_physics_switch(self):
        r=self.r['v6.58']
        self.assertEqual(r['polarized']['count'],len(model.read('nominal.json')['single_losses']))
        self.assertGreater(r['penelope']['count'],0)
        self.assertTrue(0<=r['empirical_KS']<=1)

    def test_secondary_births(self):
        for row in self.r['v6.59']:
            self.assertGreaterEqual(row['gamma_tracks'],row['birth_events'])
            self.assertGreater(row['one_sided_975_upper'],row['birth_events']/row['incident'])
            self.assertLessEqual(row['selected_secondary'],row['gamma_tracks'])

    def test_geometry(self):
        a,b=self.r['v6.60']
        self.assertLess(a['restricted'],b['restricted'])
        for row in [a,b]:
            lo,hi=row['two_strata_interval']
            self.assertLessEqual(lo,row['events']/row['incident'])
            self.assertGreater(hi,row['events']/row['incident'])

    def test_label_gap(self):
        r=self.r['v6.61']
        self.assertAlmostEqual(sum(r['single_setting']),1.)
        self.assertAlmostEqual(r['distance'],.1/2**.5)
