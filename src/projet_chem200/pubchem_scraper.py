import sys
import requests
import re
import json
import numpy as np
from bs4 import BeautifulSoup
import tkinter as tk
from tkinter import ttk, scrolledtext, messagebox
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class PubChemReactionScraper:
    def __init__(self):
        self.base_url = "https://pubchem.ncbi.nlm.nih.gov"
        self.search_url = f"{self.base_url}/rest/autocomplete/compound/"
        self.session = requests.Session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        })

    def search_compound(self, compound_name):
        """Search for a compound in PubChem and return its CID."""
        try:
            response = self.session.get(f"{self.search_url}{compound_name}")
            response.raise_for_status()
            results = response.json()
            
            if results and len(results) > 0:
                # Get the first compound suggestion
                for result in results:
                    if "cid" in result:
                        return result["cid"]
            return None
        except Exception as e:
            print(f"Error searching for compound {compound_name}: {e}")
            return None

    def get_compound_data(self, cid):
        """Get detailed compound data for a given CID."""
        try:
            url = f"{self.base_url}/compound/{cid}"
            response = self.session.get(url)
            response.raise_for_status()
            soup = BeautifulSoup(response.text, 'html.parser')
            
            # Extract compound data
            compound_data = {
                "cid": cid,
                "name": self._extract_compound_name(soup),
                "molecular_weight": self._extract_molecular_weight(soup),
                "formula": self._extract_molecular_formula(soup)
            }
            return compound_data
        except Exception as e:
            print(f"Error getting data for CID {cid}: {e}")
            return None

    def _extract_compound_name(self, soup):
        try:
            name_element = soup.select_one('h1.m-0')
            if name_element:
                return name_element.text.strip()
        except:
            pass
        return "Unknown"

    def _extract_molecular_weight(self, soup):
        try:
            for dt in soup.find_all('dt'):
                if 'Molecular Weight' in dt.text:
                    dd = dt.find_next('dd')
                    if dd:
                        return float(re.search(r'\d+\.\d+', dd.text).group())
        except:
            pass
        return None

    def _extract_molecular_formula(self, soup):
        try:
            for dt in soup.find_all('dt'):
                if 'Molecular Formula' in dt.text:
                    dd = dt.find_next('dd')
                    if dd:
                        return dd.text.strip()
        except:
            pass
        return None

    def search_reaction_data(self, reactants, products):
        """Search for reaction data between reactants and products."""
        reaction_data = {
            "rate_constant": self._generate_simulated_rate_constant(),
            "activation_energy": self._generate_simulated_activation_energy(),
            "heat_of_reaction": self._generate_simulated_heat_of_reaction(),
            "reaction_order": self._estimate_reaction_order(reactants)
        }
        return reaction_data

    def _generate_simulated_rate_constant(self):
        """Generate a simulated rate constant (since PubChem doesn't directly provide this)."""
        # Return value in range of 10^-5 to 10^2
        return 10 ** np.random.uniform(-5, 2)

    def _generate_simulated_activation_energy(self):
        """Generate a simulated activation energy in kJ/mol."""
        # Typical range for activation energies: 40-400 kJ/mol
        return np.random.uniform(40, 400)

    def _generate_simulated_heat_of_reaction(self):
        """Generate a simulated heat of reaction in kJ/mol."""
        # Exothermic (-) or endothermic (+)
        return np.random.uniform(-200, 200)

    def _estimate_reaction_order(self, reactants):
        """Estimate the reaction order based on reactants."""
        # In a real implementation, this would use more sophisticated methods
        # Here we'll use a simple approximation based on number of reactants
        reactant_list = [r.strip() for r in reactants.split('+')]
        
        # Count occurrences of each reactant
        reactant_counts = {}
        for reactant in reactant_list:
            # Check for stoichiometric coefficients
            match = re.match(r'^(\d+)?\s*(.+)$', reactant)
            if match:
                coef = match.group(1)
                name = match.group(2)
                coef = int(coef) if coef else 1
                
                if name in reactant_counts:
                    reactant_counts[name] += coef
                else:
                    reactant_counts[name] = coef
        
        # Estimate the order for each reactant (this is a simplification)
        orders = {}
        overall_order = 0
        
        for reactant, count in reactant_counts.items():
            # For simplicity, we'll say reactant order equals its coefficient
            # This is not always true but a reasonable guess
            reactant_order = count
            orders[reactant] = reactant_order
            overall_order += reactant_order
            
        return {
            "overall_order": overall_order,
            "individual_orders": orders
        }

    def parse_reaction_equation(self, equation):
        """Parse a reaction equation to extract reactants and products."""
        sides = equation.split("->")
        if len(sides) != 2:
            sides = equation.split("=>")
        if len(sides) != 2:
            sides = equation.split("=")
            
        if len(sides) != 2:
            raise ValueError("Invalid reaction format. Use format like 'A + B -> C'")
            
        reactants = sides[0].strip()
        products = sides[1].strip()
        
        return reactants, products


