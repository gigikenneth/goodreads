import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import datetime

# Function to load data
def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    data['Date Added'] = pd.to_datetime(data['Date Added'], errors='coerce')
    data['Date Read'] = pd.to_datetime(data['Date Read'], errors='coerce')
    data['Year Published'] = pd.to_numeric(data['Year Published'], errors='coerce')
    return data

# Function for distribution of book ratings
def plot_book_ratings(data, year=None):
    if year:
        data = data[data['Date Added'].dt.year == year]
    fig = px.histogram(data, x='My Rating', title=f'Distribution of Book Ratings {"in " + str(year) if year else ""}',
                       color_discrete_sequence=["lightblue"])
    return fig

# Function for cumulative books plot
def plot_cumulative_books(data, year=None):
    if year:
        data = data[data['Date Added'].dt.year == year]
    data_sorted = data.sort_values('Date Added')
    data_sorted['Cumulative Books'] = range(1, len(data_sorted) + 1)
    fig = px.line(data_sorted, x='Date Added', y='Cumulative Books', 
                  title=f'Cumulative Number of Books Added {"in " + str(year) if year else ""}',
                  color_discrete_sequence=['lightblue'])
    return fig

# Function for the distribution of book lengths
def plot_book_lengths(data, year=None):
    if year:
        data = data[data['Date Added'].dt.year == year]
    valid_page_data = data[data['Number of Pages'].notna() & (data['Number of Pages'] > 0)]
    fig = px.histogram(valid_page_data, x='Number of Pages', 
                       title=f'Distribution of Book Lengths {"in " + str(year) if year else ""}',
                       color_discrete_sequence=["lightpink"])
    return fig

# Function for read vs. unread books
def plot_read_unread_books(data, year=None):
    if year:
        data = data[data['Date Added'].dt.year == year]
    read_books_count = (data['Read Count'] > 0).sum()
    unread_books_count = (data['Read Count'] == 0).sum()
    counts = [read_books_count, unread_books_count]
    labels = ['Read Books', 'Unread Books']
    fig = px.pie(names=labels, values=counts, title=f'Read vs. Unread Books {"in " + str(year) if year else ""}',
                 color_discrete_sequence=["lightgreen", "lightblue"])
    return fig

# Customizing Streamlit's theme
st.set_page_config(page_title="Goodreads Wrapped", layout="wide")

# Main Streamlit app
st.title("Goodreads Wrapped")

# Sidebar for file upload and year selection
with st.sidebar:
    uploaded_file = st.file_uploader("Upload your Goodreads CSV", type="csv")
    if uploaded_file is not None:
        data = load_data(uploaded_file)
        min_year = int(data['Date Added'].dt.year.min())
        max_year = int(data['Date Added'].dt.year.max())
        year = st.select_slider("Select Year", options=range(min_year, max_year + 1), value=max_year)

if uploaded_file is not None:
    # Book Ratings Plot - Side by side comparison
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribution of Book Ratings")
        fig1 = plot_book_ratings(data)
        st.plotly_chart(fig1)
    with col2:
        st.subheader(f"Distribution of Book Ratings in {year}")
        fig2 = plot_book_ratings(data, year=year)
        st.plotly_chart(fig2)

    # Cumulative Books Plot - Side by side comparison
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Cumulative Number of Books Added Over Time")
        fig3 = plot_cumulative_books(data)
        st.plotly_chart(fig3)
    with col2:
        st.subheader(f"Cumulative Number of Books Added in {year}")
        fig4 = plot_cumulative_books(data, year=year)
        st.plotly_chart(fig4)

    # Book Lengths Plot - Side by side comparison
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribution of Book Lengths")
        fig5 = plot_book_lengths(data)
        st.plotly_chart(fig5)
    with col2:
        st.subheader(f"Distribution of Book Lengths in {year}")
        fig6 = plot_book_lengths(data, year=year)
        st.plotly_chart(fig6)

    # Read vs. Unread Books Plot - Side by side comparison
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Read vs. Unread Books")
        fig7 = plot_read_unread_books(data)
        st.plotly_chart(fig7)
    with col2:
        st.subheader(f"Read vs. Unread Books in {year}")
        fig8 = plot_read_unread_books(data, year=year)
        st.plotly_chart(fig8)

# Run this code in your Python environment after installing plotly and streamlit using 'pip install plotly streamlit'
# You can start the app by running 'streamlit run your_script_name.py' in the terminal
