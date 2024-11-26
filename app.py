import streamlit as st
import pickle
import pandas as pd
import sklearn

# Load the trained model
model = pickle.load(open("Stress_Detection_LRmodel.pkl",'rb'))

# App title
st.title("Stress Level Prediction App")
st.write(" This App Predict the stress level of Employees.")

# Sidebar for user input
st.sidebar.header("Individual Results / Information")

# Input fields
Heart_Rate = st.sidebar.number_input("Measured Heart rate (in beats per minute)", value=0.0)
Skin_Conductivity = st.sidebar.number_input("Measured Skin conductivity (in microsiemens)", value=0.0)
Hours_Worked = st.sidebar.number_input("Number of hours worked daily", value=0.0)
Emails_Sent = st.sidebar.number_input("Number of emails sent daily", value=0.0)
Meetings_Attended = st.sidebar.number_input("Number of meetings attended daily", value=0.0)


# Prepare input data for prediction
input_data = pd.DataFrame({
    "Heart_Rate": [Heart_Rate],
    "Skin_Conductivity": [Skin_Conductivity],
    "Hours_Worked": [Hours_Worked],
    "Emails_Sent": [Emails_Sent],
    "Meetings_Attended": [Meetings_Attended]
})

# Prediction button
if st.button("Predict"):
    prediction = model.predict(input_data)
    # Alternative conversion to scalar
    predicted_value = float(prediction[0])  
    st.success(f"Your predicted stress level is: {predicted_value:.2f}")
