import streamlit as st
import pickle
import numpy as np
import pandas as pd


def load_model():
    with open('final_model.pkl', 'rb') as file:
        model = pickle.load(file)
    return model

def load_preprocessor():
     with open('preprocessor.pkl', 'rb') as file:
        preprocessor = pickle.load(file)
     return preprocessor


model = load_model()
preprocessor = load_preprocessor()



def show_predict_page():
    st.title("Software Developer Salary Prediction")

    st.write("""### We need some information to predict the salary""")

    countries = [
        "Other",
        "United States",
        "India",
        "United Kingdom",
        "Germany",
        "Canada",
        "Brazil",
        "France",
        "Spain",
        "Australia",
        "Netherlands",
        "Poland",
        "Italy",
        "Russian Federation",
        "Sweden",
    ]

    education = [
        "Less than a Bachelors",
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
    ]
    
    employment = [
        "Employed full-time",  
        "Independent contractor, freelancer, or self-employed",
        "Employed part-time"
        ]

    country = st.selectbox("Country", countries,index=1)
    education = st.selectbox("Education Level", education)
    employment = st.selectbox("Employment Type", employment)
    expericence = st.slider("Years of Experience", 0, 50, 3)

    ok = st.button("Calculate Salary")
    if ok:
        X = pd.DataFrame(np.array([[country, education, expericence, employment]]),
                         columns = ['Country', 'EdLevel', 'YearsCodePro','Employment'])
        X = preprocessor.transform(X)

        salary = model.predict(X)
        st.subheader(f"The estimated salary is ${salary[0]:.2f}")
