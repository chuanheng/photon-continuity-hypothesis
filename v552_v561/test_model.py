import unittest

from . import model


class ProvenanceTests(unittest.TestCase):
    def test_bosonic_storage(self):
        r=model.bosonic_storage()
        self.assertLess(r['probability_error'],1e-14)
        self.assertAlmostEqual(r['final_material_two_probability'],1)
        self.assertAlmostEqual(r['final_optical_number'],0)
        for charge in r['charge_expectation']:
            self.assertAlmostEqual(charge,2)

    def test_exchange_counts(self):
        r=model.exchange_counts()
        self.assertAlmostEqual(r['normalization'],1)
        self.assertAlmostEqual(r['same_port_and_coincidence'][1],r['coincidence_formula'])
        self.assertAlmostEqual(r['coincidence_formula'],.255)
        self.assertAlmostEqual(r['changed_by_input_marker_swap'],0)

    def test_path_marker(self):
        r=model.path_marker()
        self.assertAlmostEqual(r['optical_visibility'],.55)
        self.assertAlmostEqual(r['squared_sum'],1)

    def test_marker_gauge(self):
        r=model.marker_gauge()
        self.assertAlmostEqual(r['all_path_coherence_channel_gap'],0)
        self.assertAlmostEqual(r['independently_fixed_marker_probe_gap'],1)

    def test_conditional_interference(self):
        r=model.conditional_interference()
        self.assertAlmostEqual(r['plus_fringe_span'],1)
        self.assertAlmostEqual(r['minus_fringe_span'],1)
        self.assertAlmostEqual(r['unconditioned_span'],0)
        self.assertAlmostEqual(r['unconditioned_output_probability'],.5)

    def test_source_transition(self):
        r=model.source_transition()
        self.assertAlmostEqual(r['end_only_refit_error'],0)
        self.assertAlmostEqual(r['independently_probed_intermediate_gap'],.3)
        first,second=r['final_transition']
        self.assertAlmostEqual(first[0]+second[0],1)
        self.assertAlmostEqual(first[1]+second[1],1)

    def test_simultaneous_separation(self):
        r=model.simultaneous_separation()
        self.assertGreater(r['family_separation_lower'],.034)
        self.assertLess(r['per_condition_separation_lower'][0],0)

    def test_source_contamination(self):
        r=model.source_contamination()
        self.assertLess(r['certified_fraction'],r['contamination_threshold'])
        self.assertGreater(r['weak_fraction'],r['contamination_threshold'])
        self.assertGreater(r['tight_margin'],0)
        self.assertLess(r['weak_margin'],0)

    def test_zero_event_coupling(self):
        r=model.zero_event_coupling()
        self.assertAlmostEqual(r['worst_case_upper'],r['numerical_upper'])
        self.assertAlmostEqual(r['envelope_zero_probability'],.025)
        self.assertGreater(r['zero_probability_at_nominal_using_lower'],.10)
        self.assertAlmostEqual(r['joint_error_budget'],.05)

    def test_heldout_audit(self):
        r=model.heldout_audit()
        self.assertGreater(r['ordinary_interval_separation'][0],.04)
        self.assertTrue(all(x>0 for x in r['candidate_compatibility_margin']))
        self.assertAlmostEqual(r['relaxed_ordinary_refit_residual'],0)
