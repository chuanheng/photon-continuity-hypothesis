import unittest
from .model import run

class PublishedControls(unittest.TestCase):
    @classmethod
    def setUpClass(cls):cls.r=run()

    def test_threshold(self):
        self.assertAlmostEqual(self.r['v6.72'][0]['ideal_upper_keV'],47.791)
        self.assertAlmostEqual(self.r['v6.72'][-1]['ideal_upper_keV'],46.612)

    def test_groups(self):
        r=self.r['v6.73']
        self.assertEqual(r['total_hours'],2760)
        self.assertAlmostEqual(sum(r['weights']),1)
        residual=sum((w-.25)*a for w,a in zip(r['weights'],r['achieving_multipliers']))
        self.assertAlmostEqual(residual,r['equal_weight_max_abs_bias'])

    def test_mirror(self):
        self.assertAlmostEqual(self.r['v6.74'][1]['inverse_gain'],1/.7)
        self.assertEqual(self.r['v6.74'][-1]['output'],[.5,.5])

    def test_scale(self):
        r=self.r['v6.75']
        self.assertEqual(r['common_cov_rank'],1)
        self.assertLess(r['weighted_relative_independent'],.05)
        self.assertAlmostEqual(r['weighted_relative_common'],.09)

    def test_edge(self):
        r=self.r['v6.76']
        self.assertLess(r['above'],r['below']/1000)
        self.assertAlmostEqual(r['nominal'],r['rows'][0]['transmission'],5)

    def test_lines(self):
        a,_,b=self.r['v6.77'];self.assertGreater(b['other_acceptance'],a['other_acceptance'])
        self.assertGreater(b['gram_condition'],7)

    def test_raster(self):
        for f in self.r['v6.78'].values():
            for p in f['points']:
                self.assertLess(p['lower_plotted_error_endpoint'],p['cross_section'])
                self.assertGreater(p['upper_plotted_error_endpoint'],p['cross_section'])
            self.assertGreater(f['three_pixel_relative_up'],.04)

    def test_aperture(self):
        r=self.r['v6.79'];self.assertAlmostEqual(r['analytic'],r['unit_transmission_integral'])
        self.assertLess(r['ratio_to_unweighted'],.72)

    def test_unfold(self):
        r=self.r['v6.80']
        self.assertEqual(r['energy_marginal_max_diff']+r['time_marginal_max_diff'],0)
        self.assertEqual(r['first_bin_prompt_fractions'],[.6,.2])

    def test_shared_response(self):
        design = self.r['v6.81']
        self.assertEqual(design['response_rank'], 1)
        self.assertEqual(design['profiled_scale_residual'], 0.)
        self.assertGreater(design['known_scale_column_norm'], 0.)
