import unittest
from functions import CSTRSimulator

class TestRunSimulation(unittest.TestCase):
    def test_run_simulation(self):
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
        results = sim.run_simulation(optimize_temp=True, temp_bounds=(300, 500))

        self.assertIsInstance(results, dict)
        self.assertIn("temperature", results)
        self.assertIn("concentrations", results)
        self.assertIn("yield", results)
        self.assertIn("reaction_rates", results)
        self.assertIn("mass_balance_error", results)

if __name__ == '__main__':
    unittest.main()