# Spotify Content-Based Recommendation System and Data Visualization
<img src="./items/Spotify.png" alt="Logo" width="200"/>

This is a web application that provides users with personalized Spotify music recommendations based on their listening history and music preferences. Using a combination of TensorFlow for machine learning and the Spotify API for data collection, the Streamlit application displays engaging visualizations of popular and user-specific music trends. The application is built with a Taipy or Streamlit GUI for an interactive and user-friendly experience.

## Demo
https://github.com/user-attachments/assets/81fc10a7-6f98-4ed4-a0d3-7b8e58d87ba5

## Features

- **Global Spotify Statistics**: View the most-streamed songs, trending artists, and popular albums.
- **User-Specific Insights**: Discover your most listened-to songs, favorite artists, and recent listening trends.
- **Content-Based Recommendations**: Get personalized song recommendations based on your listening history using a content-based recommendation model built with TensorFlow.
- **Interactive UI**: Explore data through a visually appealing and interactive web interface.

## Tech Stack

- **Frontend**: Streamlit for an interactive and responsive user interface.
- **Machine Learning**: TensorFlow for building a content-based recommendation model.
- **Backend**: 
    - **APIs**: Spotify API for collecting user listening data.
    - **Visualization**: plotly for interactive visualizations.
- **Data Visualization**: Matplotlib, Seaborn, and Pandas for statistical visualization.

## Setup
<!-- start with conda environment from yml -->
1. Clone the repository
```git clone https://github.com/kailinxGitHub/Spotify-UnWrapped-Spotify-Content-Based-Recommendation-System-and-Data-Visualization.git```
2. Conda environment
```conda env create -f environment.yml```
3. Activate the environment
```conda activate SpotifyUnWrapped```
4. Run the Streamlit application
```streamlit run app.py```
5. Open the Streamlit app in your browser at `http://localhost:8501`

## Usage

- **Home**: The Welcoming Page
- **Explore**: Explore global music trends and statistics.
- **User Profile**: Log in with your Spotify account to view your personal listening stats.
- **Recommendations**: Discover new music tailored to your taste based on song features.

## License

This project is licensed under the MIT License.

---

## Contributing

Contributions are welcome! Please submit a pull request for any improvements or suggestions.

---

## Acknowledgments
- [Top 100 Spotify Songs History](https://www.kaggle.com/code/varunsaikanuri/spotify-data-visualization/input)
- [Spotify API](https://developer.spotify.com/)
- [TensorFlow](https://www.tensorflow.org/)
- [Get Playlist Data](https://medium.com/@shruti.somankar/building-a-music-recommendation-system-using-spotify-api-and-python-f7418a21fa41)
- [For the SpotiPy page](https://levelup.gitconnected.com/how-to-build-a-music-recommendation-system-with-python-and-spotify-api-using-streamlit-5488d316aabd)
- [for the SpotifyAPI class](https://towardsdatascience.com/how-to-utilize-spotifys-api-and-create-a-user-interface-in-streamlit-5d8820db95d5)
