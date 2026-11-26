import unittest
from .instruments import run

class Predictions(unittest.TestCase):
    def test_v893(self):
        self.assertAlmostEqual(run()['resolved_tv'], 1, delta=1e-12)

    def test_v894(self):
        self.assertAlmostEqual(run()['weak_tv'], 0.6, delta=1e-12)

    def test_v895(self):
        self.assertAlmostEqual(run()['reset_cov'], 0, delta=1e-12)

    def test_v896(self):
        self.assertAlmostEqual(run()['telegraph_tv'], 0.5, delta=1e-12)

    def test_v897(self):
        self.assertAlmostEqual(run()['revival'], 1, delta=1e-12)

    def test_v898(self):
        self.assertAlmostEqual(run()['echo_gain'], 0.5, delta=1e-12)

    def test_v899(self):
        self.assertAlmostEqual(run()['readout_tv'], 0.49, delta=1e-12)

    def test_v900(self):
        self.assertAlmostEqual(run()['loss_tv'], 0.4, delta=1e-12)

    def test_v901(self):
        self.assertAlmostEqual(run()['ordinary_error'], 0, delta=1e-12)
