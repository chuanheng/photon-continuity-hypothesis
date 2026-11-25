import unittest
import numpy as np
from v632_v641 import model

class EventAudit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.results=model.run()

    def test_angles(self):
        r=self.results['v6.32']
        self.assertGreater(r['step_angles_range_deg'][0],3.)
        self.assertLessEqual(r['largest_exit_angle'],3.)

    def test_free(self):
        r=self.results['v6.33']
        self.assertAlmostEqual(r['free_max_3deg'],.009653,5)
        self.assertGreater(r['n_single'],0)

    def test_replay(self):
        r=self.results['v6.34']
        self.assertEqual([r[k] for k in ['replay_forward_difference','replay_line_difference','replay_selected_difference']],[0,0,0])
        self.assertLess(r['ci'][0],r['combined_rate'])

    def test_tracks(self):
        r=self.results['v6.35']
        self.assertGreaterEqual(r['tracks_selected'],r['events_with_any_selected'])
        self.assertEqual(r['tracks_selected'],sum(self.results['v6.34']['counts'])+r['secondary_selected'])

    def test_precision(self):
        r=self.results['v6.36']
        self.assertGreater(r['incident_at_pilot_lower'],r['incident_for_10pct_relative_se'])

    def test_alternation(self):
        r=self.results['v6.37']
        self.assertAlmostEqual(r['linear_bias'],0.,18)
        self.assertAlmostEqual(r['quadratic_bias'],-2e-6*model.TRANSMISSION,18)

    def test_simultaneous(self):
        r=self.results['v6.38']
        self.assertAlmostEqual(r['simultaneous_intervals'][0][1],-np.expm1(np.log(.05/6)/2700000),15)

    def test_geometry(self):
        rows=self.results['v6.39']
        self.assertGreater(rows[1]['rate'],rows[0]['rate'])
        self.assertGreater(rows[2]['rate'],rows[0]['rate'])

    def test_width(self):
        lo,hi=self.results['v6.40']['conditional_range']
        self.assertLess(lo,2.94e-5)
        self.assertGreater(hi,2.94e-5)

    def test_projection(self):
        r=self.results['v6.41']
        self.assertLess(r['shared_template_residual'],1e-12)
        self.assertGreater(r['linear_thickness_residual'],.01)
