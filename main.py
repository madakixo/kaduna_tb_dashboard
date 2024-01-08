import pandas as pd
import streamlit as st

from visuals import plot_lga_presumptive_cases_trend, plot_lga_diagnosed_tb_cases_trend, show_choropleth_for_number_of_diagnosed, show_gender_age_tb_bar, kaduna_lgas

st.set_page_config(page_title="Kaduna TB Dashboard", 
                   page_icon=None, 
                   layout="wide", 
                   initial_sidebar_state="auto", 
                   menu_items=None)

st.header("Kaduna State Tuberculosis Dashboard")

st.caption("""
Welcome to the Kaduna State Tuberculosis Dashboard, designed to provide comprehensive insights into the Tuberculosis (TB) situation in Kaduna State, Nigeria. This dashboard leverages interactive visualizations and data analytics to enhance understanding and awareness of TB trends over the years.
Explore the prevalence of TB across various age groups, genders, and local government areas (LGAs) in Kaduna State. Analyze presumptive and diagnosed TB cases, track trends over time, and gain valuable insights into the distribution of cases within the region.""")

# Display the selected year and quarter
year_quarter_options = [
    '2019 Q1', '2019 Q2', '2019 Q3', '2019 Q4', '2020 Q1', '2020 Q2',
    '2020 Q3', '2020 Q4', '2021 Q1', '2021 Q2', '2021 Q3', '2021 Q4',
    '2022 Q1', '2022 Q2', '2022 Q3', '2022 Q4', '2023 Q1', '2023 Q2'
]

year_quarter = st.select_slider('Year and Quarter', options=year_quarter_options)
selected_year = int(year_quarter.split(" ")[0])
adjusted_year_quarter = "2021 Q1" if selected_year < 2021 else year_quarter

c1, c2 = st.columns(2)
c1.plotly_chart(show_choropleth_for_number_of_diagnosed(year_quarter), use_container_width=True)
c2.plotly_chart(show_gender_age_tb_bar(adjusted_year_quarter), use_container_width=True)

lga_choice = st.selectbox(
    'Select a Kaduna LGA',
    kaduna_lgas)

c1_, c2_ = st.columns(2)
c1_.plotly_chart(plot_lga_presumptive_cases_trend(lga_choice), use_container_width=True)
c2_.plotly_chart(plot_lga_diagnosed_tb_cases_trend(lga_choice), use_container_width=True)
