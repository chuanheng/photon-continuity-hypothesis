import math
import unittest
import numpy as np
from v922_v931.model import STATES,bounds
from .audit import run,upper

class Audit(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.r=run()

    def test_floor(self):
        self.assertTrue(.899 < self.r['floor'] < .900)

    def test_margin(self):
        self.assertAlmostEqual(upper(.093),bounds(.093)[1])
        self.assertTrue(.019 < self.r['joint_margin'] < .020)

    def test_bias(self):
        self.assertAlmostEqual(self.r['bias_budget'],.909-bounds(.083)[1])

    def test_ratio(self):
        self.assertAlmostEqual(self.r['ratio_floor'],.9233)

    def test_covariance(self):
        self.assertGreater(self.r['common_sd'],self.r['independent_sd'])

    def test_binary(self):
        self.assertTrue(.148 < self.r['phase_gain'] < .150)

    def test_uniform(self):
        self.assertTrue(.035 < self.r['usd'] < .036)

    def test_witness(self):
        self.assertGreater(self.r['best_usd'],.23)

    def test_independent_fock_povm(self):
        # Independent expansion into a physical two-mode number basis.
        amplitudes=STATES*np.exp(1j*np.array(self.r['phases'])[:,None])
        columns=np.array([[np.exp(-.5)*a**k*b**(n-k)/
                          math.sqrt(math.factorial(k)*math.factorial(n-k))
                          for a,b in amplitudes] for n in range(13) for k in range(n+1)])
        dual=np.linalg.pinv(columns)
        effects=.093*dual.conj().T@dual
        table=.093*abs(dual@columns)**2
        self.assertGreater(np.linalg.eigvalsh(np.eye(len(effects))-effects)[0],0)
        np.testing.assert_allclose(table,.093*np.eye(6),atol=1e-13)
