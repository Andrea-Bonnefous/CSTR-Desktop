import unittest
from functions import CSTRSimulator
import matplotlib.figure

class TestCreateVisualization(unittest.TestCase):
    def test_create_visualization(self):
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
        fig, axes = sim.create_visualization()

        self.assertIsInstance(fig, matplotlib.figure.Figure)
        self.assertEqual(len(axes), 2)
        self.assertEqual(len(axes[0]), 2)
        self.assertEqual(len(axes[1]), 2)

if __name__ == '__main__':
    unittest.main()