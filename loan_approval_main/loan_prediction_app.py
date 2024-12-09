import streamlit as st
import pickle
import numpy as np

# Load the trained XGBoost model
model_filename = "trained_xgboost_model.pkl"
with open(model_filename, "rb") as file:
    model = pickle.load(file)

# App title
st.title("VILLAPARTHY CAPITAL")
st.markdown("Welcome to Villaparthy – Your Trusted Partner in Personal Lending! We’re here to make your loan journey smooth, transparent, and tailored to your needs. To get started, simply fill out the Loan Eligibility Assessment (LEA) Form located on the left-hand sidebar. By providing a few key details about your financial situation our system will generate an accurate prediction of your loan eligibility in just a few moments. At Villaparthy, we value your time and are committed to providing clear and instant insights to help you make confident financial decisions. Let’s take the first step toward making your goals a reality!")

            
# Function to format numbers with commas
def format_number_with_commas(number):
    return f"{number:,}"

# Inject custom CSS for styling
st.markdown(
    """
    <style>
    /* Main background styling */
    .main {
        background-color: #F7F7F7; /* Super light greyish-white background */
        color: #1E1E1E; /* Dark text for readability */
    }

    /* Center app title */
    .css-1aumxhk {
        text-align: center;
        color: #B89B56; /* Gold color */
    }

    /* Sidebar styling */
    [data-testid="stSidebar"] {
        background-color: #2E2E2E; /* Sidebar dark grey */
        color: #FFFFFF; /* White text */
        border-right: 2px solid #B89B56; /* Gold border */
    }

    /* Button customization */
    div.stButton > button {
        background-color: #B89B56; /* Gold button background */
        color: #000000; /* Black button text */
        border-radius: 5px;
        border: none;
    }

    div.stButton > button:hover {
        background-color: #FFFFFF; /* White button on hover */
        color: #000000; /* Black text on hover */
        border: 1px solid #B89B56; /* Gold border */
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Initialize default values to reset inputs on reload
if "reset" not in st.session_state:
    st.session_state.reset = True

# Sidebar input fields for the top 8 features
st.sidebar.header("Loan Eligibility Assessment (LEA)")
cibil_score = st.sidebar.number_input(
    "CIBIL Score (300-900)", min_value=300, max_value=900, value=300 if st.session_state.reset else 750, step=50, format="%d"
)
loan_term = st.sidebar.number_input(
    "Loan Term (Months)", min_value=0, value=0 if st.session_state.reset else 36, step=1, format="%d"
)
loan_amount = st.sidebar.number_input(
    "Loan Amount ($)", min_value=0, value=0 if st.session_state.reset else 10000, step=1000, format="%d"
)
income_annum = st.sidebar.number_input(
    "Annual Income ($)", min_value=0, value=0 if st.session_state.reset else 50000, step=1000, format="%d"
)
residential_asset_value = st.sidebar.number_input(
    "Residential Asset Value ($)", min_value=0, value=0 if st.session_state.reset else 50000, step=1000, format="%d"
)
no_of_dependents = st.sidebar.number_input(
    "Number of Dependents", min_value=0, value=0 if st.session_state.reset else 0, step=1, format="%d"
)
bank_asset_value = st.sidebar.number_input(
    "Bank Asset Value ($)", min_value=0, value=0 if st.session_state.reset else 10000, step=1000, format="%d"
)
commercial_asset_value = st.sidebar.number_input(
    "Commercial Asset Value ($)", min_value=0, value=0 if st.session_state.reset else 5000, step=1000, format="%d"
)

# Add placeholder values for missing features to match the model's input shape
employment_status = 0  # Default to "Unemployed"
education_level = 0  # Default to "No Degree"
luxury_asset_value = 0  # Default to $0 for luxury assets

# Centered formatted input summary
st.markdown("## Formatted Input Summary")
st.markdown("---")  # Add a horizontal line for separation
st.write(f"**CIBIL Score**: {format_number_with_commas(cibil_score)}")
st.write(f"**Loan Term**: {format_number_with_commas(loan_term)} months")
st.write(f"**Loan Amount**: ${format_number_with_commas(loan_amount)}")
st.write(f"**Annual Income**: ${format_number_with_commas(income_annum)}")
st.write(f"**Residential Asset Value**: ${format_number_with_commas(residential_asset_value)}")
st.write(f"**Number of Dependents**: {format_number_with_commas(no_of_dependents)}")
st.write(f"**Bank Asset Value**: ${format_number_with_commas(bank_asset_value)}")
st.write(f"**Commercial Asset Value**: ${format_number_with_commas(commercial_asset_value)}")

# Prediction button
if st.sidebar.button("Predict Loan Approval"):
    # Prepare input data with placeholder values for missing features
    input_data = np.array([[
        cibil_score,
        loan_term,
        loan_amount,
        income_annum,
        residential_asset_value,
        no_of_dependents,
        bank_asset_value,
        commercial_asset_value,
        employment_status,
        education_level,
        luxury_asset_value,
    ]])

    # Make predictions
    try:
        prediction = model.predict(input_data)[0]
        prediction_proba = model.predict_proba(input_data)[0]

        # Display results
        st.markdown("---")  # Add a horizontal line for separation
        if prediction == 1:
            st.success("Congratulations! The loan application is likely to be approved.")
            st.write(f"Confidence: {prediction_proba[1]:.2%}")
        else:
            st.error("Sorry, the loan application is likely to be rejected.")
            st.write(f"Confidence: {prediction_proba[0]:.2%}")
    except Exception as e:
        st.error(f"Error making prediction: {str(e)}")

# Reset session state to enforce clearing inputs on reload
st.session_state.reset = True

