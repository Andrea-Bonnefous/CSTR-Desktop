import unittest
import numpy as np
from functions import CSTRSimulator  # Assure-toi que CSTRSimulator est bien défini ici

class TestReactionRate(unittest.TestCase):
    def test_reaction_rate(self):
        sim = CSTRSimulator()
        
        sim.R = 8.314  # constante des gaz
        temp = 350.0  # température en Kelvin
        component_conc = {"A": 1.0, "B": 2.0}
        reaction = {
            "frequency_factor": 1e10,
            "activation_energy": 80000.0,
            "reaction_order": {"A": 1, "B": 1},
            "stoichiometry": {"A": -1, "B": -1, "C": 1},
            "reversible": True,
            "equilibrium_constant": 5.0,
            "heat_of_reaction": -50000.0,
            "reference_temperature": 298.15
        }

        rate = sim.reaction_rate(component_conc, temp, reaction)

        self.assertIsInstance(rate, float)
        if not reaction["reversible"]:
            self.assertGreaterEqual(rate, 0.0)
        self.assertLessEqual(rate, 100.0)

if __name__ == '__main__':
    unittest.main()