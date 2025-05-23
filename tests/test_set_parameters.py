import unittest
from functions import CSTRSimulator  

class TestSetParameters(unittest.TestCase):
    def test_set_parameters(self):
        sim = CSTRSimulator()

        volume = 1.0
        temperature = 350.0
        flow_rate = 0.01
        reactions = [{"stoichiometry": {"A": -1, "B": 1}}]
        feed_composition = {"A": 1.0, "B": 0.0}
        recycle_ratio = 0.2
        target_product = "B"
        catalyst = "Pt"

        sim.set_parameters(volume, temperature, flow_rate,
                           reactions, feed_composition,
                           recycle_ratio, target_product, catalyst)

        self.assertEqual(sim.volume, volume)
        self.assertEqual(sim.temperature, temperature)
        self.assertEqual(sim.concentrations["A"], 1.0)
        self.assertEqual(sim.concentrations["B"], 0.0)
        self.assertIn("A", sim.components)
        self.assertIn("B", sim.components)

if __name__ == '__main__':
    unittest.main()