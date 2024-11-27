import streamlit as st
import pickle
import pandas as pd
import plotly.graph_objects as go

# Load the trained model
model = pickle.load(open("Stress_Detection_LRmodel.pkl", 'rb'))

# App title
st.title("Stress Level Prediction App")
st.write("This App Predicts the stress level of Employees.")

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
    predicted_value = float(prediction[0])

    # Display predicted value
    st.success(f"Your predicted stress level is: {predicted_value:.2f}")

    # Determine stress category
    if predicted_value < 21:
        stress_category = "Low Stress"
        advice_message = "Your stress level is low—keep it up!"
    elif 21 <= predicted_value < 25:
        stress_category = "Average Stress"
        advice_message = "Your stress level is average—consider taking a break or relaxing."
    else:
        stress_category = "High Stress"
        advice_message = "Your stress level is high—take steps to relax and recharge."

    st.write(f"### {stress_category}")
    st.write(advice_message)

    # Add a gauge chart with labels
    fig = go.Figure(go.Indicator(
        mode="gauge+number",
        value=predicted_value,
        title={'text': "Stress Level"},
        gauge={
            'axis': {'range': [16, 31], 'tickwidth': 1, 'tickcolor': "darkblue"},
            'bar': {'color': "darkblue"},
            'steps': [
                {'range': [16, 21], 'color': "lightgreen"},
                {'range': [21, 25], 'color': "yellow"},
                {'range': [25, 31], 'color': "red"}
            ],
            'threshold': {
                'line': {'color': "black", 'width': 4},
                'thickness': 0.75,
                'value': predicted_value
            }
        }
    ))

    # Add custom labels for the gauge chart
    fig.add_annotation(x=0.2, y=0.5, text="Low", showarrow=False, font=dict(color="green", size=14))
    fig.add_annotation(x=0.5, y=0.5, text="Average", showarrow=False, font=dict(color="orange", size=14))
    fig.add_annotation(x=0.8, y=0.5, text="High", showarrow=False, font=dict(color="red", size=14))

    # Render the gauge chart in Streamlit
    st.plotly_chart(fig)
