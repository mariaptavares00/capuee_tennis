import streamlit as st
import pandas as pd
import math
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

#url = "https://sports-information.p.rapidapi.com/tennis/rankings"
#querystring = {"year":"2019"}

@st.cache_data
def get_tennis_data():
    """Grab tennis data from a CSV file.

    This uses caching to avoid having to read the file every time.
    """

    #headers = {
	#"x-rapidapi-key": "60751bcf50msh7f1cc568ebc9aeep1ad40bjsn94769488bc2e",
	#"x-rapidapi-host": "sports-information.p.rapidapi.com"
    #}

    #response = requests.get(url, headers=headers, params=querystring)

    #raw_tennis_df = response.json()


    # Load data from CSV
    DATA_FILENAME = Path(__file__).parent / 'data/tennis_data.csv'
    raw_tennis_df = pd.read_csv(DATA_FILENAME)

    min_rank = 1
    max_rank = 150

    # Filter players based on their current ranking (between min_rank and max_rank)
    #filtered_tennis_df = raw_tennis_df[
    #    (raw_tennis_df["current"] >= min_rank) & (raw_tennis_df["current"] <= max_rank)
    #]

    # Selecting only the desired columns for the dashboard
    #tennis_df = filtered_tennis_df[[
    #    "current", "points", "displayName", "country", "countryFlag", "picture", "age"
    #]]

    tennis_df = raw_tennis_df[
        "current", "points", "displayName", "country", "countryFlag", "picture", "age"
    ]



    # convert from strings to integers
    tennis_df['current'] = pd.to_numeric(tennis_df['current'])
    tennis_df['points'] = pd.to_numeric(tennis_df['points'])
    tennis_df['age'] = pd.to_numeric(tennis_df['age'])

    return tennis_df
tennis_df = get_tennis_data()


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
