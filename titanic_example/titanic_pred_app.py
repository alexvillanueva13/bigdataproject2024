import streamlit as st
import pickle
import numpy as np

# Load the saved model
with open("titanic_predictor.sav", "rb") as file:
    model = pickle.load(file)

# Function to make predictions
def predict_survival(model, features):
    prediction = model.predict([features])
    return "Survived" if prediction[0] == 1 else "Did Not Survive"

# Streamlit app
def main():
    st.title("Titanic Survival Predictor")
    st.write("Enter the details below to predict survival on the Titanic:")

    # Input fields
    gender = st.radio("Gender", ("Male", "Female"))
    age = st.number_input("Age", min_value=0, max_value=100, step=1, value=30)
    pclass = st.selectbox("Ticket Class (Pclass)", [1, 2, 3])
    siblings_spouses = st.number_input("Number of Siblings/Spouses Aboard", min_value=0, step=1, value=0)
    parents_children = st.number_input("Number of Parents/Children Aboard", min_value=0, step=1, value=0)
    fare = st.number_input("Fare (in USD)", min_value=0.0, step=0.01, value=50.0)

    # Convert gender to numeric
    gender_numeric = 1 if gender == "Female" else 0

    # Prepare features for prediction
    features = [
        pclass,
        gender_numeric,
        age,
        siblings_spouses,
        parents_children,
        fare
    ]

    # Prediction
    if st.button("Predict"):
        result = predict_survival(model, features)
        st.write(f"Prediction: {result}")

if __name__ == "__main__":
    main()
