import unittest
import functions

class ReactionDatabase(unittest.TestCase):
    """Database of common chemical reactions with their parameters"""
    
    def test___init__(self):
        self.reactions = self.test__load_reactions()
        
    def test__load_reactions(self):
        """Load reaction database"""
        return {
            "Ammonia Synthesis (Haber Process)": {
                "description": "N2 + 3H2 → 2NH3 - Production of ammonia from nitrogen and hydrogen",
                "reactions": [
                    {
                        "name": "Ammonia synthesis",
                        "stoichiometry": {"N2": -1, "H2": -3, "NH3": 2},
                        "frequency_factor": 8.85e9,
                        "activation_energy": 88000,  # kJ/mol converted to J/mol
                        "reaction_order": {"N2": 1.0, "H2": 0.5},
                        "reversible": True,
                        "equilibrium_constant": 6.3e-2
                    }
                ],
                "feed_composition": {
                    "N2": 100.0,
                    "H2": 300.0
                },
                "target_product": "NH3",
                "catalyst": "Iron with Potassium oxide and Aluminum oxide promoters",
                "temperature_range": (600, 800)
            },
            "Chloralkali Process": {
                "description": "2NaCl + 2H2O → Cl2 + H2 + 2NaOH - Production of chlorine, hydrogen, and sodium hydroxide",
                "reactions": [
                    {
                        "name": "Chloralkali electrolysis",
                        "stoichiometry": {"NaCl": -2, "H2O": -2, "Cl2": 1, "H2": 1, "NaOH": 2},
                        "frequency_factor": 3.2e8,
                        "activation_energy": 75200,
                        "reaction_order": {"NaCl": 0.5, "H2O": 0.5},
                        "reversible": False,
                        "equilibrium_constant": 4.5e5
                    }
                ],
                "feed_composition": {
                    "NaCl": 100.0,
                    "H2O": 100.0
                },
                "target_product": "Cl2",
                "catalyst": "Mercury electrode, Membrane, or Diaphragm",
                "temperature_range": (330, 360)
            },
            "Contact Process (Sulfuric Acid)": {
                "description": "2SO2 + O2 → 2SO3 - Oxidation of sulfur dioxide to sulfur trioxide",
                "reactions": [
                    {
                        "name": "SO2 oxidation",
                        "stoichiometry": {"SO2": -2, "O2": -1, "SO3": 2},
                        "frequency_factor": 1.2e11,
                        "activation_energy": 113000,
                        "reaction_order": {"SO2": 1, "O2": 1},
                        "reversible": True,
                        "equilibrium_constant": 3.6e4,
                        "heat_of_reaction": -98000
                    }
                ],
                "feed_composition": {
                    "SO2": 30.0,
                    "O2": 15.0
                },
                "target_product": "SO3",
                "catalyst": "Vanadium pentoxide or Platinum",
                "temperature_range": (650, 800)
            },
            "Ethylene Oxide Production": {
                "description": "C2H4 + 1/2O2 → C2H4O - Direct oxidation of ethylene to ethylene oxide",
                "reactions": [
                    {
                        "name": "Ethylene epoxidation",
                        "stoichiometry": {"C2H4": -1, "O2": -0.5, "C2H4O": 1},
                        "frequency_factor": 4.7e7,
                        "activation_energy": 57600,
                        "reaction_order": {"C2H4": 1, "O2": 1},
                        "reversible": True,
                        "equilibrium_constant": 1.2e9
                    }
                ],
                "feed_composition": {
                    "C2H4": 20.0,
                    "O2": 10.0
                },
                "target_product": "C2H4O",
                "catalyst": "Silver with Cesium promoter",
                "temperature_range": (450, 600)
            },
            "Fischer-Tropsch Process": {
                "description": "CO + 2H2 → -(CH2)- + H2O - Conversion of syngas to hydrocarbons",
                "reactions": [
                    {
                        "name": "Fischer-Tropsch synthesis",
                        "stoichiometry": {"CO": -1, "H2": -2, "CH2": 1, "H2O": 1},
                        "frequency_factor": 3.5e12,
                        "activation_energy": 140000,
                        "reaction_order": {"CO": 0.6, "H2": 0.4},
                        "reversible": True,
                        "equilibrium_constant": 2.8e2
                    }
                ],
                "feed_composition": {
                    "CO": 25.0,
                    "H2": 50.0
                },
                "target_product": "CH2",
                "catalyst": "Iron, Cobalt, or Ruthenium",
                "temperature_range": (500, 650)
            },
            "Formaldehyde Production": {
                "description": "CH3OH + 1/2O2 → CH2O + H2O - Oxidation of methanol to formaldehyde",
                "reactions": [
                    {
                        "name": "Methanol oxidation",
                        "stoichiometry": {"CH3OH": -1, "O2": -0.5, "CH2O": 1, "H2O": 1},
                        "frequency_factor": 7.3e9,
                        "activation_energy": 84600,
                        "reaction_order": {"CH3OH": 0.7, "O2": 0.3},
                        "reversible": False,
                        "equilibrium_constant": 8.9e7
                    }
                ],
                "feed_composition": {
                    "CH3OH": 25.0,
                    "O2": 12.5
                },
                "target_product": "CH2O",
                "catalyst": "Silver or Iron-molybdenum oxide",
                "temperature_range": (800, 950)
            },
            "Methanol Synthesis": {
                "description": "CO + 2H2 → CH3OH - Catalytic hydrogenation of carbon monoxide",
                "reactions": [
                    {
                        "name": "Methanol formation",
                        "stoichiometry": {"CO": -1, "H2": -2, "CH3OH": 1},
                        "frequency_factor": 5.1e10,
                        "activation_energy": 97000,
                        "reaction_order": {"CO": 1, "H2": 1},
                        "reversible": True,
                        "equilibrium_constant": 2.3e-3
                    }
                ],
                "feed_composition": {
                    "CO": 15.0,
                    "H2": 30.0
                },
                "target_product": "CH3OH",
                "catalyst": "Copper-zinc oxide with chromium oxide",
                "temperature_range": (450, 600)
            },
            "Nitric Acid Production (Ostwald Process)": {
                "description": "4NH3 + 5O2 → 4NO + 6H2O - Oxidation of ammonia to nitric oxide",
                "reactions": [
                    {
                        "name": "Ammonia oxidation",
                        "stoichiometry": {"NH3": -4, "O2": -5, "NO": 4, "H2O": 6},
                        "frequency_factor": 2.4e15,
                        "activation_energy": 209000,
                        "reaction_order": {"NH3": 0.8, "O2": 0.2},
                        "reversible": False,
                        "equilibrium_constant": 1.8e20
                    }
                ],
                "feed_composition": {
                    "NH3": 40.0,
                    "O2": 50.0
                },
                "target_product": "NO",
                "catalyst": "Platinum-rhodium gauze",
                "temperature_range": (800, 1200)
            },
            "Polyethylene Production": {
                "description": "nC2H4 → -(C2H4)n- - Polymerization of ethylene to polyethylene",
                "reactions": [
                    {
                        "name": "Ethylene polymerization",
                        "stoichiometry": {"C2H4": -1, "PE": 1},
                        "frequency_factor": 1.7e14,
                        "activation_energy": 210000,
                        "reaction_order": {"C2H4": 1},
                        "reversible": False,
                        "equilibrium_constant": 4.1e6
                    }
                ],
                "feed_composition": {
                    "C2H4": 50.0
                },
                "target_product": "PE",
                "catalyst": "Ziegler-Natta or Metallocene catalysts",
                "temperature_range": (350, 500)
            },
            "Steam Reforming of Methane": {
                "description": "CH4 + H2O → CO + 3H2 - Production of syngas from methane and steam",
                "reactions": [
                    {
                        "name": "Methane steam reforming",
                        "stoichiometry": {"CH4": -1, "H2O": -1, "CO": 1, "H2": 3},
                        "frequency_factor": 4.3e16,
                        "activation_energy": 236000,
                        "reaction_order": {"CH4": 0.6, "H2O": 0.4},
                        "reversible": True,
                        "equilibrium_constant": 2.7e-2,
                        "heat_of_reaction": 206000
                    }
                ],
                "feed_composition": {
                    "CH4": 30.0,
                    "H2O": 30.0
                },
                "target_product": "H2",
                "catalyst": "Nickel on alumina support",
                "temperature_range": (800, 1150)
            },
            "Water Gas Shift Reaction": {
                "description": "CO + H2O → CO2 + H2 - Conversion of carbon monoxide and water to carbon dioxide and hydrogen",
                "reactions": [
                    {
                        "name": "Water-gas shift",
                        "stoichiometry": {"CO": -1, "H2O": -1, "CO2": 1, "H2": 1},
                        "frequency_factor": 2.8e9,
                        "activation_energy": 88000,
                        "reaction_order": {"CO": 0.5, "H2O": 0.5},
                        "reversible": True,
                        "equilibrium_constant": 4.5e-1,
                        "heat_of_reaction": -41000
                    }
                ],
                "feed_composition": {
                    "CO": 25.0,
                    "H2O": 25.0
                },
                "target_product": "H2",
                "catalyst": "Iron oxide-chromium oxide or Copper-zinc oxide",
                "temperature_range": (600, 750)
            },
            "Acetic Acid Production": {
                "description": "CH3OH + CO → CH3COOH - Carbonylation of methanol to acetic acid",
                "reactions": [
                    {
                        "name": "Methanol carbonylation",
                        "stoichiometry": {"CH3OH": -1, "CO": -1, "CH3COOH": 1},
                        "frequency_factor": 3.7e11,
                        "activation_energy": 110000,
                        "reaction_order": {"CH3OH": 1, "CO": 1},
                        "reversible": True,
                        "equilibrium_constant": 2.8e3
                    }
                ],
                "feed_composition": {
                    "CH3OH": 20.0,
                    "CO": 20.0
                },
                "target_product": "CH3COOH",
                "catalyst": "Rhodium-iodide complex",
                "temperature_range": (400, 500)
            },
            "Bisphenol A Production": {
                "description": "2C6H5OH + (CH3)2CO → (CH3)2C(C6H4OH)2 + H2O - Condensation of phenol with acetone",
                "reactions": [
                    {
                        "name": "Phenol-acetone condensation",
                        "stoichiometry": {"C6H5OH": -2, "(CH3)2CO": -1, "BPA": 1, "H2O": 1},
                        "frequency_factor": 5.8e11,
                        "activation_energy": 125000,
                        "reaction_order": {"C6H5OH": 1, "(CH3)2CO": 1},
                        "reversible": True,
                        "equilibrium_constant": 8.6e2
                    }
                ],
                "feed_composition": {
                    "C6H5OH": 40.0,
                    "(CH3)2CO": 20.0
                },
                "target_product": "BPA",
                "catalyst": "Ion exchange resin or HCl",
                "temperature_range": (330, 360)
            },
            "Cumene Process": {
                "description": "C6H6 + C3H6 → C6H5CH(CH3)2 - Alkylation of benzene with propylene",
                "reactions": [
                    {
                        "name": "Benzene alkylation",
                        "stoichiometry": {"C6H6": -1, "C3H6": -1, "C6H5CH(CH3)2": 1},
                        "frequency_factor": 1.6e10,
                        "activation_energy": 94000,
                        "reaction_order": {"C6H6": 1, "C3H6": 1},
                        "reversible": True,
                        "equilibrium_constant": 7.2e3
                    }
                ],
                "feed_composition": {
                    "C6H6": 25.0,
                    "C3H6": 25.0
                },
                "target_product": "C6H5CH(CH3)2",
                "catalyst": "Phosphoric acid or Zeolites",
                "temperature_range": (450, 600)
            },
            "Styrene Production": {
                "description": "C6H5CH2CH3 → C6H5CH=CH2 + H2 - Dehydrogenation of ethylbenzene to styrene",
                "reactions": [
                    {
                        "name": "Ethylbenzene dehydrogenation",
                        "stoichiometry": {"C6H5CH2CH3": -1, "C6H5CH=CH2": 1, "H2": 1},
                        "frequency_factor": 5.9e16,
                        "activation_energy": 247000,
                        "reaction_order": {"C6H5CH2CH3": 1},
                        "reversible": True,
                        "equilibrium_constant": 8.4e-3,
                        "heat_of_reaction": 124500
                    }
                ],
                "feed_composition": {
                    "C6H5CH2CH3": 30.0
                },
                "target_product": "C6H5CH=CH2",
                "catalyst": "Iron oxide with potassium oxide",
                "temperature_range": (800, 950)
            },
            "Propylene Oxide Production": {
                "description": "C3H6 + H2O2 → C3H6O + H2O - Direct oxidation of propylene to propylene oxide",
                "reactions": [
                    {
                        "name": "Propylene epoxidation",
                        "stoichiometry": {"C3H6": -1, "H2O2": -1, "C3H6O": 1, "H2O": 1},
                        "frequency_factor": 4.7e8,
                        "activation_energy": 67000,
                        "reaction_order": {"C3H6": 1, "H2O2": 1},
                        "reversible": False,
                        "equilibrium_constant": 2.8e6
                    }
                ],
                "feed_composition": {
                    "C3H6": 22.0,
                    "H2O2": 22.0
                },
                "target_product": "C3H6O",
                "catalyst": "Titanium silicalite",
                "temperature_range": (300, 350)
            },
            "Acetaldehyde Production": {
                "description": "C2H4 + 1/2O2 → CH3CHO - Oxidation of ethylene to acetaldehyde",
                "reactions": [
                    {
                        "name": "Wacker process",
                        "stoichiometry": {"C2H4": -1, "O2": -0.5, "CH3CHO": 1},
                        "frequency_factor": 7.6e9,
                        "activation_energy": 92000,
                        "reaction_order": {"C2H4": 0.6, "O2": 0.4},
                        "reversible": True,
                        "equilibrium_constant": 9.5e6
                    }
                ],
                "feed_composition": {
                    "C2H4": 20.0,
                    "O2": 10.0
                },
                "target_product": "CH3CHO",
                "catalyst": "Palladium chloride and Copper chloride",
                "temperature_range": (380, 430)
            },
            "Chlorination of Methane": {
                "description": "CH4 + Cl2 → CH3Cl + HCl - Substitution of hydrogen with chlorine in methane",
                "reactions": [
                    {
                        "name": "Methane chlorination",
                        "stoichiometry": {"CH4": -1, "Cl2": -1, "CH3Cl": 1, "HCl": 1},
                        "frequency_factor": 1.8e7,
                        "activation_energy": 56000,
                        "reaction_order": {"CH4": 1, "Cl2": 0.5},
                        "reversible": False,
                        "equilibrium_constant": 7.9e5
                    }
                ],
                "feed_composition": {
                    "CH4": 25.0,
                    "Cl2": 25.0
                },
                "target_product": "CH3Cl",
                "catalyst": "UV light",
                "temperature_range": (550, 700)
            },
            "Vinyl Chloride Production": {
                "description": "C2H2 + HCl → C2H3Cl - Addition of hydrogen chloride to acetylene",
                "reactions": [
                    {
                        "name": "Acetylene hydrochlorination",
                        "stoichiometry": {"C2H2": -1, "HCl": -1, "C2H3Cl": 1},
                        "frequency_factor": 8.4e10,
                        "activation_energy": 98000,
                        "reaction_order": {"C2H2": 1, "HCl": 1},
                        "reversible": True,
                        "equilibrium_constant": 4.3e5
                    }
                ],
                "feed_composition": {
                    "C2H2": 20.0,
                    "HCl": 20.0
                },
                "target_product": "C2H3Cl",
                "catalyst": "Mercuric chloride",
                "temperature_range": (400, 450)
            },
            "Esterification (Industrial)": {
                "description": "CH3COOH + C2H5OH → CH3COOC2H5 + H2O - Formation of ethyl acetate from acetic acid and ethanol",
                "reactions": [
                    {
                        "name": "Esterification reaction",
                        "stoichiometry": {"CH3COOH": -1, "C2H5OH": -1, "CH3COOC2H5": 1, "H2O": 1},
                        "frequency_factor": 4.3e7,
                        "activation_energy": 57000,
                        "reaction_order": {"CH3COOH": 1, "C2H5OH": 1},
                        "reversible": True,
                        "equilibrium_constant": 4.2
                    }
                ],
                "feed_composition": {
                    "CH3COOH": 20.0,
                    "C2H5OH": 20.0
                },
                "target_product": "CH3COOC2H5",
                "catalyst": "Sulfuric acid",
                "temperature_range": (350, 400)
            },
            "Adipic Acid Production": {
                "description": "C6H12 + 2HNO3 → HOOC(CH2)4COOH + 2H2O + N2O - Oxidation of cyclohexane to adipic acid",
                "reactions": [
                    {
                        "name": "Cyclohexane oxidation",
                        "stoichiometry": {"C6H12": -1, "HNO3": -2, "C6H10O4": 1, "H2O": 2, "N2O": 1},
                        "frequency_factor": 9.2e12,
                        "activation_energy": 142000,
                        "reaction_order": {"C6H12": 0.7, "HNO3": 0.3},
                        "reversible": False,
                        "equilibrium_constant": 4.5e15
                    }
                ],
                "feed_composition": {
                    "C6H12": 20.0,
                    "HNO3": 40.0
                },
                "target_product": "C6H10O4",
                "catalyst": "Copper and Vanadium salts",
                "temperature_range": (330, 370)
            }
        }
if __name__ == "__main__":
    unittest.main()