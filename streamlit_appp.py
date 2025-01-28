import streamlit as st
import pandas as pd
import math
import requests
from pathlib import Path
import seaborn as sns
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta
import plotly.express as px
from geopy.geocoders import Nominatim

# BEST OF TENNIS
st.set_page_config(
    page_title='BEST TENNIS IN 2019',
    page_icon='🎾', # tennis emoji
)

# -----------------------------------------------------------------------------
# Declare some useful functions.

@st.cache_data
def get_tennis_data():
    # csv read from disk
    try:
        # Specify the file path for the CSV
        DATA_FILENAME = Path(__file__).parent / 'data/tennis_data.csv'

        # Read the CSV file into a DataFrame
        raw_tennis_df = pd.read_csv(DATA_FILENAME)

        # Debug: Display the raw DataFrame
        #st.write("Raw Tennis Data:", raw_tennis_df.head())

        # Columns to extract from the CSV
        columns = ["current", "points", "displayName", "country", "countryFlag", "picture","birthPlace", "age"]

        # Check for missing columns in the CSV
        missing_columns = [col for col in columns if col not in raw_tennis_df.columns]
        if missing_columns:
            st.warning(f"Missing columns in the CSV: {missing_columns}")

        # Filter the DataFrame to include only the desired columns
        tennis_df = raw_tennis_df[[col for col in columns if col in raw_tennis_df.columns]]

        # Ensure numeric columns are properly converted
        numeric_columns = ["current", "points", "age"]
        for col in numeric_columns:
            if col in tennis_df.columns:
                tennis_df[col] = pd.to_numeric(tennis_df[col], errors='coerce')

        return tennis_df

    except FileNotFoundError:
        st.error("The file 'tennis_data.csv' was not found. Please ensure it's in the 'data' folder.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"An error occurred while reading the data: {e}")
        return pd.DataFrame()


# Call the function to load the tennis data
tennis_df = get_tennis_data()

# Display the DataFrame in the Streamlit app
#if not tennis_df.empty:
    #st.dataframe(tennis_df)
#else:
    #st.warning("No data available to display.")


# -----------------------------------------------------------------------------
# Draw the actual page

# Set the title that appears at the top of the page.
'''
# 🎾 TENNIS dashboard 2019

Browse Tennis data from the ESPN website. As you'll
notice, the ranking goes from 1-150, for the year of 2019.
'''

# Add some spacing
''
''
#set boundary values for ananlysis of short or long term
min_value = tennis_df['current'].min()
max_value = tennis_df['current'].max()
#slider to set limits
from_rank, to_rank = st.slider(
    'Which range of ranking are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])
#filtered data according to slider choices
filtered_tennis_df = tennis_df[
    (tennis_df['current'] >= from_rank) & (tennis_df['current'] <= to_rank)
    ]
''
''
st.title('Age vs. Points interactive plot')
# Display the data in the plot
if not filtered_tennis_df.empty:
    st.write("Filtered Tennis Data:")


    fig = px.scatter(
    filtered_tennis_df,
    x="age",
    y="points",
    color="displayName",  # Color change for each player
    hover_data={
        "displayName": True,  # display name of players
        "country": True,      # country
        "points": True,       # total points
        "age": True           # age
    },
    title="Age vs Points",
    labels={"age": "Age", "points": "Points"},  # Customize axis labels
    size_max=15,  # Maximum marker size
)

# Customize the layout
fig.update_layout(
    legend_title="Player Name",
    title_font_size=18,
    xaxis_title="Age",
    yaxis_title="Points",
    template="plotly_white",  # Use a clean theme
)

# Display the Plotly chart in Streamlit
st.plotly_chart(fig, use_container_width=True)

''
''
# Aggregated points by country
country_points = filtered_tennis_df.groupby("country").agg({"points": "sum"}).reset_index()

# Display pie chart of total points by country
st.write("### Total Points by Country (Interactive Pie Chart)")
fig = px.pie(
    country_points,
    values="points",
    names="country",
    title="Total Points by Country (Filtered Data)",
    hover_data=["points"],
    labels={"points": "Total Points"},
    color_discrete_sequence=px.colors.sequential.RdBu
)
st.plotly_chart(fig, use_container_width=True)


# Country selection for detailed breakdown
st.title("Player Points by Country")
selected_country = st.selectbox(
    "Select a country to their players:",
    options=country_points["country"].unique(),
    index=0
)

# Filter players by selected country
country_filtered_df = filtered_tennis_df[filtered_tennis_df["country"] == selected_country][["displayName", "points"]]


# Bar chart for player points within the selected country
st.write(f"### Player Points Breakdown - {selected_country}")
fig_bar = px.bar(
    country_filtered_df,
    x="displayName",
    y="points",
    title=f"Points by Player - {selected_country}",
    text="points",
    labels={"displayName": "Player", "points": "Points"},
    color="points",
    color_continuous_scale="Blues"
)
st.plotly_chart(fig_bar, use_container_width=True)

''
''

# Assuming tennis_df is already defined and loaded
if not all(col in filtered_tennis_df.columns for col in ["country", "points", "displayName", "age"]):
    st.error("Missing required columns in the tennis data.")
    st.stop()
#interactive map according to filtered data
st.title('Interactive Map of Tennis Players - 2019 Rankings')

st.markdown(f"This map shows the top {filtered_tennis_df['current'].max()} tennis players in 2019, their birth countries, and ranking points.")

fig = px.scatter_geo(
    filtered_tennis_df,
    locations="country",
    locationmode="country names",
    size="points",
    hover_name="displayName",
    hover_data={"points": True, "country": True, "age": True},
    title="Top Tennis Players by Country (2019)",
    projection="natural earth",
)

fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="lightgray",
        showcountries=True,
        countrycolor="white"
    ),
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
)

st.plotly_chart(fig, use_container_width=True)

''
''
''
st.title('"I have two lives, and all the problems I might have, I feel like I drop them once I step on to the match court.""')

st.title('~ Roger Federer')

''
''
st.title('Great game!🎾')

''
''
