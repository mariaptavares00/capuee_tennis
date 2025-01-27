import streamlit as st
import pandas as pd
import math
import requests
from pathlib import Path
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
from datetime import date, datetime, timedelta

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
        st.write("Raw Tennis Data:", raw_tennis_df.head())

        # Columns to extract from the CSV
        columns = ["current", "points", "displayName", "country", "countryFlag", "picture", "age"]

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
if not tennis_df.empty:
    st.dataframe(tennis_df)
else:
    st.warning("No data available to display.")


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

min_value = tennis_df['current'].min()
max_value = tennis_df['current'].max()

from_rank, to_rank = st.slider(
    'Which range of ranking are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

countries = tennis_df['country'].unique()

# Check if the `countries` list is empty
if not len(countries):
    st.warning("Check Data for a country")

# Default selection based on your provided list
default_selected = [
    "Spain", "Serbia", "Switzerland", "Austria", "Russia", "Greece", "Germany", "Italy",
    "France", "Belgium", "Japan", "Argentina", "Canada", "Australia", "USA", "Bulgaria",
    "Croatia", "Poland", "Great Britain", "Norway", "Portugal", "Lithuania", "Kazakhstan",
    "Hungary", "Sweden", "Bolivia", "Korea", "Brazil", "South Africa", "Bosnia and Herzegovina", "Belarus"
]

# Create the multiselect widget
selected_countries = st.multiselect(
    'Select one or more countries:',
    options=countries,
    default=[country for country in default_selected if country in countries]
)

''
''
''
st.title('Interactive Map of Tennis Players - 2019 Rankings')

st.markdown('This map shows the top {max_value} tennis players in 2019, their birth countries and ranking points')

# Create the map using Plotly Express
fig = px.scatter_geo(
    df,
    locations="country",  # Geolocate using country names
    locationmode="country names",  # Match with country names
    size="points",  # Marker size based on points
    hover_name="displayName",  # Show player's full name on hover
    hover_data={"points": True, "country": True, "age": True},  # Show additional info
    title="Top Tennis Players by Country (2019)",
    projection="natural earth",  # Use a natural earth projection
)

# Customize map layout
fig.update_layout(
    geo=dict(
        showland=True,
        landcolor="lightgray",
        showcountries=True,
        countrycolor="white"
    ),
    margin={"r": 0, "t": 30, "l": 0, "b": 0},
)

# Display the map in Streamlit
st.plotly_chart(fig, use_container_width=True)


''
''
''


# Filter the data
filtered_tennis_df = tennis_df[
    (tennis_df['country'].isin(selected_countries))
    & (tennis_df['Year'] <= to_year)
    & (from_year <= gdp_df['Year'])
]

st.header('Tennis Rankings', divider='gray')

''


st.line_chart(
    filtered_tennis_df,
    x='Year',
    y='GDP',
    color='Country Code',
)

''
''
