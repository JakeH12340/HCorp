import streamlit as st
import math
import matplotlib.pyplot as plt
import time
import random

# --- CUSTOM HCORP CSS ---
st.set_page_config(page_title="HCorp Command Console", page_icon="🦅", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0E1117; color: #00FFCC; }
    h1, h2, h3, p, div { font-family: 'Courier New', Courier, monospace !important; }
    .stButton>button {
        background-color: #00FFCC; color: black; border: 2px solid #00FFCC;
        font-weight: bold; box-shadow: 0px 0px 15px #00FFCC;
    }
    .stButton>button:hover { background-color: black; color: #00FFCC; }
    .stAlert { background-color: rgba(0, 255, 204, 0.1); border: 1px solid #00FFCC; }
    /* Chat styling */
    .stChatMessage { background-color: #1A1E24; border: 1px solid #00FFCC; }
</style>
""", unsafe_allow_html=True)

st.title("🦅 HCorp Command Console")
st.subheader("Project Scions // Live Telemetry & Simulation")

tab1, tab2, tab3, tab4, tab5, tab6 = st.tabs([
    "🖥️ Mission Control", 
    "🚀 Live Launch Sim", 
    "⚛️ Fusion Physics", 
    "🌕 Lunar Extraction", 
    "💰 Economic Analysis",
    "🤖 HCorp AI Core"
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

# --- TAB 2: LIVE LAUNCH SIMULATION ---
with tab2:
    st.header("🚀 Live Transit Simulation")
    st.write("Run a live, second-by-second simulation of the HCorp Fusion Drive accelerating to Mars.")
    
    sim_distance = st.slider("Simulation Distance (Million km)", min_value=55, max_value=400, value=55)
    sim_days = st.slider("Simulation Transit Time (Days)", min_value=5, max_value=60, value=16)
    
    if st.button("INITIATE SCION LAUNCH SEQUENCE"):
        st.write("**HCorp OS: Launch sequence initiated...**")
        chart_placeholder = st.empty()
        progress_bar = st.progress(0)
        
        total_seconds = sim_days * 24 * 3600
        dv = (4 * (sim_distance * 10**9)) / total_seconds
        v_max = dv / 2
        
        steps = 100
        distances = []
        velocities = []
        
        for i in range(steps + 1):
            current_time = (total_seconds / 2) * (i / steps)
            if i <= 50:
                a = dv / total_seconds
                v = a * current_time
                d = 0.5 * a * (current_time**2)
            else:
                a = -(dv / total_seconds)
                t_dec = current_time - (total_seconds / 2)
                v = v_max + (a * t_dec)
                d = (0.5 * (dv / total_seconds) * ((total_seconds/2)**2)) + (v_max * t_dec) + (0.5 * a * (t_dec**2))
            
            distances.append(d / 10**9)
            velocities.append(v)
            
            if i % 5 == 0 or i == steps:
                fig, ax = plt.subplots(figsize=(10, 3))
                fig.patch.set_facecolor('#0E1117')
                ax.set_facecolor('#0E1117')
                ax.plot(distances, velocities, color='#00FFCC', linewidth=3)
                ax.set_title("Ship Velocity vs Distance (Million km)", color='white')
                ax.set_xlabel("Distance to Mars (Million km)", color='white')
                ax.set_ylabel("Velocity (m/s)", color='white')
                ax.tick_params(colors='white')
                ax.grid(True, color='gray', linestyle='--', alpha=0.3)
                ax.set_xlim(0, sim_distance)
                ax.set_ylim(0, v_max * 1.1)
                chart_placeholder.pyplot(fig)
                progress_bar.progress(i / steps)
                time.sleep(0.05)
                
        st.success("Orbital insertion at Mars complete. Welcome to the Scions.")

# --- TAB 3: THE PHYSICS ---
with tab3:
    st.header("The HCorp Direct Fusion Drive (DFD)")
    st.write("HCorp's engine fuses Deuterium and Helium-3. It produces a high-energy Proton, which is directed out the back by a Magnetic Nozzle, achieving an exhaust velocity of 100,000 m/s.")

# --- TAB 4: THE LUNAR EXTRACTION ---
with tab4:
    st.header("🌕 Lunar Helium-3 Extraction")
    st.write("Earth has almost no Helium-3. To fuel the Scion missions, HCorp must establish mining operations on the Moon.")

# --- TAB 5: ECONOMIC ANALYSIS ---
with tab5:
    st.header("💰 Project Scions: Economic Analysis")
    st.write("Prove to investors why HCorp's Fusion Drive is the most cost-effective way to reach Mars.")

# --- TAB 6: THE AI CORE ---
with tab6:
    st.header("🤖 HCorp Strategic AI Core")
    st.write("Welcome, Founder. I am the HCorp Strategic AI. I am here to assist with mission architecture, risk assessment, and strategic planning for Project Scions.")
    
    # Initialize chat history
    if "messages" not in st.session_state:
        st.session_state.messages = [{"role": "assistant", "content": "HCorp AI Core online. How can I assist you with the Mars colonization protocol today?"}]

    # Display chat messages from history on app rerun
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # Accept user input
    if prompt := st.chat_input("Query the HCorp AI..."):
        # Add user message to chat history
        st.session_state.messages.append({"role": "user", "content": prompt})
        # Display user message in chat message container
        with st.chat_message("user"):
            st.markdown(prompt)

        # Generate AI response based on keywords
        prompt_lower = prompt.lower()
        response = ""
        
        if "chemical" in prompt_lower or "rocket" in prompt_lower:
            response = "Analysis: Chemical rockets are structurally impossible for fast transit. At 55M km, a 16-day transit requires a mass ratio of 2.2 quadrillion. We would need more fuel than exists in the solar system. Recommend immediate shift to Fusion."
        elif "fusion" in prompt_lower or "hcorp" in prompt_lower:
            response = "Analysis: The HCorp Direct Fusion Drive is the only mathematically viable solution. Using Deuterium-He3 fusion, we achieve an exhaust velocity of 100,000 m/s. A 16-day transit requires a mass ratio of only 4.91. Payload capacity is massive."
        elif "cost" in prompt_lower or "money" in prompt_lower or "economy" in prompt_lower:
            response = "Analysis: Launching chemical fuel costs $429M per mission. The HCorp Fusion Drive reduces mission costs to $11.6M. Over a decade of Martian colonization, this saves trillions. ROI is astronomical."
        elif "moon" in prompt_lower or "helium" in prompt_lower or "fuel" in prompt_lower:
            response = "Analysis: The Moon is our primary Helium-3 mining target. Lunar regolith contains ~20 ppb of He-3. We must deploy nuclear fission-powered mining rovers to excavate and heat the regolith to extract the fuel."
        elif "g-force" in prompt_lower or "crew" in prompt_lower or "human" in prompt_lower:
            response = "Analysis: At 55M km, a 16-day transit produces only 0.01 G of sustained acceleration. The crew will experience microgravity, requiring rigorous exercise regimens to prevent bone density loss. This is optimal for crew safety."
        elif "hello" in prompt_lower or "hi" in prompt_lower:
            response = "HCorp AI Core online. Awaiting your command, Founder."
        elif "who are you" in prompt_lower:
            response = "I am the HCorp Strategic AI Core, a rule-based expert system designed to evaluate mission telemetry and ensure the success of Project Scions."
        elif "help" in prompt_lower:
            response = "I can analyze: 'chemical rockets', 'fusion drive', 'cost/money', 'moon/helium-3', and 'g-force/crew safety'. What parameters shall we review?"
        else:
            response = f"Data not found for '{prompt}'. I am currently trained on Project Scions telemetry. Please ask about Fusion Drives, Chemical Rockets, Mission Costs, Lunar Extraction, or Crew G-Forces."
            
        # Add AI response to chat history
        st.session_state.messages.append({"role": "assistant", "content": response})
        # Display AI response
        with st.chat_message("assistant"):
            st.markdown(response)
