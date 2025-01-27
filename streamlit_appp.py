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

@st.cache_data
def get_tennis_data():
    """Grab tennis data from a CSV file.

    This uses caching to avoid having to read the file every time. If we were
    reading from an HTTP endpoint instead of a file, it's a good idea to set
    a maximum age to the cache with the TTL argument: @st.cache_data(ttl='1d')
    """

    # Instead of a CSV on disk, you could read from an HTTP endpoint here too.
    DATA_FILENAME = Path(__file__).parent/'data/tennis_data.csv'
    raw_gdp_df = pd.read_csv(DATA_FILENAME)

    min_rank = 1
    max_rank = 100


    # Filter players based on their current ranking (between min_rank and max_rank)
    tennis_df = tennis_df[(tennis_df["current"] >= min_rank) & (tennis_df["current"] <= max_rank)]

    # Selecting only the desired columns for the dashboard
    tennis_df = raw_tennis_df[["current", "points", "displayName", "country", "countryFlag", "picture", "age"]]


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


first_year = gdp_df[gdp_df['Year'] == from_year]
last_year = gdp_df[gdp_df['Year'] == to_year]

st.header(f'GDP in {to_year}', divider='gray')

''

cols = st.columns(4)

for i, country in enumerate(selected_countries):
    col = cols[i % len(cols)]

    with col:
        first_gdp = first_year[first_year['Country Code'] == country]['GDP'].iat[0] / 1000000000
        last_gdp = last_year[last_year['Country Code'] == country]['GDP'].iat[0] / 1000000000

        if math.isnan(first_gdp):
            growth = 'n/a'
            delta_color = 'off'
        else:
            growth = f'{last_gdp / first_gdp:,.2f}x'
            delta_color = 'normal'

        st.metric(
            label=f'{country} GDP',
            value=f'{last_gdp:,.0f}B',
            delta=growth,
            delta_color=delta_color
        )
