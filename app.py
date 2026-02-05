"""
Carbon Footprint Prediction Web Application
Built with Streamlit
"""
import streamlit as st
import pandas as pd
import os
import pickle
from data_loader import CarbonFootprintDataLoader
from train_model import CarbonFootprintModel
from tip_generator import TipGenerator
import plotly.graph_objects as go
import plotly.express as px


# Page configuration
st.set_page_config(
    page_title="Carbon Footprint Predictor",
    page_icon="🌍",
    layout="wide"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 3rem;
        color: #2E7D32;
        text-align: center;
        margin-bottom: 2rem;
    }
    .sub-header {
        font-size: 1.5rem;
        color: #388E3C;
        margin-top: 2rem;
        margin-bottom: 1rem;
    }
    .metric-card {
        background-color: #E8F5E9;
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
    }
    .tip-box {
        background-color: #FFF9C4;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #FBC02D;
        margin: 0.5rem 0;
        color: #000000;
    }
    .what-if-box {
        background-color: #E3F2FD;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #1976D2;
        margin: 0.5rem 0;
        color: #000000;
    }
    .importance-box {
        background-color: #F3E5F5;
        padding: 1rem;
        border-radius: 8px;
        border-left: 4px solid #7B1FA2;
        margin: 0.5rem 0;
        color: #000000;
    }
