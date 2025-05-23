import unittest
from functions import CSTRSimulator

class TestCalculateElementalBalance(unittest.TestCase):
    def test_calculate_elemental_balance(self):
        sim = CSTRSimulator()
        sim.feed_composition = {"A": 1.0, "B": 2.0}
        concentrations = {"A": 0.5, "B": 2.5}

        result = sim._calculate_elemental_balance(concentrations)

        self.assertIsInstance(result, dict)
        self.assertIn("total_input_conc", result)
        self.assertIn("total_output_conc", result)
        self.assertIn("difference_percent", result)
        self.assertAlmostEqual(result["total_input_conc"], 3.0, places=5)
        self.assertAlmostEqual(result["total_output_conc"], 3.0, places=5)

if __name__ == '__main__':
    unittest.main()