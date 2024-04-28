import streamlit as st
import pandas as pd
from streamlit_folium import folium_static
import folium
import sqlite3

# Function to fetch data from the SQLite database
def fetch_data(query):
    conn = sqlite3.connect('airbnb6.db')
    cursor = conn.cursor()
    cursor.execute(query)
    data = cursor.fetchall()
    conn.close()
    return data

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
        p.amenity_wireless_internet,
        loc.latitude,
        loc.longitude
    FROM Listings l
    JOIN Property p ON l.Property_ID = p.Property_ID
    JOIN Location loc ON l.Location_ID = loc.Location_ID
    JOIN Price pr ON l.Price_ID = pr.Price_ID
    JOIN Review r ON l.Review_ID = r.Review_ID
"""

# Fetch data from the database
listing_data = fetch_data(query)

# Create DataFrame
df = pd.DataFrame(listing_data, columns=['Property_ID', 'Property_Type', 'Bedrooms', 'Bathrooms', 'Price', 'City', 'Review_Scores_Rating', 'Amenity_Wireless_Internet', 'Amenity_Kitchen', 'Latitude', 'Longitude'])

# Interactive filters
price_range = st.slider('Price Range', min_value=0, max_value=500, value=(0, 500), step=10)
rating_range = st.slider('Rating Range', min_value=0, max_value=100, value=(0, 100), step=1)

# Bedrooms and Bathrooms in the same row
col1, col2 = st.columns([1, 1])
with col1:
    bedrooms_count = st.number_input('Bedrooms', min_value=1, max_value=10, step=1, value=None)
with col2:
    bathrooms_count = st.number_input('Bathrooms', min_value=1, max_value=10, step=1, value=None)

# City and Amenities in the same row
col1, col2 = st.columns([1, 1])
with col1:
    cities = df['City'].unique()
    selected_city = st.selectbox('City', options=['Any'] + list(cities))
with col2:
    selected_amenities = st.multiselect('Amenities', options=['Wireless Internet', 'Kitchen'])

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
        amenity_column = 'Amenity_' + amenity.lower().replace(' ', '_')
        filtered_data = filtered_data[filtered_data[amenity_column] == 'Yes']

# Number input for page navigation
page_value = st.number_input('Page', min_value=1, max_value=int(len(filtered_data) / 20) + 1, value=1)

# Calculate start and end index for current page
start_index = (page_value - 1) * 20
end_index = min(page_value * 20, len(filtered_data))

# Display filtered data with pagination, set table width to 100% and apply custom CSS
st.markdown(
    f'<style>.dataframe tbody tr {{border: 1px solid #dddddd;}} .dataframe thead th {{background-color: #dddddd;}}</style>',
    unsafe_allow_html=True
)
st.table(filtered_data[start_index:end_index].style.set_table_attributes('style="width: 100%;"'))


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
            icon=folium.Icon(color='green' if row['Review_Scores_Rating'] >= 4.5 else 'red')
        ).add_to(m)

    # Display the map
    folium_static(m)
