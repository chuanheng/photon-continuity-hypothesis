import unittest
from .model import run

class SuccessWeights(unittest.TestCase):
    def test_arbitrary_weights(self):
        result=run()
        self.assertAlmostEqual(result['minimum'], .909)
        self.assertAlmostEqual(sum(result['minimizing_weights']),1.)
        self.assertGreater(result['low_eff_margin'], .04)
