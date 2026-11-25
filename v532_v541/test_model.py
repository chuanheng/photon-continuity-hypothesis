import unittest

from . import model


class ChannelWitnessTests(unittest.TestCase):
    def test_damping_threshold(self):
        report = model.damping_threshold()
        self.assertGreater(min(report['choi_minimum_eigenvalues']), 0)
        self.assertGreater(report['partial_transpose_minima'][0], 0)
        self.assertLess(report['partial_transpose_minima'][1], 0)
        self.assertAlmostEqual(report['coherence_threshold'], .6260990337)

    def test_bell_correlations(self):
        report = model.bell_correlations()
        self.assertAlmostEqual(report['overlap_from_settings'], report['direct_overlap'])
        self.assertAlmostEqual(report['overlap_from_settings'], .76)
        self.assertAlmostEqual(report['dephased_overlap'], .42)
        self.assertAlmostEqual(report['omitted_axis_overlap_difference'], .25)
        self.assertAlmostEqual(report['common_population_error'], 0)

    def test_two_basis_benchmark(self):
        report = model.two_basis_benchmark()
        self.assertAlmostEqual(report['classical_z_only_score'], 1)
        self.assertAlmostEqual(report['classical_two_basis_score'], .75)
        self.assertAlmostEqual(report['partially_coherent_two_basis_score'], .8)

    def test_misregistered_axes(self):
        report = model.misregistered_axes()
        self.assertAlmostEqual(report['reported_overlap'], 1)
        self.assertAlmostEqual(report['true_overlap'], report['trusted_direct_overlap'])
        self.assertAlmostEqual(report['true_overlap'], .5)
        self.assertEqual(report['independently_measured_axis_gram_rank'], 1)

    def test_reset_residual(self):
        report = model.reset_residual()
        self.assertAlmostEqual(report['leak_power'], .02)
        self.assertAlmostEqual(report['paired_quadrature_gap'], report['predicted_amplitude_gap'])
        self.assertGreater(report['paired_quadrature_gap'], 7*report['naive_power_gap'])

    def test_flagged_erasure(self):
        report = model.flagged_erasure()
        self.assertAlmostEqual(report['flagged_trace'], 1)
        self.assertAlmostEqual(report['success_conditioned_overlap'], 1)
        self.assertAlmostEqual(report['flagged_pt_minimum'], -.1)
        self.assertAlmostEqual(report['fallback_pt_minimum'], .1)
        self.assertAlmostEqual(report['fallback_overlap'], .4)

    def test_phase_probe(self):
        report = model.phase_probe()
        self.assertAlmostEqual(report['old_menu_gap'], 0)
        self.assertAlmostEqual(report['new_quadrature_gap'], 2*report['full_output_trace_distance'])
        self.assertGreater(report['new_quadrature_gap'], .72)

    def test_environment_reference(self):
        report = model.environment_reference()
        self.assertAlmostEqual(report['output_trace_norm_difference'], 0)
        self.assertAlmostEqual(*report['population_only_environment_z'])
        self.assertAlmostEqual(report['conjugated_measurement_gap'], 0)
        self.assertGreater(report['calibrated_environment_x'][0]-report['calibrated_environment_x'][1], .65)

    def test_environment_interventions(self):
        report = model.environment_interventions()
        self.assertAlmostEqual(report['coherent_system_x'][0], 1)
        self.assertAlmostEqual(report['coherent_system_x'][1], -1)
        self.assertEqual(report['incoherent_system_x'], [0,0])
        self.assertAlmostEqual(report['initial_local_population_gap'], 0)

    def test_instrument_relabeling(self):
        report = model.instrument_relabeling()
        self.assertEqual(report['record_count'], 36)
        self.assertAlmostEqual(report['largest_normalization_error'], 0)
        self.assertAlmostEqual(report['largest_record_gap'], 0)
        self.assertGreater(report['fixed_hidden_reference_gap'], .89)
