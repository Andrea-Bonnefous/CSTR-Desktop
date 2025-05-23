import unittest
from functions import CSTRSimulator

class TestCalculateYield(unittest.TestCase):
    def test_calculate_yield(self):
        sim = CSTRSimulator()
        sim.set_parameters(
            volume=1.0,
            temperature=350.0,
            flow_rate=0.01,
            reactions=[
                {
                    "frequency_factor": 1e10,
                    "activation_energy": 80000.0,
                    "reaction_order": {"A": 1},
                    "stoichiometry": {"A": -1, "B": 1},
                    "reversible": False
                }
            ],
            feed_composition={"A": 1.0},
            recycle_ratio=0.0,
            target_product="B"
        )
        sim.components = ["A", "B"]
        sim.concentrations = {"A": 0.4, "B": 0.6}

        yield_val = sim.calculate_yield()

        self.assertIsInstance(yield_val, float)
        self.assertGreaterEqual(yield_val, 0.0)
        self.assertLessEqual(yield_val, 1.0)

if __name__ == '__main__':
    unittest.main()