import streamlit as st
import math
import matplotlib.pyplot as plt
import time

# --- CUSTOM HCORP CSS (MAKES IT LOOK ALIVE) ---
st.set_page_config(page_title="HCorp Command Console", page_icon="🦅", layout="wide")

st.markdown("""
<style>
    /* Dark Theme */
    .stApp {
        background-color: #0E1117;
        color: #00FFCC;
    }
    /* Glowing Text */
    h1, h2, h3, p, div {
        font-family: 'Courier New', Courier, monospace !important;
    }
    .stButton>button {
        background-color: #00FFCC;
        color: black;
        border: 2px solid #00FFCC;
        font-weight: bold;
        box-shadow: 0px 0px 15px #00FFCC;
    }
    .stButton>button:hover {
        background-color: black;
        color: #00FFCC;
    }
    /* Custom Alert Box */
    .stAlert {
        background-color: rgba(0, 255, 204, 0.1);
        border: 1px solid #00FFCC;
    }
</style>
""", unsafe_allow_html=True)

st.title("🦅 HCorp Command Console")
st.subheader("Project Scions // Live Telemetry & Simulation")

tab1, tab2, tab3, tab4, tab5 = st.tabs([
    "🖥️ Mission Control", 
    "🚀 Live Launch Sim", 
    "⚛️ Fusion Physics", 
    "🌕 Lunar Extraction", 
    "💰 Economic Analysis"
])

# --- TAB 1: MISSION CONTROL ---
with tab1:
    st.header("1. Scion Mission Architecture")
    launch_mode = st.radio("Select Launch Architecture:", ["Single Launch from Earth", "Orbital Assembly (In Space)"])
    launch_ratio = math.exp(9400 / 4500) 

    st.write("---")
    st.header("Phase 2: LEO to Mars Transit")
    
    distance_mkm = st.slider("Distance to Mars (Million Kilometers)", min_value=55, max_value=400, value=55, step=5)
    days = st.slider("Desired Mars Transit Time (Days)", min_value=1, max_value=120, value=16, step=1)
    
    distance_meters = distance_mkm * 10**9
    time_seconds = days * 24 * 3600
    transit_dv = (4 * distance_meters) / time_seconds
    
    ENGINES = {"Chemical Rocket": 4500, "Nuclear Thermal": 9000, "HCorp Fusion Drive": 100000}
    col1, col2, col3 = st.columns(3)
    columns = [col1, col2, col3]

    for i, (engine_name, exhaust_velocity) in enumerate(ENGINES.items()):
        transit_ratio = math.exp(transit_dv / exhaust_velocity)
        with columns[i]:
            st.subheader(engine_name)
            st.metric(label="Transit Mass Ratio", value=f"{transit_ratio:.2f}")
            total_ratio = (launch_ratio * transit_ratio) if "Single Launch" in launch_mode else transit_ratio
            fuel_pct = ((total_ratio - 1) / total_ratio) * 100
            st.write(f"*(Fuel Weight: {fuel_pct:.1f}%)*")
            if total_ratio > 15: st.error("CRITICAL: Structurally impossible.")
            elif total_ratio > 5: st.warning("HIGH FUEL: Payload limited.")
            else: st.success("OPTIMAL: Massive payload capacity.")

    st.write("---")
    st.header("Phase 3: Human Physiology (G-Force Limits)")
    acceleration = (4 * distance_meters) / (time_seconds**2)
    g_force = acceleration / 9.81
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.metric(label="Sustained Acceleration", value=f"{acceleration:.2f} m/s²")
    with col_g2:
        st.metric(label="Sustained G-Force", value=f"{g_force:.2f} G")

# --- TAB 2: LIVE LAUNCH SIMULATION ---
with tab2:
    st.header("🚀 Live Transit Simulation")
    st.write("Run a live, second-by-second simulation of the HCorp Fusion Drive accelerating to Mars.")
    
    sim_distance = st.slider("Simulation Distance (Million km)", min_value=55, max_value=400, value=55)
    sim_days = st.slider("Simulation Transit Time (Days)", min_value=5, max_value=60, value=16)
    
    if st.button("INITIATE SCION LAUNCH SEQUENCE"):
        st.write("**HCorp OS: Launch sequence initiated...**")
        
        # Set up the live chart
        chart_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        # Simulation variables
        total_seconds = sim_days * 24 * 3600
        dv = (4 * (sim_distance * 10**9)) / total_seconds
        v_max = dv / 2
        
        # Generate data for the animation
        steps = 100
        distances = []
        velocities = []
        
        for i in range(steps + 1):
            # Calculate time progression
            current_time = (total_seconds / 2) * (i / steps)
            
            # Acceleration phase
            if i <= 50:
                a = dv / total_seconds
                v = a * current_time
                d = 0.5 * a * (current_time**2)
            # Deceleration phase
            else:
                a = -(dv / total_seconds)
                t_dec = current_time - (total_seconds / 2)
                v = v_max + (a * t_dec)
                d = (0.5 * (dv / total_seconds) * ((total_seconds/2)**2)) + (v_max * t_dec) + (0.5 * a * (t_dec**2))
            
            distances.append(d / 10**9) # Convert to million km
            velocities.append(v)
            
            # Update UI
            if i % 5 == 0 or i == steps:
                fig, ax = plt.subplots(figsize=(10, 3))
                fig.patch.set_facecolor('#0E1117')
                ax.set_facecolor('#0E1117')
                
                # Plot distance
                ax.plot(distances, velocities, color='#00FFCC', linewidth=3)
                ax.set_title("Ship Velocity vs Distance (Million km)", color='white')
                ax.set_xlabel("Distance to Mars (Million km)", color='white')
                ax.set_ylabel("Velocity (m/s)", color='white')
                ax.tick_params(colors='white')
                ax.grid(True, color='gray', linestyle='--', alpha=0.3)
                
                # Set bounds
                ax.set_xlim(0, sim_distance)
                ax.set_ylim(0, v_max * 1.1)
                
                chart_placeholder.pyplot(fig)
                progress_bar.progress(i / steps)
                time.sleep(0.05) # Animation speed
                
        st.success("Orbital insertion at Mars complete. Welcome to the Scions.")

# --- TAB 3: THE PHYSICS ---
with tab3:
    st.header("The HCorp Direct Fusion Drive (DFD)")
    st.write("""
    To achieve the Scion mission timeline, HCorp is researching **Direct Fusion Drive (DFD)** technology. 
    Unlike chemical rockets, which are limited by chemical bond energy, DFD uses the Strong Nuclear Force.
    """)

# --- TAB 4: THE LUNAR EXTRACTION ---
with tab4:
    st.header("🌕 Lunar Helium-3 Extraction")
    st.write("Earth has almost no Helium-3. To fuel the Scion missions, HCorp must establish mining operations on the Moon.")

# --- TAB 5: ECONOMIC ANALYSIS ---
with tab5:
    st.header("💰 Project Scions: Economic Analysis")
    st.write("Prove to investors why HCorp's Fusion Drive is the most cost-effective way to reach Mars.")
