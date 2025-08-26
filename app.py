import streamlit as st
import pandas as pd
import numpy as np
import pickle

st.set_page_config(page_title="Car Price Predictor", page_icon="🚗", layout="centered")

st.markdown(
    """
    <style>
    .stApp {background: linear-gradient(135deg,#141E30,#243B55);}
    .stButton button {background: linear-gradient(90deg,#ff6a00,#ee0979); color:white; font-size:18px; border-radius:10px; padding:10px 24px;}
    .stSelectbox label, .stNumberInput label {color:#f0f0f0; font-size:16px;}
    .css-10trblm {color:white; text-align:center; font-size:40px; font-weight:bold;}
    </style>
    """,
    unsafe_allow_html=True,
)

st.title("🚗 Car Price Predictor")

car = pickle.load(open('Content/car.pkl', 'rb'))

Brand = st.selectbox("Choose the Brand", car["Brand"].unique())
filtered_models = car[car["Brand"] == Brand]["Model"].unique()
Model = st.selectbox("Choose the Model", filtered_models)
Year = st.selectbox("Choose the Year", sorted(car["Year"].unique()))
filtered_engine = car[(car["Brand"] == Brand) & (car["Model"] == Model)]["Engine Size"].unique()
Engine_Size = st.selectbox("Choose the Engine Size", sorted(filtered_engine))
Fuel_Type = st.selectbox("Choose the Fuel Type", car["Fuel Type"].unique())
Transmission = st.selectbox("Choose the Transmission", car["Transmission"].unique())
Condition = st.selectbox("Choose the Condition", car["Condition"].unique())
Km_driven = 1000

pipeline = pickle.load(open('Content/pipeline.pkl', 'rb'))
model = pickle.load(open('Content/model.pkl', 'rb'))

input_dict = {
    "Brand": [Brand],
    "Model": [Model],
    "Year": [Year],
    "Engine Size": [Engine_Size],
    "Fuel Type": [Fuel_Type],
    "Transmission": [Transmission],
    "Mileage": [Km_driven],
    "Condition": [Condition],
}

L = pd.DataFrame(input_dict)
data = pipeline.transform(L)

if st.button("🔮 Predict Price"):
    Price = model.predict(data)
    st.markdown(
        f"<h2 style='text-align:center;color:#00FFCC;'>💰 Estimated Price: ${int(Price):,}</h2>",
        unsafe_allow_html=True,
    )
