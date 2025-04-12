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

# --- Streamlit UI ---
st.title("Drillhole Angle of Incidence Visualizer")

plunge = st.slider("Drillhole Plunge (°)", 0, 90, 60)

# Add multiple geological planes
st.subheader("Geological Planes (Strike / Dip)")
n_planes = st.number_input("Number of planes", min_value=1, max_value=10, value=2)

planes = []
for i in range(n_planes):
    col1, col2 = st.columns(2)
    with col1:
        strike = st.number_input(f"Strike of Plane {i+1} (°)", 0, 360, value=90, key=f"strike_{i}")
    with col2:
        dip = st.number_input(f"Dip of Plane {i+1} (°)", 0, 90, value=45, key=f"dip_{i}")
    planes.append((strike, dip))

azimuths = np.arange(0, 361, 1)

# --- Plotting ---
fig, ax = plt.subplots(figsize=(10, 5))

for i, (strike, dip) in enumerate(planes):
    incidence_angles = [angle_of_incidence(strike, dip, az, plunge) for az in azimuths]
    ax.plot(azimuths, incidence_angles, label=f"Plane {i+1}: {strike}°/{dip}°")

ax.set_title("Angle of Incidence vs Drillhole Azimuth")
ax.set_xlabel("Drillhole Azimuth (°)")
ax.set_ylabel("Angle of Incidence (°)")
ax.set_xlim(0, 360)
ax.set_ylim(0, 90)
ax.grid(True)
ax.legend()
st.pyplot(fig)
