import streamlit as st
import pandas as pd

st.title('IMDB Movie Data Analysis')

@st.cache_data
def load_data():
    data = pd.read_csv('imdb_movie_data.csv')
    # Clean up data
    # Remove parentheses and unwanted characters
    data.iloc[:, 1:] = data.iloc[:, 1:].replace({'\(|\)': '', 'I': '', " ": ""}, regex=True)
    # Handle specific characters from the third column onwards
    data.iloc[:, 2:] = data.iloc[:, 2:].replace({"'-": ''}, regex=True)
    # Rename columns
    data.columns = ['Movie Title', 'Year', 'Certificate', 'Genre 1', 'Genre 2', 'Genre 3', 
                    'IMDB Rating', 'Metascore', 'Runtime(Minutes)', 'Votes', 'Gross Earnings']
    return data

data = load_data()

# Create a unique list of genres
all_genres = pd.unique(data[['Genre 1', 'Genre 2', 'Genre 3']].values.ravel('K'))
all_genres = [genre for genre in all_genres if genre != '']

# Create a unique list of certificates, adding 'All' as the first option
all_certificates = ['All'] + list(pd.unique(data['Certificate'].values.ravel('K')))
all_certificates = [certificate for certificate in all_certificates if certificate != '']

# Multiselect widget for genre selection (defaults to all genres if none are selected)
selected_genres = st.multiselect('Select Genres', all_genres, default=all_genres)

# Single select widget for certificate selection (defaults to 'All')
selected_certificate = st.selectbox('Select Certificate', all_certificates, index=0)

# Columns for min and max IMDb rating inputs
col1, col2 = st.columns(2)
with col1:
    min_rating = st.text_input('Min Rating', value='0')
with col2:
    max_rating = st.text_input('Max Rating', value='10')

# Convert min and max ratings to float
try:
    min_rating = float(min_rating)
    max_rating = float(max_rating)
except ValueError:
    st.error('Please enter valid numbers for ratings')
    min_rating, max_rating = 0, 10

# Filter the data based on selected genres, certificate, and IMDb rating range
def filter_data(data, genres, certificate, min_rating, max_rating):
    genre_filter = (data['Genre 1'].isin(genres)) | (data['Genre 2'].isin(genres)) | (data['Genre 3'].isin(genres))
    certificate_filter = (data['Certificate'] == certificate) if certificate != 'All' else True
    rating_filter = (data['IMDB Rating'] >= min_rating) & (data['IMDB Rating'] <= max_rating)
    return data[genre_filter & certificate_filter & rating_filter].reset_index(drop=True)

filtered_data = filter_data(data, selected_genres, selected_certificate, min_rating, max_rating)

st.subheader('Filtered Data')
st.write(filtered_data)
