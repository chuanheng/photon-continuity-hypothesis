"""Independent GitHub regression checks for v0.94.
The 52 locally EXECUTED checks belong to the exact downloadable ZIP source.
No GitHub-hosted CI run is claimed.
"""
import unittest
import numpy as np
from dataclasses import replace
from models.mixed_hom_v094 import (
    Config,mixed_hom_overlap,purity,click_probability,output_coincidence,
    two_photon_pair_coincidence,components,coincidence_probability,
    contrast_slope,jacobian,simulate_records,estimate_records,
    parametric_bootstrap,ordinary_identity_equivalence
)

class MixedStateTests(unittest.TestCase):
    def test_identical_pure(self):self.assertAlmostEqual(mixed_hom_overlap(np.diag([1,0]),np.diag([1,0])),1)
    def test_orthogonal(self):self.assertEqual(mixed_hom_overlap(np.diag([1,0]),np.diag([0,1])),0)
    def test_purity_half(self):self.assertAlmostEqual(purity(np.eye(2)/2),.5)
    def test_two_different_mixed(self):self.assertAlmostEqual(mixed_hom_overlap(np.diag([.8,.2]),np.diag([.3,.7])),.38)
    def test_negative_eigenvalue(self):
        with self.assertRaises(ValueError):mixed_hom_overlap(np.diag([1.2,-.2]),np.eye(2)/2)
    def test_identity_reparameterized(self):
        x=ordinary_identity_equivalence(.9,.8)
        self.assertAlmostEqual(x['claimed_effective_overlap'],x['ordinary_mixed_state_overlap'])

class ThresholdTests(unittest.TestCase):
    def setUp(self):self.p=Config()
    def test_w00(self):self.assertAlmostEqual(self.p.w00,.02)
    def test_invalid_weights(self):
        with self.assertRaises(ValueError):replace(self.p,w11=.99).validate()
    def test_zero_photon_dark(self):self.assertAlmostEqual(click_probability(0,.8,.003),.003)
    def test_single_photon_loss(self):self.assertAlmostEqual(click_probability(1,.74,.002),.74052)
    def test_double_photon_click_more(self):self.assertGreater(click_probability(2,.74,.002),click_probability(1,.74,.002))
    def test_invalid_photon_number(self):
        with self.assertRaises(ValueError):click_probability(4,.8,.01)
    def test_hom_ideal_overlap(self):
        p=Config(eta_a=1,eta_b=1,dark_a=0,dark_b=0)
        self.assertAlmostEqual(two_photon_pair_coincidence(.72,p),.14)
    def test_same_input_two_photons(self):
        p=Config(eta_a=1,eta_b=1,dark_a=0,dark_b=0)
        self.assertAlmostEqual(components(.5,p)[1],.5)
    def test_vacuum_double_dark(self):self.assertAlmostEqual(output_coincidence(0,0,self.p),.000006)
    def test_near_vs_far(self):self.assertLess(coincidence_probability(self.p),coincidence_probability(self.p,True))
    def test_slope(self):
        a=coincidence_probability(replace(self.p,overlap=.1))
        b=coincidence_probability(replace(self.p,overlap=.9))
        self.assertAlmostEqual(a-b,.8*contrast_slope(self.p))
    def test_detector_zero_efficiency(self):
        p=replace(self.p,eta_a=0,eta_b=0)
        self.assertAlmostEqual(coincidence_probability(p),coincidence_probability(p,True))

class IdentifiabilityTests(unittest.TestCase):
    def setUp(self):self.p=Config()
    def test_one_setting_rank(self):self.assertEqual(np.linalg.matrix_rank(jacobian(self.p)),1)
    def test_two_settings_rank(self):self.assertEqual(np.linalg.matrix_rank(jacobian(self.p,True)),2)
    def test_far_no_overlap_derivative(self):self.assertAlmostEqual(jacobian(self.p,True)[1,1],0,places=8)
    def test_ideal_inversion(self):
        p=self.p
        self.assertAlmostEqual((coincidence_probability(p,True)-coincidence_probability(p))/contrast_slope(p),p.overlap)
    def test_parametric_source_calibration(self):
        records=simulate_records(self.p,seed=9401)
        fit=estimate_records(records)
        self.assertLess(abs(fit['overlap']-.72),.06)
        self.assertLess(abs(fit['w11_from_source_cal']-.90),.025)
    def test_reproducible_record(self):
        self.assertEqual(simulate_records(self.p,seed=100),simulate_records(self.p,seed=100))
    def test_bootstrap_refits(self):
        r=simulate_records(self.p,seed=9401)
        b=parametric_bootstrap(r,replications=30,seed=88)
        self.assertEqual(b['bootstrap_count'],30)
        self.assertTrue(b['refitted_calibrations_each_replication'])
        self.assertGreater(b['bootstrap_overlap_sd'],0)
    def test_invalid_bootstrap(self):
        with self.assertRaises(ValueError):parametric_bootstrap(simulate_records(self.p),replications=3)

if __name__=="__main__":unittest.main()
