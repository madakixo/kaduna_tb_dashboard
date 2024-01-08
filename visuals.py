import numpy as np
import pandas as pd
import geopandas as gpd
import plotly.express as px
import plotly.graph_objects as go

block1a = pd.read_csv("block1a_2019_to_2023_processed.csv")

# Read the shapefile
shapes = gpd.read_file("./nga_adm_osgof_20190417/nga_admbnda_adm2_osgof_20190417.shp")
c_lat = 10.3764
c_lon = 7.7095
geodf = block1a.merge(shapes, left_on='LGA', right_on='ADM2_EN', how='left')
geodf = gpd.GeoDataFrame(geodf)

block2b =  pd.read_csv('block2b_processed.csv', index_col=0)
block2b = block2b.rename(columns={"14-May":"5-14"})

kaduna_lgas = block1a['LGA'].unique()

def plot_lga_presumptive_cases_trend(lga_name):
    """
    Generates and displays a line chart showing the trend in presumptive cases
    for a specific LGA over time.

    Args:
        lga_name: The name of the LGA to analyze.

    Returns:
        A Plotly Express figure object representing the line chart.
    """

    # Filter data for the chosen LGA
    lga_data = block1a[block1a["LGA"] == lga_name]

    # Generate the line chart with Plotly Express
    fig = px.line(
        lga_data,
        x="Year_Quarter",
        y="Total number of presumptives",
        markers=True,
        line_shape="linear",
        title=f"Presumptive Cases Trend in {lga_name}<br><sup>Data from 2019 to 2023 of block1a</sup>",
    )

    # Customize the chart layout for clarity
    fig.update_layout(
        xaxis_title="Year and Quarter",
        yaxis_title="Number of Presumptives",
    )

    return fig


def plot_lga_diagnosed_tb_cases_trend(lga_name):
    """
    Generates and displays a line chart showing the trend in diagnosed tuberculosis (TB) cases
    for a specific Local Government Area (LGA) over time.

    Args:
        lga_name: The name of the LGA to analyze.

    Returns:
        A Plotly Express figure object representing the line chart.
    """

    # Filter data for the chosen LGA
    lga_data = block1a[block1a["LGA"] == lga_name]

    # Generate the line chart with Plotly Express
    fig = px.line(
        lga_data,
        x="Year_Quarter",
        y="Total diagnosed",  # Rename "Total diagnosed" to be consistent with overall data frame
        markers=True,
        line_shape="linear",
        title=f"Diagnosed TB Cases Trend in {lga_name}<br><sup>Data from 2019 to 2023 of block1a</sup>",
    )

    # Customize the chart layout for clarity
    fig.update_layout(
        xaxis_title="Year and Quarter",
        yaxis_title="Number of Diagnosed TB Cases",  # Rename y-axis title to match variable name
    )

    return fig


def show_choropleth_for_number_of_diagnosed(year_quarter):
    # Filter the GeoDataFrame for the specified year_quarter
    sliced_geodf = geodf[geodf['Year_Quarter'] == year_quarter]

    # Create a choropleth map using Plotly Express
    choropleth_fig = px.choropleth(
        sliced_geodf,
        geojson=sliced_geodf.geometry,
        locations=sliced_geodf.index,
        color='Examined for diagnosis',
        hover_name='ADM2_EN',
        color_continuous_scale='PuBu',
        projection="mercator",
        labels='Total diagnosed',
        custom_data=['ADM2_EN', 'Total diagnosed'],  # Custom data for tooltip
        title=f"Number of Diagnosed TB in Kaduta State for {year_quarter} <br><sup>Data from 2019 to 2023 of block1a</sup>"
    )

    # Customize the hover template to show LGA and number of diagnosed
    choropleth_fig.update_traces(
        hovertemplate="<b>%{customdata[0]}</b><br>Diagnosed: %{customdata[1]:,}<extra></extra>"
    )

    # Adjust layout settings
    choropleth_fig.update_layout(autosize=False, width=800, height=600)
    choropleth_fig.update_geos(fitbounds="locations", visible=False)

    return choropleth_fig

def show_gender_age_tb_bar(year_quarter):
    """
    Generates and displays a grouped bar chart showing the distribution of age groups by gender.

    Args:
        year_quarter (str): The year and quarter for which the data is visualized.

    Returns:
        A Plotly Express figure object representing the grouped bar chart.
    """
    # Melt the DataFrame to transform it into a suitable format for Plotly Express
    melted_df = pd.melt(
        block2b,
        id_vars=['Year_Quarter', 'LGA', 'Sex'],
        value_vars=['0-4', '5-14', '15-24', '25-34', '35-44', '45-54', '55-64'],
        var_name='Age_Group',
        value_name='Values'
    )

    # Sum the values grouped by year_quarter, age_group, and sex
    aggregated_df = melted_df.groupby(["Year_Quarter", "Age_Group", "Sex"], as_index=False)['Values'].sum()

    # Filter data for the specified year_quarter
    filtered_df = aggregated_df[aggregated_df["Year_Quarter"] == year_quarter]

    # Create the grouped bar chart
    fig = px.bar(
        filtered_df,
        x='Age_Group',
        y='Values',
        color='Sex',
        barmode='group',
        title=f"Distribution of Age Groups by Gender in all LGAs for {year_quarter}<br><sup>Data from 2021 to 2023 of block2b</sup>",
    )

    # Customize the layout
    fig.update_layout(
        xaxis_title='Age Group',
        yaxis_title='Count',
        height=600,
        width=1200
    )

    return fig

