import unittest
from .model import run


class Reachability(unittest.TestCase):
    def test_count_closure(self):
        row = run()['count']
        self.assertEqual(row['rank'], 2)
        self.assertAlmostEqual(row['projection_norm'], 0)
        self.assertEqual(row['probability_plus'], [0.5, 0.5])

    def test_ramsey_witness(self):
        row = run()['ramsey']
        self.assertEqual(row['rank'], 3)
        self.assertEqual(row['probability_plus'], [1., 0.])
