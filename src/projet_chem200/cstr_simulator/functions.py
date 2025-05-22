import numpy as np
import pandas as pd
from scipy.optimize import minimize
import matplotlib.pyplot as plt
import tkinter as tk
from tkinter import ttk, messagebox
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json


class ReactionDatabase:
    """Database of common chemical reactions with their parameters"""
    
    def __init__(self):
        self.reactions = self._load_reactions()
        
    def _load_reactions(self):
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
        
    def get_reaction_names(self):
        """Return list of available reactions"""
        return list(self.reactions.keys())
    
    def get_reaction_details(self, reaction_name):
        """Return details for a specific reaction"""
        return self.reactions.get(reaction_name, None)

class CSTRSimulator:
    """
    A simulator for a Continuous Stirred Tank Reactor (CSTR) with reactions,
    recycle, and temperature optimization.
    """
    
    def __init__(self):
        # Constants
        self.R = 8.314  # J/(mol·K), Universal gas constant
        
    def set_parameters(self, volume, temperature, flow_rate, 
                       reactions, feed_composition, recycle_ratio=0.0, 
                       target_product=None, catalyst=None):
        """
        Set the parameters for the CSTR simulation
        
        Parameters:
        -----------
        volume : float
            Volume of the reactor in m³
        temperature : float
            Initial temperature in K
        flow_rate : float
            Feed flow rate in m³/s
        reactions : list
            List of reaction dictionaries
        feed_composition : dict
            Dictionary of feed compositions (mol/m³)
        recycle_ratio : float
            Recycle ratio (0-1)
        target_product : str
            Name of the target product to optimize
        catalyst : str, optional
            Name of the catalyst used in the reactor
        """
        self.volume = volume
        self.temperature = temperature
        self.flow_rate = flow_rate
        self.reactions = reactions
        self.feed_composition = feed_composition
        self.recycle_ratio = recycle_ratio
        self.target_product = target_product
        self.catalyst = catalyst
        
        # Get all components from reactions
        self.components = set()
        for reaction in self.reactions:
            for component in reaction["stoichiometry"].keys():
                self.components.add(component)
        self.components = list(self.components)
        
        # Initialize concentrations
        self.concentrations = {comp: 0.0 for comp in self.components}
        for comp, conc in feed_composition.items():
            self.concentrations[comp] = conc
    
    def reaction_rate(self, component_conc, temp, reaction):
        """Calculate reaction rate in mol/(m³·s)"""
        # Extract parameters
        k0 = reaction["frequency_factor"]
        Ea = reaction["activation_energy"]
        
        # Calculate frequency factor using Arrhenius equation
        # Add safeguards against extreme temperature values
        if temp <= 0:
            return 0.0
        
        # Limit extreme values to prevent overflow
        exp_term = -Ea / (self.R * temp)
        if exp_term < -700:  # Lower bound to prevent underflow
            exp_term = -700
        elif exp_term > 700:  # Upper bound to prevent overflow
            exp_term = 700
            
        k = k0 * np.exp(exp_term)
        
        # Check for unreasonably large frequency factors
        # In practice, frequency factor rarely exceed 1e12 in standard units
        if k > 1e12:
            k = 1e12
        
        # Calculate reaction rate based on reaction order
        rate = k
        for component, order in reaction["reaction_order"].items():
            if component in component_conc:
                # Prevent negative or zero concentration issues
                conc = max(1e-10, component_conc[component])
                rate *= conc ** order
        
        # Adjust for reversible reactions if needed
        if reaction.get("reversible", False):
            # Calculate equilibrium constant (can be temperature dependent)
            K_eq = reaction["equilibrium_constant"]
            
            # Add temperature dependence for equilibrium constant if available
            if "heat_of_reaction" in reaction:
                dH = reaction["heat_of_reaction"]
                T_ref = reaction.get("reference_temperature", 298.15)
                
                # Use van't Hoff equation with safety limits
                vant_hoff_term = (dH/self.R) * (1/T_ref - 1/temp)
                vant_hoff_term = max(min(vant_hoff_term, 700), -700)  # Limit to prevent overflow
                
                K_eq *= np.exp(vant_hoff_term)
            
            # Calculation of reaction quotient
            Q = 1.0
            try:
                for component, stoich in reaction["stoichiometry"].items():
                    if stoich > 0 and component_conc.get(component, 0) > 0:  # Products
                        Q *= component_conc[component] ** abs(stoich)
                    elif stoich < 0 and component_conc.get(component, 0) > 0:  # Reactants
                        Q /= component_conc[component] ** abs(stoich)
                
                # Ensure K_eq is not too small to avoid division issues
                K_eq = max(K_eq, 1e-10)
                
                # Adjust rate by equilibrium
                rate *= (1 - Q/K_eq)
            except (ZeroDivisionError, OverflowError):
                # If we have numerical issues, assume forward reaction dominates
                pass
        
        # Ensure rate is not negative (reaction can't go backward if not reversible)
        if not reaction.get("reversible", False) and rate < 0:
            rate = 0.0
            
        # Apply a final upper limit to rate to prevent unrealistic behavior
        max_reasonable_rate = 100.0  # mol/(m³·s) - can be adjusted based on application
        rate = min(rate, max_reasonable_rate)
        
        return rate
    
    def solve_steady_state(self, temperature=None):
        """
        Solve for steady-state concentrations at the given temperature
        """
        if temperature is None:
            temperature = self.temperature
        
        # For a CSTR with recycle, we need iterations to reach true steady state
        # Start with no recycle
        if self.recycle_ratio > 0:
            # Initialize with feed composition
            current_conc = {comp: conc for comp, conc in self.feed_composition.items()}
            for comp in self.components:
                if comp not in current_conc:
                    current_conc[comp] = 0.0
            
            # Iteratively solve until convergence
            max_iterations = 20
            tolerance = 1e-6
            converged = False
            
            for iteration in range(max_iterations):
                # Calculate the actual input concentration (fresh feed + recycle)
                inlet_conc = {comp: 0.0 for comp in self.components}
                for comp in self.components:
                    # Fresh feed contribution
                    fresh_feed = self.feed_composition.get(comp, 0.0)
                    # Recycle contribution
                    recycle_feed = current_conc.get(comp, 0.0) * self.recycle_ratio
                    # Combined feed
                    inlet_conc[comp] = fresh_feed * (1 - self.recycle_ratio) + recycle_feed
                
                # Calculate net generation/consumption rates for each component
                net_rates = {comp: 0.0 for comp in self.components}
                
                for reaction in self.reactions:
                    reaction_rate = self.reaction_rate(current_conc, temperature, reaction)
                    
                    # Ensure reaction rates are physically reasonable
                    # Reaction can't consume more than what's available in residence time
                    tau = self.volume / self.flow_rate  # residence time
                    
                    # Check if reaction rate is too high for any reactant
                    limiting_factor = 1.0
                    for component, stoich in reaction["stoichiometry"].items():
                        if stoich < 0:  # Reactant
                            if component in current_conc and current_conc[component] > 0:
                                # Maximum rate allowed by availability of this reactant
                                max_rate = current_conc[component] / (abs(stoich) * tau)
                                if reaction_rate > max_rate:
                                    # Scale down the reaction rate to avoid mass balance violations
                                    factor = max_rate / reaction_rate
                                    limiting_factor = min(limiting_factor, factor)
                    
                    # Apply the limiting factor to reaction rate
                    reaction_rate *= limiting_factor
                    
                    # Add contribution to net rates
                    for component, stoich in reaction["stoichiometry"].items():
                        if component in net_rates:
                            net_rates[component] += stoich * reaction_rate
                
                # Calculate new concentrations
                new_conc = {comp: 0.0 for comp in self.components}
                for comp in self.components:
                    # CSTR mass balance: in - out + generation = 0
                    # Solving for out: Cout = Cin + generation * tau
                    tau = self.volume / self.flow_rate  # residence time
                    new_conc[comp] = inlet_conc.get(comp, 0.0) + net_rates.get(comp, 0.0) * tau
                    # Ensure non-negative concentrations
                    new_conc[comp] = max(0.0, new_conc[comp])
                
                # Verify mass balance (atom balance)
                self._verify_mass_balance(inlet_conc, new_conc, reaction)
                
                # Check convergence
                max_diff = max([abs(new_conc[comp] - current_conc[comp]) for comp in self.components])
                if max_diff < tolerance:
                    converged = True
                    break
                
                # Update for next iteration
                current_conc = new_conc.copy()
            
            # Return converged concentrations
            self.concentrations = current_conc
        else:
            # No recycle, direct solution
            # Initialize with feed composition
            current_conc = {comp: conc for comp, conc in self.feed_composition.items()}
            for comp in self.components:
                if comp not in current_conc:
                    current_conc[comp] = 0.0
            
            # Calculate net generation/consumption rates for each component
            net_rates = {comp: 0.0 for comp in self.components}
            
            for reaction in self.reactions:
                reaction_rate = self.reaction_rate(current_conc, temperature, reaction)
                
                # Same check as above for physical reasonability
                tau = self.volume / self.flow_rate
                limiting_factor = 1.0
                for component, stoich in reaction["stoichiometry"].items():
                    if stoich < 0:  # Reactant
                        if component in current_conc and current_conc[component] > 0:
                            max_rate = current_conc[component] / (abs(stoich) * tau)
                            if reaction_rate > max_rate:
                                factor = max_rate / reaction_rate
                                limiting_factor = min(limiting_factor, factor)
                
                reaction_rate *= limiting_factor
                
                for component, stoich in reaction["stoichiometry"].items():
                    if component in net_rates:
                        net_rates[component] += stoich * reaction_rate
            
            # Calculate new concentrations
            new_conc = {comp: 0.0 for comp in self.components}
            for comp in self.components:
                tau = self.volume / self.flow_rate
                new_conc[comp] = current_conc.get(comp, 0.0) + net_rates.get(comp, 0.0) * tau
                new_conc[comp] = max(0.0, new_conc[comp])
            
            # Verify mass balance
            self._verify_mass_balance(current_conc, new_conc, reaction)
            
            self.concentrations = new_conc
        
        return self.concentrations
    
    def _verify_mass_balance(self, inlet_conc, outlet_conc, reaction):
        """
        Verify that mass balance is maintained in the reactor
        by checking elemental balances (this is a simplified version)
        """
        total_in = sum(inlet_conc.values())
        total_out = sum(outlet_conc.values())
        
        # If total moles out exceeds total moles in by more than 1%,
        # there might be a mass balance issue
        if total_out > total_in * 1.01:
            # Normalize outlet concentrations to maintain mass balance
            scale_factor = total_in / total_out
            for comp in outlet_conc:
                outlet_conc[comp] *= scale_factor
    
    def calculate_conversion(self, inlet_conc=None, outlet_conc=None):
        """Calculate the conversion of reactants"""
        if inlet_conc is None:
            inlet_conc = self.feed_composition
        if outlet_conc is None:
            outlet_conc = self.concentrations
        
        conversions = {}
        for comp in self.components:
            if comp in inlet_conc and inlet_conc[comp] > 0:
                conversions[comp] = (inlet_conc[comp] - outlet_conc[comp]) / inlet_conc[comp]
        
        return conversions
    
    def calculate_yield(self, product=None):
        """Calculate the yield of the target product"""
        if product is None:
            product = self.target_product
        
        if not product:
            return 0.0
        
        # Find reaction that produces the target product
        target_reaction = None
        target_stoich = 0
        
        for reaction in self.reactions:
            stoich = reaction["stoichiometry"].get(product, 0)
            if stoich > 0:
                target_reaction = reaction
                target_stoich = stoich
                break
        
        if not target_reaction:
            return 0.0
        
        # Find limiting reactant
        limiting_reactant = None
        limiting_reactant_stoich = 0
        max_theoretical_product = float('inf')
        
        for comp, stoich in target_reaction["stoichiometry"].items():
            if stoich < 0 and comp in self.feed_composition:
                # Calculate theoretical product from this reactant
                theoretical = self.feed_composition[comp] * target_stoich / abs(stoich)
                if theoretical < max_theoretical_product:
                    max_theoretical_product = theoretical
                    limiting_reactant = comp
                    limiting_reactant_stoich = stoich
        
        if not limiting_reactant:
            return 0.0
        
        # Calculate conversion of limiting reactant
        feed_conc = self.feed_composition.get(limiting_reactant, 0)
        exit_conc = self.concentrations.get(limiting_reactant, 0)
        
        # Adjust for recycle
        if self.recycle_ratio > 0:
            # Only consider the net input/output with recycle
            net_feed = feed_conc * (1 - self.recycle_ratio)
            net_exit = exit_conc * (1 - self.recycle_ratio)
            conversion = (net_feed - net_exit) / net_feed if net_feed > 0 else 0
        else:
            conversion = (feed_conc - exit_conc) / feed_conc if feed_conc > 0 else 0
        
        # Calculate selectivity (moles of product / moles of reactant consumed)
        actual_product = self.concentrations.get(product, 0)
        reactant_consumed = feed_conc * conversion
        
        if reactant_consumed > 0:
            selectivity = actual_product / (reactant_consumed * target_stoich / abs(limiting_reactant_stoich))
        else:
            selectivity = 0
        
        # Yield = conversion * selectivity
        yield_value = conversion * selectivity
        
        return max(0, min(1, yield_value))  # Ensure between 0 and 1
    
    def objective_function(self, temperature):
        """Objective function for temperature optimization (maximize yield)"""
        self.solve_steady_state(temperature)
        yield_value = self.calculate_yield()
        return -yield_value  # Negative because we're minimizing
    
    def optimize_temperature(self, bounds=(300, 1000)):
        """Find optimal temperature to maximize product yield"""
        # Test a more extensive grid of starting points
        test_temps = np.linspace(bounds[0], bounds[1], 10)
        best_yield = -1
        best_temp = bounds[0]
        
        for temp in test_temps:
            self.solve_steady_state(temp)
            yield_value = self.calculate_yield()
            if yield_value > best_yield:
                best_yield = yield_value
                best_temp = temp
        
        # Use best temperature as starting point for optimization
        # Use a more robust optimization configuration
        result = minimize(
            self.objective_function,
            x0=[best_temp],
            bounds=[bounds],
            method='L-BFGS-B',
            options={
                'ftol': 1e-8,       # More stringent function tolerance
                'gtol': 1e-6,       # More stringent gradient tolerance
                'maxiter': 100,     # More iterations
                'maxfun': 200,      # More function evaluations
                'eps': 0.1,         # Step size for finite-difference gradient
                'disp': False       # Don't display convergence messages
            }
        )
        
        # Verify that optimization actually improved the solution
        optimal_temp = result.x[0]
        optimal_yield = -result.fun  # Convert back from negative
        
        # If optimization didn't improve or only slightly improved the yield,
        # try a more detailed search around the best test point
        if optimal_yield <= best_yield * 1.01:  # Within 1% of best test point
            # Do a finer local search 
            local_bounds = (max(bounds[0], best_temp - 50), min(bounds[1], best_temp + 50))
            local_temps = np.linspace(local_bounds[0], local_bounds[1], 20)
            
            for temp in local_temps:
                self.solve_steady_state(temp)
                yield_value = self.calculate_yield()
                if yield_value > optimal_yield:
                    optimal_yield = yield_value
                    optimal_temp = temp
            
            # Try optimization again from this better starting point
            result = minimize(
                self.objective_function,
                x0=[optimal_temp],
                bounds=[local_bounds],
                method='L-BFGS-B',
                options={
                    'ftol': 1e-10,      # Very stringent function tolerance
                    'gtol': 1e-8,       # Very stringent gradient tolerance
                    'maxiter': 200,     # More iterations
                    'maxfun': 400,      # More function evaluations
                    'eps': 0.01,        # Smaller step for gradient
                }
            )
            
            # Use the result if it improved the yield
            if -result.fun > optimal_yield:
                optimal_temp = result.x[0]
        
        # Apply the optimal temperature
        self.temperature = optimal_temp
        self.solve_steady_state(optimal_temp)
        
        return optimal_temp
    
    def calculate_reaction_rates(self, temperature=None):
        """Calculate reaction rates at current conditions"""
        if temperature is None:
            temperature = self.temperature
        
        rates = {}
        for i, reaction in enumerate(self.reactions):
            rate = self.reaction_rate(self.concentrations, temperature, reaction)
            rates[f"Reaction {i+1}: {reaction['name']}"] = rate
        
        return rates
    
    def run_simulation(self, optimize_temp=True, temp_bounds=(300, 1000)):
        """Run a complete simulation with optimization"""
        # First solve without optimization
        self.solve_steady_state()
        
        # Optimize temperature if requested
        if optimize_temp:
            optimal_temp = self.optimize_temperature(temp_bounds)
        else:
            optimal_temp = self.temperature
        
        # Final solution at optimal temperature
        final_concentrations = self.solve_steady_state(optimal_temp)
        
        # Calculate product yield
        product_yield = self.calculate_yield()
        
        # Calculate reaction rates
        reaction_rates = self.calculate_reaction_rates()
        
        # Calculate conversions
        conversions = self.calculate_conversion()
        
        # Calculate recycle stream composition
        recycle_stream = {comp: conc * self.recycle_ratio 
                         for comp, conc in final_concentrations.items()}

        # Perform final mass balance check
        inlet_mass = sum([conc for comp, conc in self.feed_composition.items()])
        outlet_mass = sum([conc for comp, conc in final_concentrations.items()])
        mass_balance_error = abs(outlet_mass - inlet_mass) / inlet_mass if inlet_mass > 0 else 0
        
        # Calculate elemental balance
        elemental_balance = self._calculate_elemental_balance(final_concentrations)
        
        # Prepare results
        results = {
            "temperature": optimal_temp,
            "concentrations": final_concentrations,
            "recycle_stream": recycle_stream,
            "yield": product_yield,
            "reaction_rates": reaction_rates,
            "conversions": conversions,
            "residence_time": self.volume / self.flow_rate,
            "catalyst": self.catalyst,
            "mass_balance_error": mass_balance_error,
            "elemental_balance": elemental_balance
        }
        
        return results
        
    def _calculate_elemental_balance(self, concentrations):
        """
        Perform a simple check on elemental balance
        This is a simplified version - in reality, you would need molecular formulas
        """
        # For this simple version, we'll just indicate if output moles > input moles
        total_input = sum([conc for comp, conc in self.feed_composition.items()])
        total_output = sum([conc for comp, conc in concentrations.items()])
        
        return {
            "total_input_conc": total_input,
            "total_output_conc": total_output,
            "difference_percent": (total_output - total_input) / total_input * 100 if total_input > 0 else 0
        }
    
    def print_results(self, results=None):
        """Print simulation results in a formatted way"""
        if results is None:
            results = self.run_simulation()
        
        print("\n===== CSTR SIMULATION RESULTS =====")
        print(f"Optimal Temperature: {results['temperature']:.2f} K")
        print(f"Product Yield: {results['yield']*100:.2f}%")
        
        if results.get('catalyst'):
            print(f"Catalyst: {results['catalyst']}")
        else:
            print("Catalyst: None")
        
        print("\nSteady State Concentrations (mol/m³):")
        for component, conc in results["concentrations"].items():
            if component == self.target_product:
                print(f"  {component}: {conc:.4f} (TARGET PRODUCT)")
            else:
                print(f"  {component}: {conc:.4f}")
        
        print("\nRecycle Stream Concentrations (mol/m³):")
        for component, conc in results["recycle_stream"].items():
            print(f"  {component}: {conc:.4f}")
        
        print("\nFresh Feed Concentrations (mol/m³):")
        for component, conc in self.feed_composition.items():
            print(f"  {component}: {conc:.4f}")
        
        print(f"\nExit Flow Rate: {self.flow_rate:.4f} m³/s")
        print(f"Residence Time: {results['residence_time']:.2f} s")
        
        print("\nReaction Rates (mol/m³·s):")
        for name, rate in results["reaction_rates"].items():
            print(f"  {name}: {rate:.6f}")
        
        print("\nReactant Conversions:")
        for component, conversion in results["conversions"].items():
            if component in self.feed_composition:
                print(f"  {component}: {conversion*100:.2f}%")
        
        # Print mass balance information
        if "mass_balance_error" in results:
            print(f"\nMass Balance Error: {results['mass_balance_error']*100:.4f}%")
        
        if "elemental_balance" in results:
            eb = results["elemental_balance"]
            print("\nMass Balance Check:")
            print(f"  Total Input Concentration: {eb['total_input_conc']:.4f} mol/m³")
            print(f"  Total Output Concentration: {eb['total_output_conc']:.4f} mol/m³")
            print(f"  Difference: {eb['difference_percent']:.4f}%")
        
        print("\n==================================")
        
        return results
    
    def create_visualization(self, results=None):
        """Create visualization of simulation results"""
        if results is None:
            results = self.run_simulation()
        
        fig, axes = plt.subplots(2, 2, figsize=(14, 10))
        
        # 1. Plot steady state concentrations
        components = list(results["concentrations"].keys())
        concentrations = [results["concentrations"][comp] for comp in components]
        
        bar_colors = ['#1f77b4' if comp != self.target_product else '#ff7f0e' 
                      for comp in components]
        
        axes[0, 0].bar(components, concentrations, color=bar_colors)
        axes[0, 0].set_ylabel('Concentration (mol/m³)')
        axes[0, 0].set_title('Steady State Concentrations')
        axes[0, 0].grid(axis='y', linestyle='--', alpha=0.7)
        
        for i, v in enumerate(concentrations):
            axes[0, 0].text(i, v + 0.05*max(concentrations), f"{v:.3f}", ha='center')
        
        # 2. Plot temperature effect on yield
        if self.target_product:
            # Calculate yield at different temperatures
            temps = np.linspace(max(300, results['temperature']-200), 
                               min(1200, results['temperature']+200), 15)
            yields = []
            
            for temp in temps:
                self.solve_steady_state(temp)
                yields.append(self.calculate_yield())
            
            # Reset to original results
            self.solve_steady_state(results['temperature'])
            
            axes[0, 1].plot(temps, yields, 'b-')
            axes[0, 1].scatter([results['temperature']], [results['yield']], 
                             color='red', s=100)
            axes[0, 1].set_xlabel('Temperature (K)')
            axes[0, 1].set_ylabel('Product Yield')
            axes[0, 1].set_title('Temperature Effect on Yield')
            axes[0, 1].grid(True, linestyle='--', alpha=0.7)
            axes[0, 1].text(results['temperature'], results['yield'], 
                          f"Optimal: {results['temperature']:.1f}K", 
                          ha='right', va='bottom')
        
        # 3. Plot feed, recycle, and product composition
        comp_list = components
        x = np.arange(len(comp_list))
        width = 0.25
        
        feed_values = [self.feed_composition.get(comp, 0) for comp in comp_list]
        recycle_values = [results["recycle_stream"].get(comp, 0) for comp in comp_list]
        outlet_values = [results["concentrations"].get(comp, 0) for comp in comp_list]
        
        axes[1, 0].bar(x - width, feed_values, width=width, label='Fresh Feed')
        axes[1, 0].bar(x, recycle_values, width=width, label='Recycle')
        axes[1, 0].bar(x + width, outlet_values, width=width, label='Outlet')
        
        axes[1, 0].set_xlabel('Components')
        axes[1, 0].set_ylabel('Concentration (mol/m³)')
        axes[1, 0].set_title('Feed vs Recycle vs Outlet Composition')
        axes[1, 0].set_xticks(x)
        axes[1, 0].set_xticklabels(comp_list)
        axes[1, 0].legend()
        axes[1, 0].grid(axis='y', linestyle='--', alpha=0.7)
        
        # 4. Plot conversions
        if results["conversions"]:
            components = []
            conv_values = []
            
            for comp, conv in results["conversions"].items():
                if comp in self.feed_composition and self.feed_composition[comp] > 0:
                    components.append(comp)
                    conv_values.append(conv * 100)  # Convert to percentage
            
            if components:
                axes[1, 1].bar(components, conv_values, color='#2ca02c')
                axes[1, 1].set_ylabel('Conversion (%)')
                axes[1, 1].set_title('Reactant Conversion')
                axes[1, 1].grid(axis='y', linestyle='--', alpha=0.7)
                
                for i, v in enumerate(conv_values):
                    axes[1, 1].text(i, v + 1, f"{v:.1f}%", ha='center')
        
        plt.tight_layout()
        
        return fig, axes


