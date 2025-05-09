import streamlit as st
import pandas as pd
import numpy as np
import joblib
import statsmodels.api as sm

# Load trained model
model = joblib.load("mro_duration_predictor_model_final.pkl")

# Title
st.title("✈️ Predictive MRO Duration Calculator")
st.markdown("Estimate the maintenance downtime for C-checks based on aircraft usage and provider region.")

# Sidebar inputs
st.sidebar.header("Aircraft Inputs")
aircraft_type = st.sidebar.selectbox("Aircraft Type", ["777", "787", "A350"])
age = st.sidebar.slider("Aircraft Age (years)", 0.0, 30.0, 10.0, 0.1)
cumulative_fc = st.sidebar.number_input("Cumulative Flight Cycles", min_value=0, value=10000)
avg_annual_cycles = st.sidebar.number_input("Avg Annual Flight Cycles", min_value=0, value=500)
avg_annual_hours = st.sidebar.number_input("Avg Annual Flight Hours", min_value=0, value=4500)
avg_daily_util = st.sidebar.slider("Avg Daily Utilisation (hrs)", 5.0, 20.0, 12.0, 0.1)

mro_region = st.sidebar.selectbox("MRO Region", ["East Asia", "Middle East", "SE Asia", "USA"])

# Feature construction
input_df = pd.DataFrame({
    'age': [age],
    'age_squared': [age ** 2],
    'cumulative_fc': [cumulative_fc],
    'avg_annual_cycles': [avg_annual_cycles],
    'avg_annual_hours': [avg_annual_hours],
    'avg_daily_utilisation': [avg_daily_util],
    'aircraft_type_787': [1 if aircraft_type == "787" else 0],
    'aircraft_type_A350': [1 if aircraft_type == "A350" else 0],
    'mro_region_Middle East': [1 if mro_region == "Middle East" else 0],
    'mro_region_SE Asia': [1 if mro_region == "SE Asia" else 0],
    'mro_region_USA': [1 if mro_region == "USA" else 0],
    'age_x_util': [age * avg_daily_util],
    'age_x_787': [age if aircraft_type == "787" else 0],
    'age_x_A350': [age if aircraft_type == "A350" else 0],
    'fc_x_me': [cumulative_fc if mro_region == "Middle East" else 0],
    'util_x_787': [avg_daily_util if aircraft_type == "787" else 0]
})

# Add constant manually (statsmodels compatibility)
input_df = sm.add_constant(input_df, has_constant='add')

# Prediction
predicted_duration = model.predict(input_df)[0]

# Output
st.subheader("📈 Predicted MRO Duration")
st.metric(label="Estimated Duration (days)", value=f"{predicted_duration:.2f}")

# ⚠ Warning if duration is very low
threshold = 7  # Editable threshold
if predicted_duration < threshold:
    st.warning("⚠️ This predicted duration is unusually short for a C-check. Please verify inputs or consult with MRO experts.")

# Notes
st.markdown("---")
st.markdown("Model accuracy: **83% R²**\n\nYou can change the warning threshold in the code (`threshold = 7`).")
st.caption("Developed for academic and decision-support use.")
