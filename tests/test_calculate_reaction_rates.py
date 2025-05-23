import unittest
from functions import CSTRSimulator

class TestCalculateReactionRates(unittest.TestCase):
    def test_calculate_reaction_rates(self):
        sim = CSTRSimulator()
        sim.set_parameters(
            volume=1.0,
            temperature=350.0,
            flow_rate=0.01,
            reactions=[
                {
                    "name": "A to B",
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
        sim.concentrations = {"A": 0.5, "B": 0.5}
        rates = sim.calculate_reaction_rates()

        self.assertIsInstance(rates, dict)
        self.assertIn("Reaction 1: A to B", rates)
        self.assertIsInstance(rates["Reaction 1: A to B"], float)

if __name__ == '__main__':
    unittest.main()