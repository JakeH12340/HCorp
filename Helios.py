import streamlit as st
import math
import matplotlib.pyplot as plt

# Set up the page configuration
st.set_page_config(page_title="HCorp Project Helios v0.5", page_icon="🚀", layout="wide")

st.title("🚀 HCorp Systems: Project Helios v0.5")
st.subheader("Mission Architecture & Propulsion Analysis")

# --- LAUNCH ARCHITECTURE TOGGLE ---
st.header("1. Mission Architecture")
launch_mode = st.radio(
    "Select Launch Architecture:",
    ["Single Launch from Earth (All fuel launched at once)", 
     "Orbital Assembly (Ship and fuel launched separately, assembled in space)"]
)

st.write("---")

# --- PHASE 1: EARTH LAUNCH ---
st.header("Phase 1: Earth to Low Earth Orbit (LEO)")
launch_ratio = math.exp(9400 / 4500) # Chemical rocket launch ratio

if "Single Launch" in launch_mode:
    st.write(f"**Launch Mass Ratio:** {launch_ratio:.2f}")
    st.write(f"*(Note: {((launch_ratio - 1) / launch_ratio) * 100:.1f}% of the launchpad weight is fuel just to reach orbit).*")
else:
    st.write("**Launch Mass Ratio: N/A** (Ship and fuel are launched separately. The Mars transit vehicle starts its calculation already in LEO).")

st.write("---")

# --- PHASE 2: MARS TRANSIT ---
st.header("Phase 2: LEO to Mars Transit")
days = st.slider("Desired Mars Transit Time (Days)", min_value=10, max_value=120, value=30, step=1)

transit_dv = 225000 / days
st.write(f"**Target Transit Delta-V:** {transit_dv:,.0f} m/s")

ENGINES = {
    "Chemical Rocket": 4500,
    "Nuclear Thermal": 9000,
    "HCorp Fusion Drive": 100000
}

col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

for i, (engine_name, exhaust_velocity) in enumerate(ENGINES.items()):
    transit_ratio = math.exp(transit_dv / exhaust_velocity)
    
    with columns[i]:
        st.subheader(engine_name)
        st.metric(label="Transit Mass Ratio", value=f"{transit_ratio:.2f}")
        
        # Calculate total mission based on launch mode
        if "Single Launch" in launch_mode:
            total_ratio = launch_ratio * transit_ratio
            label = "Total Mission Mass Ratio"
        else:
            total_ratio = transit_ratio
            label = "Transit Vehicle Mass Ratio (In Space)"
            
        fuel_pct = ((total_ratio - 1) / total_ratio) * 100
        
        st.write(f"**{label}:** {total_ratio:.2f}")
        st.write(f"*(Fuel Weight: {fuel_pct:.1f}%)*")
        
        if total_ratio > 15:
            st.error("CRITICAL: Ship structurally impossible.")
        elif total_ratio > 5:
            st.warning("HIGH FUEL: Payload severely limited.")
        elif total_ratio > 2.5:
            st.info("MODERATE: Acceptable for unmanned cargo.")
        else:
            st.success("OPTIMAL: Massive payload capacity.")

# --- Generate the Graph ---
st.write("---")
st.subheader("Projected Fuel Weight vs. Transit Time")

days_range = list(range(10, 121, 5))
fig, ax = plt.subplots(figsize=(10, 4))
colors = {"Chemical Rocket": "red", "Nuclear Thermal": "orange", "HCorp Fusion Drive": "green"}

for engine_name, exhaust_velocity in ENGINES.items():
    total_ratios = []
    for d in days_range:
        t_dv = 225000 / d
        t_ratio = math.exp(t_dv / exhaust_velocity)
        
        if "Single Launch" in launch_mode:
            total_r = launch_ratio * t_ratio
        else:
            total_r = t_ratio
            
        total_fuel_pct = ((total_r - 1) / total_r) * 100
        total_ratios.append(min(total_fuel_pct, 100)) 
        
    ax.plot(days_range, total_ratios, label=engine_name, color=colors[engine_name], linewidth=3)

ax.axvline(x=days, color='blue', linestyle='--', label=f'Selection ({days} days)')
ax.set_ylim(0, 105)
ax.set_xlabel("Mars Transit Time (Days)")
ax.set_ylabel("Fuel Weight (%)")
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend()
st.pyplot(fig)
