import streamlit as st
import pandas as pd
from components.top_100_table import top_100_table, top_100_plotly_chart, top_100_treemap, top_100_over_time
from datetime import timedelta

# configures the page
st.set_page_config(
    page_title="Explore", 
    page_icon=":world_map:", 
    layout="centered"
)

# main content
st.write("# Explore Global Music Trends 🌍")
top_100 = top_100_table()
st.dataframe(top_100)
top_100_plotly_chart()
top_100_treemap()
top_100_over_time()