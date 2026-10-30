import streamlit as st
import math
import matplotlib.pyplot as plt

# Set up the page configuration
st.set_page_config(page_title="HCorp Project Helios v0.4", page_icon="🚀", layout="wide")

# HCorp Header
st.title("🚀 HCorp Systems: Project Helios v0.4")
st.subheader("Full Mission Profile: Earth Launch to Mars Transit")
st.write("This model calculates the mass ratio to escape Earth's gravity, and then the mass ratio to transit to Mars.")

# --- PHASE 1: EARTH LAUNCH ---
st.header("Phase 1: Earth to Low Earth Orbit (LEO)")
st.write("Delta-V required to reach orbit: **9,400 m/s** (Accounts for gravity and atmospheric drag).")

launch_engine = st.selectbox(
    "Select Launch Engine (Currently, only chemical rockets have the thrust-to-weight ratio to launch from Earth):",
    ["Chemical Rocket (Ve = 4,500 m/s)"]
)

# Extract exhaust velocity from selection
ve_launch = 4500

# Calculate Launch Mass Ratio
launch_ratio = math.exp(9400 / ve_launch)
st.metric(label="Mass Ratio to reach LEO", value=f"{launch_ratio:.2f}")
st.write(f"*(This means {((launch_ratio - 1) / launch_ratio) * 100:.1f}% of the launchpad weight is just fuel to get to orbit).*")

st.write("---")

# --- PHASE 2: MARS TRANSIT ---
st.header("Phase 2: LEO to Mars Transit")
days = st.slider("Desired Mars Transit Time (Days)", min_value=10, max_value=120, value=30, step=1)

# Math for Delta-V based on days
transit_dv = 225000 / days
st.write(f"**Target Transit Delta-V:** {transit_dv:,.0f} m/s")

ENGINES = {
    "Chemical Rocket": 4500,
    "Nuclear Thermal": 9000,
    "HCorp Fusion Drive": 100000
}

col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

# Display the live math for each engine
for i, (engine_name, exhaust_velocity) in enumerate(ENGINES.items()):
    transit_ratio = math.exp(transit_dv / exhaust_velocity)
    fuel_pct = ((transit_ratio - 1) / transit_ratio) * 100
    
    with columns[i]:
        st.subheader(engine_name)
        st.metric(label="Transit Mass Ratio", value=f"{transit_ratio:.2f}")
        
        # Calculate TOTAL mission mass ratio (Launch Ratio * Transit Ratio)
        # Note: If the transit engine is different from the launch engine, 
        # the mass ratio multiplies because you have to launch the transit fuel into space.
        total_ratio = launch_ratio * transit_ratio
        st.write(f"**Total Mission Mass Ratio:** {total_ratio:.2f}")
        st.write(f"*(Fuel Weight: {((total_ratio - 1) / total_ratio) * 100:.1f}% of initial Earth mass)*")
        
        if total_ratio > 30:
            st.error("CRITICAL: Total mission is mathematically impossible.")
        elif total_ratio > 15:
            st.warning("HIGH FUEL: Requires orbital refueling or massive staging.")
        else:
            st.success("OPTIMAL: Mission profile is viable.")

# --- Generate the Graph ---
st.write("---")
st.subheader("Projected Total Mission Fuel Mass vs. Transit Time")

days_range = list(range(10, 121, 5))
fig, ax = plt.subplots(figsize=(10, 4))
colors = {"Chemical Rocket": "red", "Nuclear Thermal": "orange", "HCorp Fusion Drive": "green"}

for engine_name, exhaust_velocity in ENGINES.items():
    total_ratios = []
    for d in days_range:
        t_dv = 225000 / d
        t_ratio = math.exp(t_dv / exhaust_velocity)
        total_r = launch_ratio * t_ratio
        total_fuel_pct = ((total_r - 1) / total_r) * 100
        total_ratios.append(min(total_fuel_pct, 100)) # Cap at 100% for graph
        
    ax.plot(days_range, total_ratios, label=engine_name, color=colors[engine_name], linewidth=3)

# Add a marker for the user's selected day
current_transit_dv = 225000 / days
ax.axvline(x=days, color='blue', linestyle='--', label=f'Selection ({days} days)')

ax.set_ylim(0, 105)
ax.set_xlabel("Mars Transit Time (Days)")
ax.set_ylabel("Total Mission Fuel Weight (%)")
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend()

st.pyplot(fig)
