import unittest
from functions import CSTRSimulator

class TestOptimizeTemperature(unittest.TestCase):
    def test_optimize_temperature(self):
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
        optimal_temp = sim.optimize_temperature(bounds=(300, 500))

        self.assertIsInstance(optimal_temp, float)
        self.assertGreaterEqual(optimal_temp, 300)
        self.assertLessEqual(optimal_temp, 500)

if __name__ == '__main__':
    unittest.main()