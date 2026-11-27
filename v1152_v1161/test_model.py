import unittest
from .model import run
class CouplingTests(unittest.TestCase):
    def test_exchange_symmetry(self):
        r=run()['exchange_symmetry']; self.assertGreater(r['slot_commutator'],1); self.assertEqual(r['collective_commutator'],0)
    def test_number_conservation(self):
        r=run()['number_conservation']; self.assertEqual(r['exchange_commutator'],0); self.assertGreater(r['pair_commutator'],1)
