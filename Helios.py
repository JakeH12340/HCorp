import streamlit as st
import math
import matplotlib.pyplot as plt

st.set_page_config(page_title="HCorp Project Helios v0.8", page_icon="💰", layout="wide")

st.title("🚀 HCorp Systems: Project Helios v0.9")

# Create four tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Mission Calculator", 
    "⚛️ Fusion Physics", 
    "🌕 Lunar Extraction", 
    "💰 Economic Analysis"
])

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
    
    he3_per_mission = st.number_input("Helium-3 required per Mars mission (in metric tons):", min_value=1.0, max_value=100.0, value=25.0, step=1.0)
    concentration = st.number_input("He-3 concentration in regolith (parts per billion - ppb):", min_value=1.0, max_value=50.0, value=20.0, step=1.0)
    
    regolith_per_ton = 1000000 / concentration
    total_regolith_needed = regolith_per_ton * he3_per_mission
    
    st.metric(label="Regolith to be Processed", value=f"{total_regolith_needed:,.0f} Metric Tons")
    
    st.info(f"""
    **The Challenge:** To fuel one 30-day Mars mission, HCorp rovers would need to excavate and heat {total_regolith_needed:,.0f} tons of lunar dirt. 
    This is why HCorp is also researching compact nuclear fission reactors to power the massive lunar mining equipment.
    """)

# --- TAB 4: ECONOMIC ANALYSIS ---
with tab4:
    st.header("💰 Mission Economic Analysis")
    st.write("Prove to investors why HCorp's Fusion Drive is the most cost-effective way to reach Mars. (Assumes Orbital Assembly for a 30-day transit).")

    col_a, col_b, col_c, col_d = st.columns(4)
    
    with col_a:
        dry_mass = st.number_input("Ship Dry Mass (Metric Tons):", min_value=10, max_value=5000, value=100, step=10)
    with col_b:
        chem_cost = st.number_input("Chemical Fuel Cost ($/ton):", min_value=100, max_value=50000, value=5000, step=500)
    with col_c:
        he3_cost = st.number_input("Helium-3 Cost ($/ton):", min_value=10000, max_value=5000000, value=500000, step=50000)
    with col_d:
        launch_cost = st.number_input("Cost to Launch 1 Ton to Orbit ($):", min_value=100000, max_value=5000000, value=1000000, step=100000)

    # Math for 30-day transit
    dv = 7500
    chem_ratio = math.exp(dv / 4500)
    fusion_ratio = math.exp(dv / 100000)

    # Total masses
    chem_total_mass = dry_mass * chem_ratio
    fusion_total_mass = dry_mass * fusion_ratio

    # Fuel masses
    chem_fuel_mass = chem_total_mass - dry_mass
    fusion_fuel_mass = fusion_total_mass - dry_mass

    # Costs
    chem_fuel_cost = chem_fuel_mass * chem_cost
    fusion_fuel_cost = fusion_fuel_mass * he3_cost

    # Launch Costs (You have to launch the fuel!)
    chem_launch_cost = chem_fuel_mass * launch_cost
    fusion_launch_cost = fusion_fuel_mass * launch_cost

    # Total Costs
    chem_total = chem_fuel_cost + chem_launch_cost
    fusion_total = fusion_fuel_cost + fusion_launch_cost

    st.write("---")
    st.subheader("Results (30-Day Transit)")
    
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

    # Bar Chart
    fig2, ax2 = plt.subplots(figsize=(8, 4))
    bars = ax2.bar(["Chemical Rocket", "HCorp Fusion Drive"], [chem_total, fusion_total], color=['red', 'green'])
    ax2.set_ylabel("Total Mission Cost ($)")
    ax2.set_title("Total Cost (Fuel + Launch): 30-Day Mars Transit")
    
    for bar in bars:
        yval = bar.get_height()
        ax2.text(bar.get_x() + bar.get_width()/2, yval, f"${yval:,.0f}", ha='center', va='bottom')

    st.pyplot(fig2)

    st.info("""
    **The HCorp Advantage:** Even if Helium-3 is incredibly expensive, the HCorp Fusion Drive requires so little fuel mass that it avoids the astronomical cost of launching thousands of tons of chemical fuel into orbit.
    """)
