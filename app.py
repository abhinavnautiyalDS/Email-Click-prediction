import streamlit as st
import numpy as np
import pickle
import base64
import os


if not os.path.exists(".installed_dependencies"):  # Run only once
    os.system("pip install -r requirements.txt")
    open(".installed_dependencies", "w").close()
    
# Set page config
st.set_page_config(layout="centered") 

# --- SET BACKGROUND IMAGE ---
def set_bg(image_file):
    with open(image_file, "rb") as image:
        encoded = base64.b64encode(image.read()).decode()
    css = f"""
    <style>
    .stApp {{
        background-image: url("data:image/jpg;base64,{encoded}");
        background-size: cover;
        background-repeat: no-repeat;
        background-attachment: fixed;
    }}
    </style>
    """
    st.markdown(css, unsafe_allow_html=True)

set_bg("image.jpg")  # Replace with your image filename

# --- TITLE & INTRO TEXT ---
st.markdown(
    """
    <h1 style='text-align: center; font-size: 42px; color: white;'>📧 Smart Email Click Predictor</h1>
    """, unsafe_allow_html=True
)

st.markdown(
    """
    <p style='text-align: center; font-size: 20px; color: white;'>
        Predict whether a user will click on an email based on content, timing, and user demographics.
    </p>
    """, unsafe_allow_html=True
)

# --- Load model ---
with open('model.pkl', 'rb') as file:
    model = pickle.load(file)

# --- Input Fields ---
st.subheader("🔧 Email Campaign Details")

# Direct time range selection
time_range = st.selectbox("Time of Email", ['Morning', 'Afternoon', 'Evening', 'Night'])

# Weekday
weekday = st.selectbox("Day of the Week", ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'])

def segment_weekday(day):
    if day in ['Monday', 'Tuesday']:
        return 'Early_Week'
    elif day in ['Wednesday', 'Thursday']:
        return 'Mid_Week'
    else:
        return 'Late_Week'

weekday_segment = segment_weekday(weekday)

user_past_purchases = st.number_input("User Past Purchases", min_value=0, step=1)
email_text_type = st.radio("Email Text Type", ['Long', 'Short'])
email_version = st.radio("Email Version", ['Generic', 'Personalized'])
user_country = st.selectbox("User Country", ['ES', 'FR', 'UK', 'US'])

# --- Create input vector ---
def create_feature_vector():
    features = [user_past_purchases]
    features.append(1 if email_text_type == 'Long' else 0)
    features.append(1 if email_text_type == 'Short' else 0)
    features.append(1 if email_version == 'Generic' else 0)
    features.append(1 if email_version == 'Personalized' else 0)
    features += [1 if user_country == c else 0 for c in ['ES', 'FR', 'UK', 'US']]
    features += [1 if weekday_segment == seg else 0 for seg in ['Early_Week', 'Late_Week', 'Mid_Week']]
    features += [1 if time_range == tr else 0 for tr in ['Afternoon', 'Evening', 'Morning', 'Night']]
    return np.array(features).reshape(1, -1)

# --- Prediction ---
if st.button("🔍 Predict Click"):
    input_data = create_feature_vector()
    prediction = model.predict(input_data)[0]
    result = "✅ User is likely to click!" if prediction == 1 else "❌ User is unlikely to click."
    
    st.markdown(
        f"""
        <div style='text-align: center; font-size: 24px; font-weight: bold; color: white; margin-top: 20px;'>
            {result}
        </div>
        """, unsafe_allow_html=True
    )
