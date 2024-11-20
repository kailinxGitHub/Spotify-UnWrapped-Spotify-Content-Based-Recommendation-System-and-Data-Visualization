import streamlit as st
import pandas as pd
import plotly.express as px

# the table for top 100
def top_100_table():
    df = pd.read_csv("data/top100.csv")
    df.to_parquet("large_file.parquet")
    df = df.sort_values(by="streams", ascending=False)
    df = df[["title", "artist", "streams", "date", "url"]]
    return df

# the chart for top 100
def top_100_plotly_chart():
    top_100 = top_100_table()
    fig = px.bar(top_100.head(10), x='title', y='streams', color='artist', title='Top 10 Streamed Songs')
    st.plotly_chart(fig)

# the treemap for top 100
def top_100_treemap():
    top_100 = top_100_table()
    fig = px.treemap(top_100, path=['artist', 'title'], values='streams',
                 title="Regional Popularity of Top 100 Songs by Artist and Song")
    
# the top 100 over time functionality in streamlit
def top_100_over_time():
    top_100 = top_100_table()
    top_100['date'] = pd.to_datetime(top_100['date'], format="%Y-%m-%d")
    top_100['year'] = top_100['date'].dt.year

    top_100 = top_100.sort_values(by=['year', 'streams'], ascending=[True, False])

    st.title("Top Songs Over Time")
    st.write("Use the slider to explore the most streamed songs in specific years.")

    min_year = top_100['year'].min()
    max_year = top_100['year'].max()
    selected_year = st.slider("Select a Year", min_year, max_year, value=min_year, step=1)

    filtered_top_100 = top_100[top_100['year'] == selected_year].nlargest(3, 'streams')

    fig = px.bar(
        filtered_top_100,
        x='streams', 
        y='title',
        color='artist',
        title=f"Top Songs in {selected_year}",
        labels={'streams': 'Stream Count', 'title': 'Song Title'},
        hover_data={'artist': True, 'streams': True}
    )

    fig.update_layout(
        xaxis_title="Stream Count",
        yaxis_title="Top Songs",
        yaxis={'categoryorder':'total ascending'}
    )

    st.plotly_chart(fig)