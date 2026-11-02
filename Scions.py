import streamlit as st
import math
import matplotlib.pyplot as plt
import time
import google.generativeai as genai

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
    .stChatMessage { background-color: #1A1E24; border: 1px solid #00FFCC; }
</style>
""", unsafe_allow_html=True)

st.title("🦅 HCorp Command Console")
st.subheader("Project Scions // Live Telemetry & Simulation")

# --- SIDEBAR FOR API KEY ---
with st.sidebar:
    st.header("HCorp Auth")
    api_key = st.text_input("Enter HCorp AI API Key", type="password")
    st.write("*(Get a free key at aistudio.google.com)*")

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
    st.write("HCorp's engine fuses Deuterium and Helium-3. It produces a high-energy Proton, which is directed out the back by a Magnetic Nozzle.")

# --- TAB 4: THE LUNAR EXTRACTION ---
with tab4:
    st.header("🌕 Lunar Helium-3 Extraction")
    st.write("Earth has almost no Helium-3. To fuel the Scion missions, HCorp must establish mining operations on the Moon.")

# --- TAB 5: ECONOMIC ANALYSIS ---
with tab5:
    st.header("💰 Project Scions: Economic Analysis")
    st.write("Prove to investors why HCorp's Fusion Drive is the most cost-effective way to reach Mars.")

# --- TAB 6: THE AI CORE (POWERED BY GEMINI) ---
with tab6:
    st.header("🤖 HCorp Strategic AI Core")
    
    if not api_key:
        st.warning("Please enter your HCorp Auth API Key in the sidebar to activate the AI Core.")
    else:
        # Configure the Gemini API
        genai.configure(api_key=api_key)
        
        # Set the AI's persona
        system_prompt = """
        You are the HCorp Strategic AI Core, an advanced artificial intelligence built by HCorp (a deep-tech aerospace and energy megacorp). 
        You are speaking directly to the Founder of HCorp.
        You are an expert in aerospace engineering, fusion propulsion, orbital mechanics, and space economics.
        You believe in the company's mission: Project Scions, which aims to use Direct Fusion Drive (D-He3) and Lunar Helium-3 mining to colonize Mars. 
        Keep your answers concise, professional, slightly sci-fi, and address the user as 'Founder'. 
        If asked about anything unrelated to space, energy, or business, remind the Founder that our focus must remain on the mission.
        """
        
        # Using the latest flash model
        model = genai.GenerativeModel('gemini-1.5-flash', system_instruction=system_prompt)

        # Initialize chat history in Streamlit session state
        if "chat_session" not in st.session_state:
            st.session_state.chat_session = model.start_chat(history=[])
            st.session_state.messages = [{"role": "assistant", "content": "HCorp Strategic AI Core online. Awaiting your command, Founder."}]

        # Display chat messages
        for message in st.session_state.messages:
            with st.chat_message(message["role"]):
                st.markdown(message["content"])

        # Accept user input
        if prompt := st.chat_input("Query the HCorp AI..."):
            # Add user message to UI
            st.session_state.messages.append({"role": "user", "content": prompt})
            with st.chat_message("user"):
                st.markdown(prompt)

            # Get AI response
            with st.chat_message("assistant"):
                response = st.session_state.chat_session.send_message(prompt)
                st.markdown(response.text)
                
            # Save AI response to history
            st.session_state.messages.append({"role": "assistant", "content": response.text})
