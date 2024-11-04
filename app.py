import streamlit as st

st.set_page_config(
    page_title="Spotify UnWrapped",
    page_icon="👋",
)

st.write("# Welcome to Spotify UnWrapped! 👋")

contentFromReadme = '''
- **LinkedIn**: [Kailin Xing](https://www.linkedin.com/in/kailinx/)
- **GitHub**: [Spotify UnWrapped](https://github.com/kailinxGitHub/Spotify-UnWrapped-Spotify-Content-Based-Recommendation-System-and-Data-Visualization)

This is a web application that provides users with personalized Spotify music recommendations based on their listening history and music preferences. 
Using a combination of TensorFlow for machine learning and the Spotify API for data collection, the Streamlit application displays engaging visualizations of popular and user-specific music trends. 
The application is built with a Taipy or Streamlit GUI for an interactive and user-friendly experience.

### Features
- **Global Spotify Statistics**: View the most-streamed songs, trending artists, and popular albums.
- **User-Specific Insights**: Discover your most listened-to songs, favorite artists, and recent listening trends.
- **Content-Based Recommendations**: Get personalized song recommendations based on your listening history using a content-based recommendation model built with TensorFlow.
- **Interactive UI**: Explore data through a visually appealing and interactive web interface.

### Tech Stack
- **Frontend**: Streamlit for an interactive and responsive user interface.
- **Machine Learning**: TensorFlow for building a content-based recommendation model.
- **Backend**: Spotify API (via Spotipy) for accessing music data and user-specific information.
- **Data Visualization**: Matplotlib, Seaborn, and Pandas for statistical visualization.

### Usage
- **Home**: The Welcoming Page
- **Explore**: Explore global music trends and statistics.
- **User Profile**: Log in with your Spotify account to view your personal listening stats.
- **Recommendations**: Discover new music tailored to your taste based on song features.
'''

st.markdown(contentFromReadme)