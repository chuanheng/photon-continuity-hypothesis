import unittest

from . import model


class MixedPathTests(unittest.TestCase):
    def test_atomic_change(self):
        r=model.atomic_change()
        self.assertLess(abs(r['first_batch_relative_difference']),.001)
        self.assertGreater(r['relative_change'],.07)
        self.assertLess(r['relative_change'],.09)

    def test_mixed(self):
        r=model.mixed_paths()
        self.assertAlmostEqual(sum(r['rates'].values()),r['combined'])
        self.assertGreater(r['mixed_fraction'],.09)
        self.assertLess(r['mixed_fraction'],.10)

    def test_beam_offset(self):
        r=model.source_offset()
        self.assertGreater(r['rates'][0],r['rates'][1])
        self.assertGreater(r['rates'][1],r['rates'][2])

    def test_uncomputed_paths(self):
        r=model.omitted_bound()
        self.assertLess(r['at_least_three_interactions_bound'],r['all_first_interaction_probability'])
        self.assertGreater(r['bound_over_modeled_two'],10000)

    def test_energy_scan(self):
        r=model.energy_scan()
        self.assertGreater(r['rates'][-1],r['rates'][0])
        self.assertLess(r['max_to_min'],1.1)

    def test_order_difference(self):
        r=model.repeat_integration()
        self.assertGreater(r['ratio_of_mixed_orders'],1.25)
        self.assertLess(max(r['relative_integration_se']),1e-4)

    def test_detector(self):
        r=model.energy_efficiency()
        self.assertGreater(r['weighted_efficiency'],.75)
        self.assertLess(r['weighted_efficiency'],.78)
        self.assertTrue(all(measured<raw for measured,raw in zip(r['detector_folded'],r['raw'])))

    def test_power(self):
        r=model.exposure_budget()
        self.assertGreater(r['powers'][1],.9)
        self.assertLess(r['powers'][2],.09)

    def test_hidden_paths(self):
        r=model.indistinguishable_histories()
        self.assertLess(r['visible_gap'],1e-14)
        self.assertEqual(r['independently_measured_route_gap'],.25)

    def test_readiness(self):
        r=model.readiness()
        self.assertGreater(r['unresolved_budget_ratio'],4000)
        self.assertLess(r['known_selected_two_interaction_rate'],r['illustrative_candidate_increment'])
