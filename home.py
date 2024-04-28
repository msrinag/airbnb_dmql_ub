import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import sqlite3

# Function to fetch data from the SQLite database
def fetch_data(query):
    conn = sqlite3.connect('airbnb.db')
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

#setting view to wide looks better to view table data
st.set_page_config(layout="wide")

# SQL query
query = """
    SELECT DISTINCT 
        p.Property_ID, 
        p.property_type, 
        p.bedrooms,
        p.bathrooms,
        pr.price,
        loc.city, 
        r.review_scores_rating,
        p.amenity_wireless_internet,     
        p.Amenity_air_conditioning,
        p.Amenity_free_parking_on_premises,
        p.amenity_tv,
        loc.latitude,
        loc.longitude
    FROM Listings l
    JOIN Property p ON l.Property_ID = p.Property_ID
    JOIN Location loc ON l.Location_ID = loc.Location_ID
    JOIN Price pr ON l.Price_ID = pr.Price_ID
    JOIN Review r ON l.Review_ID = r.Review_ID
"""

# initial featch and store in chace for dynamic view 

def select_columns(df, cols_to_ignore):
    cols_to_select = [col for col in df.columns if col not in cols_to_ignore]
    return df[cols_to_select]
# for filtering df views etc 

# Fetch data from the database
listing_data = fetch_data(query)

# Create DataFrame
df = pd.DataFrame(listing_data, columns=['Property_ID', 'Property_Type', 'Bedrooms', 'Bathrooms', 'Price', 'City', 'Review_Scores_Rating', 'Amenity Wireless Internet', 'Amenity Air Conditioning', 'Amenity Free Parking On Premises', 'Amenity TV','Latitude','Longitude'])

# Interactive filters
price_range = st.slider('Price Range', min_value=0, max_value=df['Price'].max(), value=(0, df['Price'].max()), step=10)
rating_range = st.slider('Rating Range', min_value=0, max_value=100, value=(0, 100), step=1)

# Bedrooms and Bathrooms in the same row
col1, col2 = st.columns([1, 1])
with col1:
    bedrooms_count = st.select_slider('Bedrooms', options=['Any'] + list(range(1, 11)), value=None)
    # Convert 'Any' selection to None
    if bedrooms_count == 'Any':
        bedrooms_count = None
with col2:
    bathrooms_count = st.select_slider('Bathrooms', options=['Any'] + list(range(1, 11)), value=None)
    # Convert 'Any' selection to None
    if bathrooms_count == 'Any':
        bathrooms_count = None

# City and Amenities in the same row
col1, col2 = st.columns([1, 1])
with col1:
    cities = df['City'].unique()
    selected_city = st.selectbox('City', options=['Any'] + list(cities))
with col2:
    selected_amenities = st.multiselect('Amenities', options=['Wireless Internet', 'Air Conditioning', 'Free Parking On Premises', 'TV'])

# Filter data based on user input
filtered_data = df[(df['Price'].between(price_range[0], price_range[1])) &
                   (df['Review_Scores_Rating'].between(rating_range[0], rating_range[1]))]

if bedrooms_count is not None:
    filtered_data = filtered_data[filtered_data['Bedrooms'] == bedrooms_count]

if bathrooms_count is not None:
    filtered_data = filtered_data[filtered_data['Bathrooms'] == bathrooms_count]

if selected_city != 'Any':
    filtered_data = filtered_data[filtered_data['City'] == selected_city]

if selected_amenities:
    for amenity in selected_amenities:
        amenity_column = 'Amenity ' + amenity
        filtered_data = filtered_data[filtered_data[amenity_column] == 'Yes']

# Number input for page navigation
page_value = st.number_input('Page', min_value=1, max_value=int(len(filtered_data) / 20) + 1, value=1)

# Calculate start and end index for current page
start_index = (page_value - 1) * 20
end_index = min(page_value * 20, len(filtered_data))

cols_to_ignore=['Latitude','Longitude']
st.table(select_columns(filtered_data[start_index:end_index], cols_to_ignore))

# Show results on map button
if st.button('View Results on Map'):
    # Create a map centered on the average latitude and longitude of filtered data
    avg_latitude = filtered_data['Latitude'].mean()
    avg_longitude = filtered_data['Longitude'].mean()
    m = folium.Map(location=[avg_latitude, avg_longitude], zoom_start=10)

    # Add markers for each listing in the current page
    for index, row in filtered_data[start_index:end_index].iterrows():
        folium.Marker(
            location=[row['Latitude'], row['Longitude']],
            popup=f"Property ID: {row['Property_ID']} - Rating: {row['Review_Scores_Rating']} - Price: {row['Price']}",
            icon=folium.Icon(color='green' if row['Review_Scores_Rating'] >= 80 else 'red')
        ).add_to(m)

    # Display the map
    folium_static(m)