</style>
""", unsafe_allow_html=True)


@st.cache_resource
def load_model_and_preprocessor():
    """Load trained model and preprocessor"""
    model = CarbonFootprintModel()
    loader = CarbonFootprintDataLoader()
    
    model_path = 'models/carbon_footprint_model.pkl'
    preprocessor_path = 'models/preprocessor.pkl'
    
    if os.path.exists(model_path) and os.path.exists(preprocessor_path):
        model.load_model(model_path)
        loader.load_preprocessor(preprocessor_path)
        return model, loader
    else:
        st.error("❌ Model not found! Please train the model first by running 'train_model.py'")
        st.stop()


def create_gauge_chart(value, title, max_value=16):
    """Create a gauge chart for carbon footprint"""
    # Determine color based on value (matching impact level thresholds)
    if value > 9.5:
        color = "#D32F2F"  # Red (High)
    elif value >= 7:
        color = "#F57C00"  # Orange (Medium)
    else:
        color = "#388E3C"  # Green (Low)
    
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=value,
        title={'text': title, 'font': {'size': 20}},
        number={'suffix': " kg CO₂", 'font': {'size': 30}},
        gauge={
            'axis': {'range': [None, max_value], 'tickwidth': 1},
            'bar': {'color': color},
            'steps': [
                {'range': [0, 7], 'color': "#C8E6C9"},     # Low - Green
                {'range': [7, 9.5], 'color': "#FFE082"},   # Medium - Yellow
                {'range': [9.5, max_value], 'color': "#FFCDD2"}  # High - Red
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': value
            }
        }
    ))
    
    fig.update_layout(height=300, margin=dict(l=20, r=20, t=50, b=20))
    return fig


def create_what_if_chart(what_if_results):
    """Create bar chart for what-if analysis"""
    if not what_if_results:
        return None
    
    df = pd.DataFrame(what_if_results)
    
    fig = px.bar(
        df,
        x='savings',
        y='change',
        orientation='h',
        title='Potential CO₂ Savings by Making Changes',
        labels={'savings': 'CO₂ Savings (kg)', 'change': ''},
        color='savings',
        color_continuous_scale='Greens'
    )
    
    fig.update_layout(
        height=400,
        showlegend=False,
        yaxis={'categoryorder': 'total ascending'}
    )
    
    return fig


def main():
    # Header
    st.markdown('<h1 class="main-header">🌍 Personal Carbon Footprint Predictor</h1>', unsafe_allow_html=True)
    st.markdown("### Predict your carbon footprint and get personalized tips to reduce it!")
    
    # Load model
    model, loader = load_model_and_preprocessor()
    tip_gen = TipGenerator(model, loader)
    
    # Center section for user inputs
    st.markdown('<h2 class="sub-header">📝 Enter Your Lifestyle Information</h2>', unsafe_allow_html=True)
    
    col1, col2 = st.columns(2)
    
    with col1:
        # Transport Mode
        transport_mode = st.selectbox(
            "🚗 How do you usually travel?",
            options=['Car', 'Bus', 'Bike', 'EV', 'Walk'],
            help="Select your primary mode of transportation"
        )
        
        # Distance
        distance_km = st.slider(
            "🛣️ Average daily travel distance (km)",
            min_value=0.0,
            max_value=100.0,
            value=10.0,
            step=0.5,
            help="Total distance you travel per day"
        )
        
        # Electricity Usage
        electricity_kwh = st.slider(
            "💡 Daily electricity usage (kWh)",
            min_value=0.0,
            max_value=20.0,
            value=7.0,
            step=0.5,
            help="Average household uses 5-10 kWh per day"
        )
    
    with col2:
        # Food Type
        food_type = st.selectbox(
            "🍽️ What's your diet type?",
            options=['Non-Veg', 'Mixed', 'Veg'],
            help="Non-Veg: Meat-based, Mixed: Balanced, Veg: Plant-based"
        )
        
        # Screen Time
        screen_time_hours = st.slider(
            "📱 Daily screen time (hours)",
            min_value=0.0,
            max_value=24.0,
            value=6.0,
            step=0.5,
            help="Total hours spent on electronic devices per day"
        )
    
    # Predict button
    st.markdown("<br>", unsafe_allow_html=True)
    if st.button("🔮 Calculate My Carbon Footprint", type="primary", use_container_width=True):
        # Prepare input
        user_input = {
            'transport_mode': transport_mode,
            'distance_km': distance_km,
            'electricity_kwh': electricity_kwh,
            'food_type': food_type,
            'screen_time_hours': screen_time_hours
        }
        
        # Preprocess and predict with food ordering correction
        X_preprocessed = loader.preprocess_user_input(user_input)
        carbon_footprint = model.predict_footprint_corrected(X_preprocessed, food_type=food_type)
        impact_level = model.classify_impact_level(carbon_footprint)
        
        # Store in session state
        st.session_state['prediction'] = {
            'footprint': carbon_footprint,
            'impact_level': impact_level,
            'user_input': user_input,
            'X_preprocessed': X_preprocessed
        }
    
    # Display results
    if 'prediction' in st.session_state:
        pred = st.session_state['prediction']
        
        st.markdown("---")
        
        # Main results
        col1, col2, col3 = st.columns([2, 1, 1])
        
        with col1:
            # Gauge chart
            fig = create_gauge_chart(pred['footprint'], "Your Carbon Footprint")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            st.metric("Impact Level", pred['impact_level'])
            st.markdown('</div>', unsafe_allow_html=True)
        
        with col3:
            st.markdown('<div class="metric-card">', unsafe_allow_html=True)
            yearly = pred['footprint'] * 365
            st.metric("Yearly Footprint", f"{yearly:.0f} kg CO₂")
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Generate all tips
        all_tips = tip_gen.generate_all_tips(
            pred['user_input'],
            pred['footprint'],
            pred['X_preprocessed']
        )
        
        # Tabs for different tip levels
        tab1, tab2, tab3 = st.tabs([
            "💡 Quick Tips",
            "🔄 What-If Analysis",
            "📊 Your Top Impact Factors"
        ])
        
        with tab1:
            st.markdown('<h2 class="sub-header">💡 Personalized Quick Tips</h2>', unsafe_allow_html=True)
            st.write("Based on your lifestyle, here are some actionable tips:")
            
            for i, tip in enumerate(all_tips['level_1_rules'], 1):
                st.markdown(f'<div class="tip-box"><strong>Tip {i}:</strong> {tip}</div>', unsafe_allow_html=True)
        
        with tab2:
            st.markdown('<h2 class="sub-header">🔄 What-If Scenarios</h2>', unsafe_allow_html=True)
            st.write("See how much you could save by making these changes:")
            
            what_if_results = all_tips['level_2_what_if']
            
            if what_if_results:
                # Show chart
                fig = create_what_if_chart(what_if_results)
                if fig:
                    st.plotly_chart(fig, use_container_width=True)
                
                # Show detailed results
                for i, result in enumerate(what_if_results[:5], 1):  # Top 5
                    st.markdown(f"""
                    <div class="what-if-box">
                        <strong>{result['icon']} {result['change']}</strong><br>
                        💚 Save <strong>{result['savings']:.2f} kg CO₂</strong> per day<br>
                        📉 New footprint: {result['new_footprint']:.2f} kg CO₂
                    </div>
                    """, unsafe_allow_html=True)
            else:
                st.success("🎉 You're already making great choices! Your footprint is well-optimized.")
        
        with tab3:
            st.markdown('<h2 class="sub-header">📊 Your Top Contributing Factors</h2>', unsafe_allow_html=True)
            st.write("These factors have the biggest impact on your carbon footprint:")
            
            importance_tips = all_tips['level_3_importance']
            
            for i, tip_data in enumerate(importance_tips, 1):
                st.markdown(f"""
                <div class="importance-box">
                    <strong>Factor {i}: {tip_data['category'].title()}</strong><br>
                    {tip_data['tip']}
                </div>
                """, unsafe_allow_html=True)
        
        # Summary section
        st.markdown("---")
        st.markdown('<h2 class="sub-header">🎯 Your Action Plan</h2>', unsafe_allow_html=True)
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("### 🌟 Immediate Actions")
            st.write("Start with these high-impact changes:")
            if what_if_results:
                for result in what_if_results[:3]:
                    st.write(f"• {result['change']} - Save {result['savings']:.2f} kg CO₂/day")
            else:
                st.success("Keep up your current habits!")
        
        with col2:
            st.markdown("### 📈 Potential Impact")
            if what_if_results:
                total_savings = sum(r['savings'] for r in what_if_results[:3])
                st.metric("Daily Savings Potential", f"{total_savings:.2f} kg CO₂")
                st.metric("Yearly Impact", f"{total_savings * 365:.2f} kg CO₂")
                st.write("That's equivalent to:")
                st.write(f"🌳 Planting {int(total_savings * 365 / 20)} trees!")
            else:
                st.success("You're already at optimal levels!")
    
    # Show example scenarios at the bottom
    st.markdown("---")
    st.markdown("### 📊 Example Scenarios")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.markdown("#### 🌱 Eco-Warrior")
        st.write("- Transport: Bike")
        st.write("- Diet: Veg")
        st.write("- Low Electricity")
        st.success("Footprint: ~3-5 kg CO₂/day")
    
    with col2:
        st.markdown("#### ⚖️ Balanced")
        st.write("- Transport: Bus")
        st.write("- Diet: Mixed")
        st.write("- Moderate Usage")
        st.warning("Footprint: ~6-8 kg CO₂/day")
    
    with col3:
        st.markdown("#### ⚠️ High Impact")
        st.write("- Transport: Car")
        st.write("- Diet: Non-Veg")
        st.write("- High Electricity")
        st.error("Footprint: ~10-15 kg CO₂/day")
    
    # Footer
    st.markdown("---")
    st.markdown("""
    <div style='text-align: center; color: #666;'>
        <p>🌍 Carbon Footprint Predictor | Built with ML & Streamlit</p>
        <p><small>Data-driven insights to help you reduce your environmental impact</small></p>
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
