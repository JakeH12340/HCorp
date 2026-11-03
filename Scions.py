import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="HCorp Project Scions", page_icon="🦅", layout="wide")

st.title("🦅 HCorp Systems: Project Scions")
st.subheader("Advanced Propulsion & Solar System Logistics")

tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Mission Calculator", 
    "⚛️ Fusion Physics", 
    "🌕 Lunar Extraction", 
    "💰 Economic Analysis"
])

# --- TAB 1: THE CALCULATOR ---
with tab1:
    st.header("1. Scion Mission Architecture")
    launch_mode = st.radio("Select Launch Architecture:", ["Single Launch from Earth", "Orbital Assembly (In Space)"])
    launch_ratio = math.exp(9400 / 4500) 

    if "Single Launch" in launch_mode:
        st.write(f"**Launch Mass Ratio:** {launch_ratio:.2f}")
    else:
        st.write("**Launch Mass Ratio: N/A** (Assembled in space).")

    st.write("---")
    st.header("Phase 2: LEO to Mars Transit")
    
    # NEW: Distance Slider
    st.write("Earth and Mars orbit the Sun at different speeds. The distance between them changes constantly.")
    distance_mkm = st.slider("Distance to Mars (Million Kilometers)", min_value=55, max_value=400, value=225, step=5)
    
    days = st.slider("Desired Mars Transit Time (Days)", min_value=1, max_value=120, value=30, step=1)
    
    # Brachistochrone Delta-V Math: Delta-V = 4 * Distance / Time
    distance_meters = distance_mkm * 10**9
    time_seconds = days * 24 * 3600
    transit_dv = (4 * distance_meters) / time_seconds
    
    st.write(f"**Required Transit Delta-V:** {transit_dv:,.0f} m/s")
    
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
    st.write("Project Scions utilizes a constant-thrust Brachistochrone trajectory. This calculates the physical forces on the crew.")
    
    # Brachistochrone acceleration math: a = 4 * Distance / Time^2
    acceleration = (4 * distance_meters) / (time_seconds**2)
    g_force = acceleration / 9.81
    
    col_g1, col_g2 = st.columns(2)
    with col_g1:
        st.metric(label="Sustained Acceleration", value=f"{acceleration:.2f} m/s²")
    with col_g2:
        st.metric(label="Sustained G-Force", value=f"{g_force:.2f} G")

    if g_force > 4.0:
        st.error("CRITICAL: Lethal to human crew. Astronauts would not survive the transit.")
    elif g_force > 1.5:
        st.warning("HIGH G: Unsafe for sustained periods. Astronauts risk severe physiological damage.")
    elif g_force < 0.05:
        st.info("MICROGRAVITY: Crew will experience zero-g. Requires rigorous exercise regimens to prevent bone/muscle loss.")
    else:
        st.success("OPTIMAL: Safe for human crew. Provides a comfortable gravity environment.")

    # Graph 1: Fuel Mass
    # To keep the graph clean, we calculate fuel mass at the currently selected distance
    days_range = list(range(1, 121, 2))
    fig, ax = plt.subplots(figsize=(10, 3))
    colors = {"Chemical Rocket": "red", "Nuclear Thermal": "orange", "HCorp Fusion Drive": "green"}
    for engine_name, exhaust_velocity in ENGINES.items():
        total_ratios = []
        for d in days_range:
            t_time = d * 24 * 3600
            t_dv = (4 * distance_meters) / t_time
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
    To achieve the Scion mission timeline, HCorp is researching **Direct Fusion Drive (DFD)** technology. 
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
    Earth has almost no Helium-3. To fuel the Scion missions, HCorp must establish mining operations on the Moon. 
    The Moon's regolith has been bombarded by solar wind for billions of years, trapping Helium-3 in the dust.
    """)
    
    st.subheader("Lunar Mining Calculator")
    he3_per_mission = st.number_input("Helium-3 required per Mars mission (in metric tons):", min_value=1.0, max_value=100.0, value=25.0, step=1.0)
    concentration = st.number_input("He-3 concentration in regolith (parts per billion - ppb):", min_value=1.0, max_value=50.0, value=20.0, step=1.0)
    
    regolith_per_ton = 1000000 / concentration
    total_regolith_needed = regolith_per_ton * he3_per_mission
    
    st.metric(label="Regolith to be Processed", value=f"{total_regolith_needed:,.0f} Metric Tons")
    
    st.info(f"""
    **The Challenge:** To fuel one Scion mission, HCorp rovers would need to excavate and heat {total_regolith_needed:,.0f} tons of lunar dirt. 
    This is why HCorp is also researching compact nuclear fission reactors to power the massive lunar mining equipment.
    """)

# --- TAB 4: ECONOMIC ANALYSIS ---
with tab4:
    st.header("💰 Project Scions: Economic Analysis")
    st.write("Prove to investors why HCorp's Fusion Drive is the most cost-effective way to reach Mars. (Assumes Orbital Assembly).")

    col_a, col_b, col_c, col_d = st.columns(4)
    
    with col_a:
        dry_mass = st.number_input("Ship Dry Mass (Metric Tons):", min_value=10, max_value=5000, value=100, step=10)
    with col_b:
        chem_cost = st.number_input("Chemical Fuel Cost ($/ton):", min_value=100, max_value=50000, value=5000, step=500)
    with col_c:
        he3_cost = st.number_input("Helium-3 Cost ($/ton):", min_value=10000, max_value=5000000, value=500000, step=50000)
    with col_d:
        launch_cost = st.number_input("Cost to Launch 1 Ton to Orbit ($):", min_value=100000, max_value=5000000, value=1000000, step=100000)

    # We will use the 225 million km average for the economic baseline
    dv = 7500 
    chem_ratio = math.exp(dv / 4500)
    fusion_ratio = math.exp(dv / 100000)

    chem_total_mass = dry_mass * chem_ratio
    fusion_total_mass = dry_mass * fusion_ratio

    chem_fuel_mass = chem_total_mass - dry_mass
    fusion_fuel_mass = fusion_total_mass - dry_mass

    chem_fuel_cost = chem_fuel_mass * chem_cost
    fusion_fuel_cost = fusion_fuel_mass * he3_cost

    chem_launch_cost = chem_fuel_mass * launch_cost
    fusion_launch_cost = fusion_fuel_mass * launch_cost

    chem_total = chem_fuel_cost + chem_launch_cost
    fusion_total = fusion_fuel_cost + fusion_launch_cost

    st.write("---")
    st.subheader("Results (30-Day Transit @ 225M km Average)")
    
    res1, res2 = st.columns(2)
    
    with res1:
        st.write("**Chemical Rocket**")
        st.write(f"Fuel Mass: **{chem_fuel_mass:,.1f} tons**")
        st.write(f"Fuel Cost: ${chem_fuel_cost:,.0f}")
        st.write(f"Launch Cost: ${chem_launch_cost:,.0f}")
        st.metric(label="Total Mission Cost", value=f"${chem_total:,.0f}")
        
    with res2:
        st.write("**HCorp Fusion Drive**")
        st.write(f"Fuel Mass: **{fusion_fuel_mass:,.1f} tons**")
        st.write(f"Fuel Cost: ${fusion_fuel_cost:,.0f}")
        st.write(f"Launch Cost: ${fusion_launch_cost:,.0f}")
        st.metric(label="Total Mission Cost", value=f"${fusion_total:,.0f}")

    fig2, ax2 = plt.subplots(figsize=(8, 4))
    bars = ax2.bar(["Chemical Rocket", "HCorp Fusion Drive"], [chem_total, fusion_total], color=['red', 'green'])
    ax2.set_ylabel("Total Mission Cost ($)")
    ax2.set_title("Project Scions: Total Cost (Fuel + Launch)")
    
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval, f"${yval:,.0f}", ha='center', va='bottom')

    st.pyplot(fig2)

    st.info("""
    **The HCorp Advantage:** Even if Helium-3 is incredibly expensive, the HCorp Fusion Drive requires so little fuel mass that it avoids the astronomical cost of launching thousands of tons of chemical fuel into orbit.
    """)
