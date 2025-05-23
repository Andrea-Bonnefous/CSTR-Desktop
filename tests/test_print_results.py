import unittest
from functions import CSTRSimulator
import io
import sys

class TestPrintResults(unittest.TestCase):
    def test_print_results(self):
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

        captured_output = io.StringIO()
        sys.stdout = captured_output
        results = sim.print_results()
        sys.stdout = sys.__stdout__

        self.assertIsInstance(results, dict)
        self.assertIn("temperature", results)
        self.assertIn("yield", results)
        self.assertTrue("CSTR SIMULATION RESULTS" in captured_output.getvalue())

if __name__ == '__main__':
    unittest.main()