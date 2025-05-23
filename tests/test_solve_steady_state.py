import unittest
from functions import CSTRSimulator

class TestSolveSteadyState(unittest.TestCase):
    def test_solve_steady_state(self):
        sim = CSTRSimulator()

        # Définition des paramètres du réacteur
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
            recycle_ratio=0.0
        )

        concentrations = sim.solve_steady_state()

        # Vérifications de base
        self.assertIsInstance(concentrations, dict)
        self.assertIn("A", concentrations)
        self.assertIn("B", concentrations)
        for conc in concentrations.values():
            self.assertGreaterEqual(conc, 0.0)

if __name__ == '__main__':
    unittest.main()