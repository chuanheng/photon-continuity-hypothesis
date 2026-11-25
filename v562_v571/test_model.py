import unittest

from . import model


class IndependentControlTests(unittest.TestCase):
    def test_controlled_paths(self):
        r=model.controlled_paths()
        self.assertAlmostEqual(r['single_setting_gap'],0)
        self.assertGreater(r['smallest_singular_value'],.85)
        self.assertAlmostEqual(r['recovered_components'][0][0],.13)
        self.assertAlmostEqual(r['ordinary_two_path_refit'],0)

    def test_auxiliary_port(self):
        r=model.auxiliary_port()
        for value in r['without_selective_reset']:
            self.assertAlmostEqual(value,1)
        self.assertAlmostEqual(r['with_reset_on_first_memory'][0],0)
        self.assertAlmostEqual(r['with_reset_on_first_memory'][1],1)
        self.assertEqual(r['with_common_reset'],[0,0])

    def test_mode_leakage(self):
        r=model.mode_leakage()
        self.assertAlmostEqual(r['full_window_coincidence'],.1679)
        self.assertAlmostEqual(r['main_window_only_coincidence'],.095)

    def test_block_randomization(self):
        r=model.blocked_randomization()
        self.assertEqual(r['assignments'],256)
        self.assertAlmostEqual(r['observed_pvalue'],.015625)
        self.assertLessEqual(r['exact_null_rejection_fraction'],.05)
        self.assertLess(r['invariance_to_additive_drift'],1e-13)

    def test_joint_intervention(self):
        r=model.intervention_rank()
        self.assertEqual(r['rank_all'],3)
        self.assertAlmostEqual(r['two_control_alternative_gap'],0)
        self.assertAlmostEqual(r['third_control_alternative_gap'],.04)

    def test_stratum_power(self):
        r=model.stratum_power()
        self.assertLessEqual(r['null_size'],.05)
        self.assertGreater(r['powers'][0],.99)
        self.assertLess(r['worst_condition_power'],.12)

    def test_dictionary_certificate(self):
        r=model.dictionary_certificate()
        self.assertGreater(r['lower_distance'],.20)
        self.assertAlmostEqual(r['lower_distance'],r['matching_upper_distance'])
        self.assertAlmostEqual(r['uncalibrated_extra_mode_refit'],0)

    def test_identified_set(self):
        r=model.identified_interval()
        self.assertAlmostEqual(r['endpoint_predictors'][0],.29)
        self.assertAlmostEqual(r['endpoint_predictors'][1],.31)
        lo,hi=r['identified_interval']
        self.assertLess(lo,.23)
        self.assertGreater(hi,.52)

    def test_charge_echo(self):
        r=model.charge_echo()
        self.assertAlmostEqual(r['contrast'],1)
        self.assertLess(r['ordinary_refit_error'],1e-14)

    def test_eligibility(self):
        r=model.eligibility_intersection()
        self.assertAlmostEqual(r['max_calibrated_ordinary_gap'],.01)
        self.assertGreater(r['candidate_margin'],0)
        self.assertAlmostEqual(r['relaxed_ordinary_exact_refit'],0)
