
import streamlit as st
import numpy as np

st.set_page_config(page_title="Aircraft MRO CBA Dashboard", layout="centered")

st.title("🛠️ Aircraft Maintenance CBA Dashboard")
st.markdown("Make strategic decisions based on predicted MRO duration, maintenance costs, lease losses, and residual value erosion.")

# --- USER INPUTS ---
st.header("🔧 Input Parameters")

col1, col2 = st.columns(2)
with col1:
    aircraft_type = st.selectbox("Aircraft Type", ["777", "787", "A350"])
    mro_region = st.selectbox("MRO Region", ["Middle East", "East Asia", "SE Asia", "USA"])
    labor_hours = st.number_input("Total Labor Hours (C-Check)", min_value=1000, max_value=8000, value=5000, step=100)
with col2:
    lost_rev_per_hr = st.number_input("Lost Revenue per Hour (USD)", min_value=5000, max_value=30000, value=21000, step=100)
    lease_rate_daily = st.number_input("Daily Lease Rate (USD)", min_value=1000, max_value=200000, value=85000, step=1000)
    predicted_duration_days = st.number_input("Predicted Downtime (Days)", min_value=1, max_value=60, value=17, step=1)

# --- MAINTENANCE COST CALCULATION ---
st.header("💵 Maintenance Cost")
labor_rate_map = {"Middle East": 75, "East Asia": 95, "SE Asia": 85, "USA": 120}
labor_rate = labor_rate_map[mro_region]
labor_cost = labor_hours * labor_rate
material_cost = 0.30 * labor_cost
total_maintenance_cost = labor_cost + material_cost

st.markdown(f"**Labor Rate:** ${labor_rate}/hr")
st.markdown(f"**Labor Cost:** ${labor_cost:,.0f}")
st.markdown(f"**Material Cost (30%):** ${material_cost:,.0f}")
st.markdown(f"**Total Maintenance Cost:** ${total_maintenance_cost:,.0f}")

# --- OPPORTUNITY COST ---
st.header("⏱️ Opportunity Cost of Downtime")
downtime_hours = predicted_duration_days * 24
opportunity_cost = downtime_hours * lost_rev_per_hr
st.markdown(f"**Downtime (hours):** {downtime_hours}")
st.markdown(f"**Lost Revenue:** ${opportunity_cost:,.0f}")

# --- LEASE LOSS (OPTIONAL) ---
st.header("📉 Lease Loss")
lease_loss = predicted_duration_days * lease_rate_daily
st.markdown(f"**Daily Lease Rate:** ${lease_rate_daily}")
st.markdown(f"**Lease Loss (Idle Asset):** ${lease_loss:,.0f}")

# --- RESIDUAL VALUE LOSS ---
st.header("💸 Residual Value Loss")
half_life_value = 28970000  # avg. from AA + UA
annual_dep = 0.05 * half_life_value
daily_dep = annual_dep / 365
residual_loss = daily_dep * predicted_duration_days
st.markdown(f"**Daily Depreciation:** ${daily_dep:,.0f}")
st.markdown(f"**Residual Value Loss:** ${residual_loss:,.0f}")

# --- SUMMARY ---
st.header("📊 Total Economic Impact")
total_cost = total_maintenance_cost + opportunity_cost + residual_loss + lease_loss
st.success(f"**Total Estimated Cost of MRO Downtime: ${total_cost:,.0f}**")

st.markdown("ℹ️ This dashboard is built for strategic assessment by airlines, lessors, financiers, and MRO providers.")
