import unittest
from models.atomic_selection_rules import multipole_allowed as allowed

class SelectionRuleTests(unittest.TestCase):
    def test_e1_opposite_parity(self): self.assertTrue(allowed(0,2,1,-1,'E1'))
    def test_e1_same_parity_forbidden(self): self.assertFalse(allowed(0,2,1,1,'E1'))
    def test_e1_zero_to_zero_forbidden(self): self.assertFalse(allowed(0,0,1,-1,'E1'))
    def test_m1_same_parity(self): self.assertTrue(allowed(2,2,1,1,'M1'))
    def test_m1_opposite_parity_forbidden(self): self.assertFalse(allowed(2,2,1,-1,'M1'))
    def test_e2_same_parity(self): self.assertTrue(allowed(0,4,1,1,'E2'))
    def test_e2_zero_to_zero_forbidden(self): self.assertFalse(allowed(0,0,1,1,'E2'))
    def test_triangle_forbidden(self): self.assertFalse(allowed(0,4,1,-1,'E1'))
    def test_half_integer(self): self.assertTrue(allowed(1,3,1,-1,'E1'))
    def test_mismatched_sector(self): self.assertFalse(allowed(1,2,1,-1,'E1'))
    def test_invalid(self):
        with self.assertRaises(ValueError): allowed(-1,2,1,-1,'E1')
        with self.assertRaises(ValueError): allowed(0,2,0,-1,'E1')
        with self.assertRaises(ValueError): allowed(0,2,1,-1,'E3')

if __name__ == '__main__': unittest.main()
