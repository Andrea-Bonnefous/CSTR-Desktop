import unittest
from functions import CSTRSimulator

class TestVerifyMassBalance(unittest.TestCase):
    def test_mass_balance_adjustment(self):
        sim = CSTRSimulator()


        inlet = {"A": 1.0, "B": 0.0}
        

        outlet = {"A": 0.5, "B": 0.7}
        

        sim._verify_mass_balance(inlet, outlet, reaction={})

        total_in = sum(inlet.values())
        total_out = sum(outlet.values())


        self.assertAlmostEqual(total_in, total_out, delta=total_in * 0.01)

if __name__ == '__main__':
    unittest.main()