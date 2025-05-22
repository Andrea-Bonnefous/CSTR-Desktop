import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from typing import Dict, List, Any
import matplotlib.pyplot as plt
import io
import base64

# Import your actual classes (make sure these are in the same directory or properly installed)
from final_cstr_simulator import CSTRSimulator, ReactionDatabase

class StreamlitCSTRApp:
    """Streamlit interface for CSTR Simulator with process flow visualization"""
    
    def __init__(self):
        # Initialize simulator and database using your actual classes
        self.simulator = CSTRSimulator()
        self.database = ReactionDatabase()
        
    def create_process_flowchart(self, reaction_data: Dict, params: Dict, results: Dict = None):
        """Create an interactive process flow diagram"""
        fig = go.Figure()
        
        # Define positions for process elements (even wider spacing and better vertical positioning)
        positions = {
            'feed': (2, 4),
            'recycle_split': (3, 1.5),
            'mixer': (5, 4),
            'reactor': (8, 4),
            'separator': (11, 4),
            'product': (14, 4),
            'recycle': (11, 1.5)
        }
        
        # Add process boxes (larger boxes)
        boxes = [
            {'name': 'Fresh Feed', 'pos': positions['feed'], 'color': 'lightblue'},
            {'name': 'Recycle Split', 'pos': positions['recycle_split'], 'color': 'lightcoral'},
            {'name': 'Mixer', 'pos': positions['mixer'], 'color': 'lightgreen'},
            {'name': 'CSTR Reactor', 'pos': positions['reactor'], 'color': 'orange'},
            {'name': 'Separator', 'pos': positions['separator'], 'color': 'lightcyan'},
            {'name': 'Product', 'pos': positions['product'], 'color': 'gold'},
            {'name': 'Recycle', 'pos': positions['recycle'], 'color': 'lightcoral'}
        ]
        
        # Add boxes to figure (larger boxes)
        for box in boxes:
            x, y = box['pos']
            fig.add_shape(
                type="rect",
                x0=x-0.8, y0=y-0.5, x1=x+0.8, y1=y+0.5,
                fillcolor=box['color'],
                line=dict(color="black", width=2)
            )
            fig.add_annotation(
                x=x, y=y,
                text=box['name'],
                showarrow=False,
                font=dict(size=14, color="black"),
                bgcolor="white",
                bordercolor="black",
                borderwidth=1
            )
        
        # Add process streams (arrows) - completely avoid box overlap with better routing
        streams = [
            # Fresh feed to mixer - horizontal arrow
            ((positions['feed'][0]+0.8, positions['feed'][1]), (positions['mixer'][0]-0.8, positions['mixer'][1])),
            # Recycle split to mixer - angled upward
            ((positions['recycle_split'][0]+0.8, positions['recycle_split'][1]+0.5), (positions['mixer'][0]-0.8, positions['mixer'][1]-0.5)),
            # Mixer to reactor - horizontal arrow
            ((positions['mixer'][0]+0.8, positions['mixer'][1]), (positions['reactor'][0]-0.8, positions['reactor'][1])),
            # Reactor to separator - horizontal arrow
            ((positions['reactor'][0]+0.8, positions['reactor'][1]), (positions['separator'][0]-0.8, positions['separator'][1])),
            # Separator to product - horizontal arrow
            ((positions['separator'][0]+0.8, positions['separator'][1]), (positions['product'][0]-0.8, positions['product'][1])),
            # Separator to recycle - vertical down arrow
            ((positions['separator'][0], positions['separator'][1]-0.5), (positions['recycle'][0], positions['recycle'][1]+0.5)),
            # Recycle to recycle split - horizontal left arrow
            ((positions['recycle'][0]-0.8, positions['recycle'][1]), (positions['recycle_split'][0]+0.8, positions['recycle_split'][1]))
        ]
        
        for start, end in streams:
            fig.add_annotation(
                x=end[0], y=end[1],
                ax=start[0], ay=start[1],
                xref='x', yref='y',
                axref='x', ayref='y',
                arrowhead=2,
                arrowsize=1.5,
                arrowwidth=3,
                arrowcolor='blue'
            )
        
        # Add stream information if results are available
        if results:
            # Add feed composition info - positioned to the left and below to avoid cropping
            feed_comps = list(reaction_data['feed_composition'].keys())[:2]  # Show first 2 components
            feed_info = "Feed:\n" + "\n".join([f"{comp}: {reaction_data['feed_composition'][comp]:.1f} mol/m³" for comp in feed_comps])
            fig.add_annotation(
                x=positions['feed'][0]-1.2, y=positions['feed'][1]-1.2,  # Further left and down
                text=feed_info,
                showarrow=False,
                font=dict(size=11),
                bgcolor="lightyellow",
                bordercolor="gray",
                borderwidth=1
            )
            
            # Add reactor conditions - positioned below reactor
            reactor_info = f"T: {results.get('temperature', params['temperature']):.0f} K\nV: {params['volume']} m³\nτ: {results.get('residence_time', 0):.1f} s"
            fig.add_annotation(
                x=positions['reactor'][0], y=positions['reactor'][1]-1.2,
                text=reactor_info,
                showarrow=False,
                font=dict(size=11),
                bgcolor="lightyellow",
                bordercolor="gray",
                borderwidth=1
            )
            
            # Add product yield info - positioned to the right and below
            product_info = f"Yield: {results.get('yield', 0)*100:.1f}%\n{reaction_data['target_product']}: {results['concentrations'].get(reaction_data['target_product'], 0):.2f} mol/m³"
            fig.add_annotation(
                x=positions['product'][0]+1.2, y=positions['product'][1]-1.2,  # Further right and down
                text=product_info,
                showarrow=False,
                font=dict(size=11),
                bgcolor="lightgreen",
                bordercolor="gray",
                borderwidth=1
            )
            
            # Add recycle ratio info - positioned below recycle
            recycle_info = f"Recycle: {params['recycle_ratio']*100:.0f}%"
            fig.add_annotation(
                x=positions['recycle'][0], y=positions['recycle'][1]-1.0,
                text=recycle_info,
                showarrow=False,
                font=dict(size=11),
                bgcolor="lightcoral",
                bordercolor="gray",
                borderwidth=1
            )
            
            # Add steady state concentrations display - positioned at bottom center
            all_concentrations = results.get('concentrations', {})
            conc_text = "Steady State Concentrations:\n"
            for comp, conc in all_concentrations.items():
                if comp == reaction_data['target_product']:
                    conc_text += f"• {comp}: {conc:.3f} mol/m³ (TARGET)\n"
                else:
                    conc_text += f"• {comp}: {conc:.3f} mol/m³\n"
            
            # Position the concentration display at the bottom center of the chart
            fig.add_annotation(
                x=8, y=0.2,  # Center bottom of the chart
                text=conc_text,
                showarrow=False,
                font=dict(size=10),
                bgcolor="lightsteelblue",
                bordercolor="navy",
                borderwidth=2,
                align="left"
            )
        
        # Configure layout (much wider range to accommodate all elements without cropping)
        fig.update_layout(
            title="CSTR Process Flow Diagram",
            xaxis=dict(range=[-1, 17], showgrid=False, showticklabels=False),
            yaxis=dict(range=[-1, 6], showgrid=False, showticklabels=False),
            showlegend=False,
            width=1200,
            height=650,
            plot_bgcolor='white'
        )
        
        return fig
    
    def create_results_charts(self, results: Dict):
        """Create visualization charts for simulation results"""
        if not results:
            return None
        
        # Create single plot for concentrations only
        fig = go.Figure()
        
        # Concentrations bar chart
        if 'concentrations' in results:
            components = list(results['concentrations'].keys())
            concentrations = list(results['concentrations'].values())
            colors = ['red' if comp == self.simulator.target_product else 'steelblue' for comp in components]
            
            fig.add_trace(
                go.Bar(x=components, y=concentrations, name="Concentrations", 
                      marker_color=colors, showlegend=False)
            )
        
        fig.update_layout(
            title="Component Concentrations",
            xaxis_title="Components",
            yaxis_title="Concentration (mol/m³)",
            height=400,
            font=dict(size=12)
        )
        
        return fig
    
    def matplotlib_to_plotly(self, fig_mpl):
        """Convert matplotlib figure to plotly for better web integration"""
        # Save matplotlib figure to bytes
        img_buffer = io.BytesIO()
        fig_mpl.savefig(img_buffer, format='png', dpi=150, bbox_inches='tight')
        img_buffer.seek(0)
        img_b64 = base64.b64encode(img_buffer.read()).decode()
        
        # Create plotly figure with the image
        fig_plotly = go.Figure()
        fig_plotly.add_layout_image(
            dict(
                source=f"data:image/png;base64,{img_b64}",
                xref="paper", yref="paper",
                x=0, y=1,
                sizex=1, sizey=1,
                sizing="stretch",
                opacity=1,
                layer="below"
            )
        )
        fig_plotly.update_xaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig_plotly.update_yaxes(showgrid=False, showticklabels=False, zeroline=False)
        fig_plotly.update_layout(
            xaxis=dict(range=[0, 1]),
            yaxis=dict(range=[0, 1]),
            width=800,
            height=600,
            margin=dict(l=0, r=0, t=0, b=0)
        )
        
        plt.close(fig_mpl)  # Close matplotlib figure
        return fig_plotly

