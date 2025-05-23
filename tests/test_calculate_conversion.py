import unittest
from functions import CSTRSimulator

class TestCalculateConversion(unittest.TestCase):
    def test_calculate_conversion(self):
        sim = CSTRSimulator()
        sim.components = ["A", "B"]
        sim.feed_composition = {"A": 1.0, "B": 2.0}
        sim.concentrations = {"A": 0.4, "B": 1.5}

        conversions = sim.calculate_conversion()

        self.assertIsInstance(conversions, dict)
        self.assertIn("A", conversions)
        self.assertIn("B", conversions)
        self.assertAlmostEqual(conversions["A"], 0.6, places=5)
        self.assertAlmostEqual(conversions["B"], 0.25, places=5)

if __name__ == '__main__':
    unittest.main()