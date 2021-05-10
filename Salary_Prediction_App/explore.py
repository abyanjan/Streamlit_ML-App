import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
#import plotly.express as px

def regroup_country(country_count, cutoff):
    country_map = {}
    for i in range(len(country_count)):
        if country_count.values[i] >= cutoff:
            country_map[country_count.index[i]] = country_count.index[i]
        else:
            country_map[country_count.index[i]] = 'Other'
    return country_map


def convert_experience(x):
    if x ==  'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def process_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedComp"]]
    df = df[df["ConvertedComp"].notnull()]
    df = df.dropna()
    #df = df[df["Employment"] == "Employed full-time"]
    #df = df.drop("Employment", axis=1)

    country_map = regroup_country(df.Country.value_counts(), 400)
    df["Country"] = df["Country"].map(country_map)
    df = df[df["ConvertedComp"] <= 250000]
    df = df[df["ConvertedComp"] >= 10000]
    #df = df[df["Country"] != "Other"]

    df["YearsCodePro"] = df["YearsCodePro"].apply(convert_experience)
    df["EdLevel"] = df["EdLevel"].apply(process_education)
    df = df.rename({"ConvertedComp": "Salary"}, axis=1)
    return df

df = load_data()

def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
    ### Stack Overflow Developer Survey 2020
    """
    )

    country_data = df["Country"].value_counts()

    #fig1, ax1 = plt.subplots()
    #ax1.pie(data, labels=data.index, autopct="%1.1f%%", shadow=True, startangle=90)
    #ax1.axis("equal")  # Equal aspect ratio ensures that pie is drawn as a circle.
    
    st.write("""#### Number of Data from different countries""")

    st.bar_chart(country_data)
    
    st.write(
        """
    #### Mean Salary Based On Country
    """
    )

    salary_data = df.groupby(["Country"])["Salary"].mean()
    st.bar_chart(salary_data)

    st.write(
        """
    #### Mean Salary Based On Experience
    """
    )

    mean_salary_data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(mean_salary_data)

