import unittest
from functions import CSTRSimulator

class TestObjectiveFunction(unittest.TestCase):
    def test_objective_function(self):
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
        result = sim.objective_function(temperature=350.0)

        self.assertIsInstance(result, float)
        self.assertLessEqual(result, 0.0)

if __name__ == '__main__':
    unittest.main()