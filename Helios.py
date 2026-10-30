import streamlit as st
import math
import matplotlib.pyplot as plt

# Set up the page configuration
st.set_page_config(page_title="HCorp Project Helios", page_icon="🚀", layout="wide")

# HCorp Header
st.title("🚀 HCorp Systems: Project Helios")
st.subheader("Advanced Propulsion & Energy Analysis")
st.write("Adjust the transit time below to see the fuel mass requirements for an Earth-to-Mars mission.")

# Engine Exhaust Velocities (m/s)
ENGINES = {
    "Chemical Rocket": 4500,
    "Nuclear Thermal": 9000,
    "HCorp Fusion Drive": 100000
}

def calculate_mass_ratio(delta_v, exhaust_velocity):
    return math.exp(delta_v / exhaust_velocity)

# Create an interactive slider for the user
days = st.slider("Desired Earth-to-Mars Transit Time (Days)", min_value=10, max_value=120, value=30, step=1)

# Math for Delta-V
delta_v = 225000 / days
st.write(f"**Target Delta-V:** {delta_v:,.0f} m/s")

# Split the screen into 3 columns for the engines
col1, col2, col3 = st.columns(3)
columns = [col1, col2, col3]

# Display the live math for each engine
for i, (engine_name, exhaust_velocity) in enumerate(ENGINES.items()):
    ratio = calculate_mass_ratio(delta_v, exhaust_velocity)
    fuel_pct = ((ratio - 1) / ratio) * 100
    
    with columns[i]:
        st.header(engine_name)
        st.metric(label="Fuel Weight", value=f"{fuel_pct:.1f}%")
        st.write(f"Mass Ratio: {ratio:.2f}")
        
        # Updated Warning Logic
        if ratio > 10:
            st.error("CRITICAL: Ship structurally impossible.")
        elif ratio > 2.5:
            st.warning("HIGH FUEL: Payload severely limited.")
        elif ratio > 1.5:
            st.info("MODERATE: Acceptable for unmanned cargo.")
        else:
            st.success("OPTIMAL: Massive payload capacity.")

# --- Generate the Graph ---
st.write("---")
st.subheader("Projected Fuel Mass vs. Transit Time")

days_range = list(range(10, 121, 5))
fig, ax = plt.subplots(figsize=(10, 4))
colors = {"Chemical Rocket": "red", "Nuclear Thermal": "orange", "HCorp Fusion Drive": "green"}

for engine_name, exhaust_velocity in ENGINES.items():
    fuel_percentages = []
    for d in days_range:
        dv = 225000 / d
        ratio = calculate_mass_ratio(dv, exhaust_velocity)
        fuel_pct = ((ratio - 1) / ratio) * 100
        fuel_percentages.append(min(fuel_pct, 100)) 
        
    ax.plot(days_range, fuel_percentages, label=engine_name, color=colors[engine_name], linewidth=3)

# Add a marker for the user's selected day
ax.axvline(x=days, color='blue', linestyle='--', label=f'Current Selection ({days} days)')

ax.set_ylim(0, 105)
ax.set_xlabel("Transit Time (Days)")
ax.set_ylabel("Fuel Weight (%)")
ax.grid(True, linestyle='--', alpha=0.7)
ax.legend()

# Display the graph in the web app
st.pyplot(fig)