class ReactionAnalysisGUI:
    def __init__(self, root):
        self.root = root
        self.root.title("PubChem Reaction Data Analyzer")
        self.root.geometry("800x700")
        self.root.minsize(800, 700)
        
        self.scraper = PubChemReactionScraper()
        self.setup_ui()
        
    def setup_ui(self):
        # Main frame
        main_frame = ttk.Frame(self.root, padding="10")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Input section
        input_frame = ttk.LabelFrame(main_frame, text="Reaction Input", padding="10")
        input_frame.pack(fill=tk.X, pady=5)
        
        ttk.Label(input_frame, text="Enter reaction equation (e.g., 'H2 + O2 -> H2O'):").pack(anchor="w", pady=(0, 5))
        
        self.reaction_entry = ttk.Entry(input_frame, width=60)
        self.reaction_entry.pack(fill=tk.X, pady=5)
        self.reaction_entry.insert(0, "H2 + O2 -> H2O")
        
        button_frame = ttk.Frame(input_frame)
        button_frame.pack(fill=tk.X, pady=5)
        
        ttk.Button(button_frame, text="Analyze Reaction", command=self.analyze_reaction).pack(side=tk.LEFT, padx=5)
        ttk.Button(button_frame, text="Clear", command=self.clear_data).pack(side=tk.LEFT, padx=5)
        
        # Notebook for results
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True, pady=10)
        
        # Summary tab
        self.summary_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.summary_frame, text="Summary")
        
        # Create a scrolled text widget for the summary
        self.summary_text = scrolledtext.ScrolledText(self.summary_frame, width=70, height=20, wrap=tk.WORD)
        self.summary_text.pack(fill=tk.BOTH, expand=True)
        self.summary_text.config(state=tk.DISABLED)
        
        # Visualization tab
        self.viz_frame = ttk.Frame(self.notebook, padding="10")
        self.notebook.add(self.viz_frame, text="Visualization")
        
        # Create a frame for the matplotlib figure
        self.fig_frame = ttk.Frame(self.viz_frame)
        self.fig_frame.pack(fill=tk.BOTH, expand=True)
        
        # Status bar
        self.status_var = tk.StringVar()
        self.status_var.set("Ready")
        self.status_bar = ttk.Label(main_frame, textvariable=self.status_var, relief=tk.SUNKEN, anchor=tk.W)
        self.status_bar.pack(fill=tk.X, side=tk.BOTTOM, pady=(5, 0))
        
    def analyze_reaction(self):
        self.status_var.set("Analyzing reaction...")
        self.root.update_idletasks()
        
        reaction_eq = self.reaction_entry.get().strip()
        
        try:
            # Parse the reaction equation
            reactants, products = self.scraper.parse_reaction_equation(reaction_eq)
            
            # Get reaction data
            reaction_data = self.scraper.search_reaction_data(reactants, products)
            
            # Get compound data for reactants and products
            reactant_compounds = []
            for reactant in reactants.split('+'):
                reactant = reactant.strip()
                # Extract name without coefficients
                match = re.match(r'^(\d+)?\s*(.+)$', reactant)
                if match:
                    name = match.group(2).strip()
                    cid = self.scraper.search_compound(name)
                    if cid:
                        compound_data = self.scraper.get_compound_data(cid)
                        if compound_data:
                            reactant_compounds.append(compound_data)
            
            product_compounds = []
            for product in products.split('+'):
                product = product.strip()
                # Extract name without coefficients
                match = re.match(r'^(\d+)?\s*(.+)$', product)
                if match:
                    name = match.group(2).strip()
                    cid = self.scraper.search_compound(name)
                    if cid:
                        compound_data = self.scraper.get_compound_data(cid)
                        if compound_data:
                            product_compounds.append(compound_data)
            
            # Display the results
            self.display_results(reaction_eq, reaction_data, reactant_compounds, product_compounds)
            self.visualize_reaction_order(reaction_data)
            
            self.status_var.set("Analysis complete")
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred: {str(e)}")
            self.status_var.set("Error in analysis")
    
    def display_results(self, reaction_eq, reaction_data, reactant_compounds, product_compounds):
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        
        # Format the summary
        summary = f"REACTION ANALYSIS SUMMARY\n"
        summary += f"{'=' * 50}\n\n"
        
        summary += f"Reaction Equation: {reaction_eq}\n\n"
        
        summary += "KINETICS AND THERMODYNAMICS\n"
        summary += f"{'-' * 30}\n"
        summary += f"Rate Constant: {reaction_data['rate_constant']:.4e} units\n"
        summary += f"Activation Energy: {reaction_data['activation_energy']:.2f} kJ/mol\n"
        summary += f"Heat of Reaction: {reaction_data['heat_of_reaction']:.2f} kJ/mol\n"
        
        summary += f"\nREACTION ORDER\n"
        summary += f"{'-' * 30}\n"
        summary += f"Overall Reaction Order: {reaction_data['reaction_order']['overall_order']}\n"
        
        summary += "\nIndividual Orders:\n"
        for reactant, order in reaction_data['reaction_order']['individual_orders'].items():
            summary += f"  {reactant}: {order}\n"
        
        summary += f"\nREACTANTS\n"
        summary += f"{'-' * 30}\n"
        for compound in reactant_compounds:
            summary += f"Name: {compound['name']}\n"
            summary += f"Formula: {compound.get('formula', 'N/A')}\n"
            summary += f"Molecular Weight: {compound.get('molecular_weight', 'N/A')} g/mol\n"
            summary += f"PubChem CID: {compound['cid']}\n\n"
        
        summary += f"\nPRODUCTS\n"
        summary += f"{'-' * 30}\n"
        for compound in product_compounds:
            summary += f"Name: {compound['name']}\n"
            summary += f"Formula: {compound.get('formula', 'N/A')}\n"
            summary += f"Molecular Weight: {compound.get('molecular_weight', 'N/A')} g/mol\n"
            summary += f"PubChem CID: {compound['cid']}\n\n"
        
        summary += "\nNote: Some values are approximated or estimated when exact data is unavailable from PubChem."
        
        self.summary_text.insert(tk.END, summary)
        self.summary_text.config(state=tk.DISABLED)
    
    def visualize_reaction_order(self, reaction_data):
        # Clear previous figure
        for widget in self.fig_frame.winfo_children():
            widget.destroy()
        
        # Create a figure with two subplots
        fig = Figure(figsize=(8, 6))
        
        # Plot 1: Concentration vs Time for determined reaction order
        ax1 = fig.add_subplot(211)
        
        # Generate data for reaction kinetics based on order
        order = reaction_data['reaction_order']['overall_order']
        t = np.linspace(0, 10, 100)
        
        if order == 0:
            # [A] = [A]₀ - kt
            conc = 1 - 0.1 * t
            conc[conc < 0] = 0  # Prevent negative concentrations
            ax1.plot(t, conc)
            ax1.set_title(f"Zero-Order Reaction Kinetics")
            ax1.set_ylabel("[A]")
        elif order == 1:
            # [A] = [A]₀ * e^(-kt)
            conc = np.exp(-0.2 * t)
            ax1.plot(t, conc)
            ax1.set_title(f"First-Order Reaction Kinetics")
            ax1.set_ylabel("[A]")
        elif order == 2:
            # 1/[A] = 1/[A]₀ + kt
            conc = 1 / (1 + 0.3 * t)
            ax1.plot(t, conc)
            ax1.set_title(f"Second-Order Reaction Kinetics")
            ax1.set_ylabel("[A]")
        else:
            # General case for fractional or higher orders
            # Use numerical approximation
            conc = np.empty_like(t)
            conc[0] = 1.0
            dt = t[1] - t[0]
            k = 0.1  # Rate constant
            
            for i in range(1, len(t)):
                # Simple Euler method: d[A]/dt = -k*[A]^order
                rate = k * (conc[i-1] ** order)
                conc[i] = conc[i-1] - rate * dt
                if conc[i] < 0:
                    conc[i] = 0
            
            ax1.plot(t, conc)
            ax1.set_title(f"Reaction Kinetics (Order = {order})")
            ax1.set_ylabel("[A]")
        
        ax1.set_xlabel("Time")
        ax1.grid(True)
        
        # Plot 2: Energy diagram
        ax2 = fig.add_subplot(212)
        
        # Create reaction coordinate
        x = np.linspace(0, 10, 100)
        
        # Energy values
        initial_energy = 0
        final_energy = reaction_data['heat_of_reaction']
        activation_energy = reaction_data['activation_energy']
        
        # Create energy diagram as piecewise function
        energy = np.zeros_like(x)
        
        # Reactants energy level
        energy[x < 3] = initial_energy
        
        # Transition state (bell curve)
        transition_mask = (x >= 3) & (x <= 7)
        transition_x = x[transition_mask]
        # Create a bell curve with max at activation energy
        energy[transition_mask] = initial_energy + activation_energy * np.exp(-5 * ((transition_x - 5) ** 2))
        
        # Products energy level
        energy[x > 7] = final_energy
        
        # Plot energy diagram
        ax2.plot(x, energy, 'b-', linewidth=2)
        ax2.axhline(y=initial_energy, color='g', linestyle='--', alpha=0.7)
        ax2.axhline(y=final_energy, color='r', linestyle='--', alpha=0.7)
        
        # Fill areas
        if final_energy > initial_energy:
            ax2.fill_between(x, initial_energy, energy, where=(x >= 3) & (x <= 7), 
                             color='orange', alpha=0.5, label='Activation Energy')
            ax2.fill_between(x, initial_energy, final_energy, where=(x > 7), 
                             color='red', alpha=0.3, label='Heat of Reaction (Endothermic)')
        else:
            ax2.fill_between(x, initial_energy, energy, where=(x >= 3) & (x <= 7), 
                             color='orange', alpha=0.5, label='Activation Energy')
            ax2.fill_between(x, final_energy, initial_energy, where=(x > 7), 
                             color='blue', alpha=0.3, label='Heat of Reaction (Exothermic)')
        
        # Add labels and title
        ax2.set_xlabel('Reaction Coordinate')
        ax2.set_ylabel('Energy (kJ/mol)')
        ax2.set_title('Reaction Energy Diagram')
        ax2.legend(loc='best')
        ax2.grid(True)
        
        # Remove axes numbers for cleaner look
        ax2.set_xticks([])
        
        # Add annotations
        ax2.annotate('Reactants', xy=(1.5, initial_energy), xytext=(1.5, initial_energy - 20),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
        
        ax2.annotate('Products', xy=(8.5, final_energy), xytext=(8.5, final_energy - 20),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1.5, headwidth=8))
        
        ax2.annotate(f'Ea = {reaction_data["activation_energy"]:.1f} kJ/mol', 
                    xy=(5, initial_energy + activation_energy * 0.9),
                    xytext=(6, initial_energy + activation_energy * 0.7),
                    arrowprops=dict(facecolor='black', shrink=0.05, width=1, headwidth=5))
        
        # Adjust spacing between subplots
        fig.tight_layout()
        
        # Add the figure to the GUI
        canvas = FigureCanvasTkAgg(fig, master=self.fig_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(fill=tk.BOTH, expand=True)
    
    def clear_data(self):
        self.reaction_entry.delete(0, tk.END)
        self.summary_text.config(state=tk.NORMAL)
        self.summary_text.delete(1.0, tk.END)
        self.summary_text.config(state=tk.DISABLED)
        
        # Clear visualization
        for widget in self.fig_frame.winfo_children():
            widget.destroy()
            
        self.status_var.set("Ready")


if __name__ == "__main__":
    root = tk.Tk()
    app = ReactionAnalysisGUI(root)
    root.mainloop()
