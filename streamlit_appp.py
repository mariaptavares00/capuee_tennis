import streamlit as st
import pandas as pd
import math
import requests
from pathlib import Path
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

min_value = tennis_df['current'].min()
max_value = tennis_df['current'].max()

from_rank, to_rank = st.slider(
    'Which range of ranking are you interested in?',
    min_value=min_value,
    max_value=max_value,
    value=[min_value, max_value])

filtered_tennis_df = tennis_df[
    (tennis_df['current'] >= min_rank) & (tennis_df['current'] <= max_rank)
    ]
''
''
st.title('Age vs. Points')
# Display the data
if not tennis_df.empty:
    st.write("Filtered Tennis Data:", tennis_df)

    # Filter data for the scatter plot
    df_age_points = tennis_df[["age", "points", "displayName"]].dropna()

    # Create the plot
    st.write("### Age vs Points Scatter Plot")
    plt.figure(figsize=(8, 6))
    sns.scatterplot(
        x="age",
        y="points",
        hue="displayName",
        data=df_age_points,
        s=100,
        palette="tab10"
    )
    plt.title("Age vs Points", fontsize=16)
    plt.xlabel("Age")
    plt.ylabel("Points")
    plt.legend(title="Player", bbox_to_anchor=(1.05, 1), loc="upper left", fontsize=8)
    plt.tight_layout()

    # Show the plot in the Streamlit app
    st.pyplot(plt)

''
''
st.title('Interactive Map of Tennis Players - 2019 Rankings')

st.markdown('This map shows the top {max_value} tennis players in 2019, their birth countries and ranking points')

# geocoding birthplaces from players
geolocator = Nominatim(user_agent="tennis_dashboard")

def geocode_birthplace(row):
    try:
        # Geocode the birthPlace value
        location = geolocator.geocode(row['birthPlace'])
        if location:
            return pd.Series([location.latitude, location.longitude])
        else:
            return pd.Series([None, None])
    except Exception as e:
        return pd.Series([None, None])

# Add latitude and longitude columns to the DataFrame
filtered_tennis_df[['latitude', 'longitude']] = filtered_tennis_df.apply(geocode_birthplace, axis=1)



# Check if latitude and longitude columns exist
if not all(col in tennis_df.columns for col in ["latitude", "longitude"]):
    st.error("Latitude and Longitude columns are missing. Please geocode the data.")
    st.stop()

# Create the map
fig = px.scatter_geo(
    filtered_tennis_df,
    lat="latitude",  # Use latitude column for location
    lon="longitude",  # Use longitude column for location
    size="points",  # Use points for marker size
    hover_name="displayName",  # Display player name on hover
    hover_data={"points": True, "birthPlace": True, "age": True},  # Additional hover info
    title="Top Tennis Players by Birthplace (2019)",
    projection="natural earth"  # Use a natural earth projection
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

st.title('Thank you!')

''
''
