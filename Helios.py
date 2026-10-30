import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="HCorp Project Helios v0.7", page_icon="🌕", layout="wide")

st.title("🚀 HCorp Systems: Project Helios v0.7")

# Create three tabs
tab1, tab2, tab3 = st.tabs(["📊 Mission Calculator", "⚛️ Fusion Physics", "🌕 Lunar Extraction"])

# --- TAB 1: THE CALCULATOR ---
with tab1:
    st.header("1. Mission Architecture")
    launch_mode = st.radio("Select Launch Architecture:", ["Single Launch from Earth", "Orbital Assembly (In Space)"])
    launch_ratio = math.exp(9400 / 4500) 

    if "Single Launch" in launch_mode:
        st.write(f"**Launch Mass Ratio:** {launch_ratio:.2f}")
    else:
        st.write("**Launch Mass Ratio: N/A** (Assembled in space).")

    st.write("---")
    st.header("Phase 2: LEO to Mars Transit")
    days = st.slider("Desired Mars Transit Time (Days)", min_value=10, max_value=120, value=30, step=1)
    transit_dv = 225000 / days
    
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

    # Graph
    days_range = list(range(10, 121, 5))
    fig, ax = plt.subplots(figsize=(10, 3))
    colors = {"Chemical Rocket": "red", "Nuclear Thermal": "orange", "HCorp Fusion Drive": "green"}
    for engine_name, exhaust_velocity in ENGINES.items():
        total_ratios = []
        for d in days_range:
            t_dv = 225000 / d
            t_ratio = math.exp(t_dv / exhaust_velocity)
            total_r = launch_ratio * t_ratio if "Single Launch" in launch_mode else t_ratio
            total_fuel_pct = ((total_r - 1) / total_r) * 100
            total_ratios.append(min(total_fuel_pct, 100)) 
        ax.plot(days_range, total_ratios, label=engine_name, color=colors[engine_name], linewidth=3)
    ax.set_ylim(0, 105)
    ax.set_xlabel("Mars Transit Time (Days)")
    ax.set_ylabel("Fuel Weight (%)")
    ax.grid(True, linestyle='--', alpha=0.7)
    ax.legend()
    st.pyplot(fig)

# --- TAB 2: THE PHYSICS ---
with tab2:
    st.header("The HCorp Direct Fusion Drive (DFD)")
    st.write("""
    To achieve a 30-day transit to Mars, HCorp is researching **Direct Fusion Drive (DFD)** technology. 
    Unlike chemical rockets, which are limited by chemical bond energy, DFD uses the Strong Nuclear Force.
    """)
    st.subheader("1. The Fuel: D-He3")
    st.write("""
    HCorp's engine will fuse **Deuterium (D)** and **Helium-3 (He-3)**. This reaction produces a high-energy **Proton** and Helium-4. 
    *   **Deuterium** is extracted from seawater on Earth.
    *   **Helium-3** is rare on Earth, but abundant on the Lunar surface.
    """)
    st.subheader("2. The Magnetic Nozzle")
    st.write("""
    Because the fusion plasma reaches temperatures over 100,000 degrees Celsius, no physical metal nozzle could survive. 
    Instead, HCorp uses superconducting magnets to create a **Magnetic Nozzle**. 
    The magnetic field catches the charged Protons and directs them out the back of the ship.
    """)

# --- TAB 3: THE LUNAR EXTRACTION ---
with tab3:
    st.header("🌕 Lunar Helium-3 Extraction")
    st.write("""
    Earth has almost no Helium-3. To fuel the HCorp Fusion Drive, HCorp must establish mining operations on the Moon. 
    The Moon's regolith has been bombarded by solar wind for billions of years, trapping Helium-3 in the dust.
    """)
    
    st.subheader("Lunar Mining Calculator")
    st.write("Calculate how much lunar regolith must be processed to fuel a single Mars mission.")
    
    # Inputs
    he3_per_mission = st.number_input("Helium-3 required per Mars mission (in metric tons):", min_value=1.0, max_value=100.0, value=25.0, step=1.0)
    concentration = st.number_input("He-3 concentration in regolith (parts per billion - ppb):", min_value=1.0, max_value=50.0, value=20.0, step=1.0)
    
    # Math
    # If concentration is 20 ppb, it means 20 grams per 1,000,000,000 grams (1,000,000 kg or 1,000 metric tons).
    # So, 1 ton of regolith contains (concentration / 1000) kg of He-3.
    # To get 1 ton of He-3, we need (1000 / (concentration / 1000)) tons of regolith.
    # Simplified: (1,000,000 / concentration) tons of regolith per ton of He-3.
    
    regolith_per_ton = 1000000 / concentration
    total_regolith_needed = regolith_per_ton * he3_per_mission
    
    st.metric(label="Regolith to be Processed", value=f"{total_regolith_needed:,.0f} Metric Tons")
    
    st.info(f"""
    **The Challenge:** To fuel one 30-day Mars mission, HCorp rovers would need to excavate and heat {total_regolith_needed:,.0f} tons of lunar dirt. 
    This is why HCorp is also researching compact nuclear fission reactors to power the massive lunar mining equipment, as solar power cannot survive the 14-day lunar night.
    """)
