import unittest
import math
from .model import run

class Benchmark(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r = run()

    def test_v912(self):
        self.assertAlmostEqual(self.r['benchmark'], 0.8010434324627794, delta=1e-12)

    def test_v913(self):
        self.assertAlmostEqual(self.r['nonempty'], 0.14712383373884735, delta=1e-12)

    def test_v914(self):
        self.assertAlmostEqual(self.r['fraction2'], 0.0690367631752921, delta=1e-12)

    def test_v915(self):
        self.assertAlmostEqual(self.r['low_eff'], 0.8071932436028734, delta=1e-12)

    def test_v916(self):
        self.assertAlmostEqual(self.r['ceiling2'], 0.43233235838169365, delta=1e-12)

    def test_v917(self):
        # Integrate t*exp(t-1) on [0,1], then exclude vacuum.
        self.assertAlmostEqual(self.r['flat'], 1 - .5/(math.e-1))
        self.assertAlmostEqual(self.r['selection_gain'], .0920317858974424)

    def test_v918(self):
        self.assertAlmostEqual(self.r['background'], 0.14, delta=1e-12)

    def test_v919(self):
        self.assertAlmostEqual(self.r['channel_fidelity'], 0.93, delta=1e-12)

    def test_v920(self):
        self.assertAlmostEqual(self.r['rank5'], 6, delta=1e-12)

    def test_v921(self):
        self.assertAlmostEqual(self.r['min_eigenvalue'], .5)
        self.assertTrue(.001 < self.r['usd_efficiency'] < .002)