def main():
    st.set_page_config(page_title="CSTR Simulator", layout="wide")
    
    app = StreamlitCSTRApp()
    
    st.title("🧪 CSTR Simulator with Process Flow Visualization")
    st.markdown("---")
    
    # Sidebar for inputs
    with st.sidebar:
        st.header("Simulation Parameters")
        
        # Reaction selection
        reaction_names = app.database.get_reaction_names()
        selected_reaction = st.selectbox("Select Reaction:", reaction_names)
        reaction_data = app.database.get_reaction_details(selected_reaction)
        
        st.subheader("Reactor Parameters")
        volume = st.number_input("Reactor Volume (m³):", min_value=0.1, value=5.0, step=0.1)
        flow_rate = st.number_input("Feed Flow Rate (m³/s):", min_value=0.001, value=0.02, step=0.001)
        recycle_ratio = st.slider("Recycle Ratio:", min_value=0.0, max_value=0.9, value=0.2, step=0.05)
        
        temp_range = reaction_data['temperature_range']
        temperature = st.slider(
            "Temperature (K):", 
            min_value=temp_range[0], 
            max_value=temp_range[1], 
            value=(temp_range[0] + temp_range[1]) // 2,
            step=5
        )
        
        optimize_temp = st.checkbox("Optimize Temperature", value=True)
        
        run_simulation = st.button("🚀 Run Simulation", type="primary")
    
    # Main content area
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Process Flow Diagram")
        
        # Collect parameters
        params = {
            'volume': volume,
            'flow_rate': flow_rate,
            'recycle_ratio': recycle_ratio,
            'temperature': temperature,
            'optimize_temp': optimize_temp
        }
        
        # Run simulation if button pressed
        results = None
        if run_simulation:
            with st.spinner("Running simulation..."):
                try:
                    # Set up simulator with actual parameters
                    app.simulator.set_parameters(
                        volume=volume,
                        temperature=temperature, 
                        flow_rate=flow_rate,
                        reactions=reaction_data['reactions'],
                        feed_composition=reaction_data['feed_composition'],
                        recycle_ratio=recycle_ratio,
                        target_product=reaction_data['target_product'],
                        catalyst=reaction_data['catalyst']
                    )
                    
                    # Run actual simulation
                    results = app.simulator.run_simulation(
                        optimize_temp=optimize_temp, 
                        temp_bounds=temp_range
                    )
                    
                    st.session_state['results'] = results
                    st.success("Simulation completed successfully!")
                    
                except Exception as e:
                    st.error(f"Simulation failed: {str(e)}")
                    
        elif 'results' in st.session_state:
            results = st.session_state['results']
        
        # Display process flow chart
        flow_chart = app.create_process_flowchart(reaction_data, params, results)
        st.plotly_chart(flow_chart, use_container_width=True)
    
    with col2:
        st.subheader("Reaction Details")
        
        # Display reaction information
        st.write(f"**Description:** {reaction_data['description']}")
        st.write(f"**Target Product:** {reaction_data['target_product']}")
        st.write(f"**Catalyst:** {reaction_data['catalyst']}")
        st.write(f"**Temperature Range:** {temp_range[0]}-{temp_range[1]} K")
        
        st.write("**Reactions:**")
        for i, reaction in enumerate(reaction_data['reactions']):
            st.write(f"{i+1}. {reaction['name']}")
            
            # Format stoichiometry
            reactants = []
            products = []
            for comp, coef in reaction['stoichiometry'].items():
                if coef < 0:
                    if coef == -1:
                        reactants.append(f"{comp}")
                    else:
                        reactants.append(f"{abs(coef)} {comp}")
                else:
                    if coef == 1:
                        products.append(f"{comp}")
                    else:
                        products.append(f"{coef} {comp}")
            
            stoich_str = " + ".join(reactants) + " → " + " + ".join(products)
            st.write(f"   {stoich_str}")
            
            if reaction.get('reversible', False):
                st.write("   *(Reversible reaction)*")
        
        st.write("**Feed Composition:**")
        feed_df = pd.DataFrame([
            {"Component": comp, "Concentration (mol/m³)": conc} 
            for comp, conc in reaction_data['feed_composition'].items()
        ])
        st.dataframe(feed_df, hide_index=True)
    
    # Results section
    if results:
        st.markdown("---")
        st.subheader("Simulation Results")
        
        # Key metrics in columns (removed mass balance error)
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Optimal Temperature", f"{results['temperature']:.1f} K")
        with col2:
            st.metric("Product Yield", f"{results['yield']*100:.1f}%")
        with col3:
            st.metric("Residence Time", f"{results['residence_time']:.1f} s")
        
        # Detailed results in tabs (removed reaction rates and conversions)
        tab1, tab2, tab3 = st.tabs(["📊 Component Concentrations", "🔬 Original Plots", "🧮 Detailed Data"])
        
        with tab1:
            charts = app.create_results_charts(results)
            if charts:
                st.plotly_chart(charts, use_container_width=True)
        
        with tab2:
            # Use the original matplotlib visualization from your code
            st.write("**Original CSTR Visualization (from your simulator):**")
            fig_mpl, axes = app.simulator.create_visualization(results)
            
            # Convert matplotlib to plotly for better web display
            fig_plotly = app.matplotlib_to_plotly(fig_mpl)
            st.plotly_chart(fig_plotly, use_container_width=True)
        
        with tab3:
            col1, col2 = st.columns(2)
            
            with col1:
                st.write("**Steady State Concentrations (mol/m³):**")
                conc_df = pd.DataFrame([
                    {"Component": comp, 
                     "Concentration": f"{conc:.4f}",
                     "Is Target": "✓" if comp == reaction_data['target_product'] else ""}
                    for comp, conc in results['concentrations'].items()
                ])
                st.dataframe(conc_df, hide_index=True)
            
            with col2:
                st.write("**Recycle Stream Concentrations (mol/m³):**")
                recycle_df = pd.DataFrame([
                    {"Component": comp, "Concentration": f"{conc:.4f}"}
                    for comp, conc in results['recycle_stream'].items()
                ])
                st.dataframe(recycle_df, hide_index=True)
            
            # Show reaction rates and conversions in this tab
            st.write("**Reaction Rates (mol/m³·s):**")
            rates_df = pd.DataFrame([
                {"Reaction": name.split(':')[1].strip() if ':' in name else name, 
                 "Rate": f"{rate:.6f}"}
                for name, rate in results['reaction_rates'].items()
            ])
            st.dataframe(rates_df, hide_index=True)
            
            st.write("**Reactant Conversions:**")
            conv_df = pd.DataFrame([
                {"Component": comp, "Conversion": f"{conv*100:.2f}%"}
                for comp, conv in results['conversions'].items()
                if comp in reaction_data['feed_composition']
            ])
            st.dataframe(conv_df, hide_index=True)
        
        # Additional detailed results
        with st.expander("📋 Detailed Results Summary"):
            st.write("**Mass Balance Information:**")
            if "elemental_balance" in results:
                eb = results["elemental_balance"]
                st.write(f"- Total Input Concentration: {eb['total_input_conc']:.4f} mol/m³")
                st.write(f"- Total Output Concentration: {eb['total_output_conc']:.4f} mol/m³")
                st.write(f"- Difference: {eb['difference_percent']:.4f}%")
            
            st.write(f"**Reactor Design:**")
            st.write(f"- Volume: {params['volume']} m³")
            st.write(f"- Flow Rate: {params['flow_rate']} m³/s")
            st.write(f"- Residence Time: {results['residence_time']:.2f} s")
            st.write(f"- Recycle Ratio: {params['recycle_ratio']*100:.1f}%")
            
            if results.get('catalyst'):
                st.write(f"**Catalyst:** {results['catalyst']}")

if __name__ == "__main__":
    main()