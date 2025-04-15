import streamlit as st
import numpy as np
import matplotlib.pyplot as plt

# --- Geometry Functions ---
def deg2rad(deg):
    return np.radians(deg)

def vector_from_azimuth_plunge(azimuth, plunge):
    az = deg2rad(azimuth)
    pl = deg2rad(plunge)
    x = np.cos(pl) * np.sin(az)
    y = np.cos(pl) * np.cos(az)
    z = -np.sin(pl)
    return np.array([x, y, z])

def normal_vector_from_strike_dip(strike, dip):
    strike_rad = deg2rad(strike)
    dip_rad = deg2rad(dip)
    dip_dir_rad = strike_rad + np.pi / 2
    x = np.sin(dip_rad) * np.sin(dip_dir_rad)
    y = np.sin(dip_rad) * np.cos(dip_dir_rad)
    z = np.cos(dip_rad)
    return np.array([x, y, z])

def angle_of_incidence(strike, dip, azimuth, plunge):
    line_vec = vector_from_azimuth_plunge(azimuth, plunge)
    normal_vec = normal_vector_from_strike_dip(strike, dip)
    line_vec /= np.linalg.norm(line_vec)
    normal_vec /= np.linalg.norm(normal_vec)
    dot_product = np.dot(line_vec, normal_vec)
    angle_rad = np.arccos(np.clip(dot_product, -1.0, 1.0))
    incidence_angle = np.degrees(np.pi / 2 - angle_rad)
    return abs(incidence_angle)

def true_thickness_ratio(incidence_angle):
    return np.sin(np.radians(incidence_angle))

# --- Streamlit UI ---
st.title("Drillhole Angle of Incidence Visualizer")

plunge = st.slider("Drillhole Plunge (°)", 0, 90, 55)

# Add multiple geological planes
st.subheader("Geological Planes (Strike / Dip)")
n_planes = st.number_input("Number of planes", min_value=1, max_value=10, value=2)

planes = []
default_strikes = [90, 135]
default_dips = [45, 60]

for i in range(n_planes):
    # Use specific defaults for Plane 1 and 2, then fall back to generic
    strike_default = default_strikes[i] if i < len(default_strikes) else 90
    dip_default = default_dips[i] if i < len(default_dips) else 45

    col1, col2 = st.columns(2)
    with col1:
        strike = st.number_input(f"Strike of Plane {i+1} (°)", 0, 360, value=strike_default, key=f"strike_{i}")
    with col2:
        dip = st.number_input(f"Dip of Plane {i+1} (°)", -90, 90, value=dip_default, key=f"dip_{i}")

    planes.append((strike, dip))


azimuths = np.arange(0, 361, 1)

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 5))

for i, (strike, dip) in enumerate(planes):
    incidence_angles = [angle_of_incidence(strike, dip, az, plunge) for az in azimuths]
    ax.plot(azimuths, incidence_angles, label=f"Plane {i+1}: {strike}°/{dip}°")


ax.set_title("Angle of Incidence and True Thickness Ratio vs Drillhole Azimuth")
ax.set_xlabel("Drillhole Azimuth (°)")
ax.set_xlim(0, 360)
ax.set_ylim(0, 90)
ax.grid(True)

ax.set_ylabel("Angle of Incidence (°)")
secax = ax.secondary_yaxis('right',
    functions=(true_thickness_ratio,
               lambda r: np.degrees(np.arcsin(np.clip(r, 0, 1)))))
secax.set_ylabel("True Thickness Ratio")

ax.legend(loc="upper right", frameon=True)

ax.text(0.02, 0.95, f"Plunge: {plunge}°", transform=ax.transAxes,
        fontsize=9, verticalalignment='top', bbox=dict(boxstyle='round,pad=0.3', fc='white', alpha=0.5))

fig.text(0.98, 0.02, "App by E. Slater", fontsize=8, color="gray",
         ha='right', va='bottom', alpha=0.5)

st.pyplot(fig)
