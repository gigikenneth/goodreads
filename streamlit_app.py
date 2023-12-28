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

# Function for most common authors
def plot_common_authors(data, year=None):
    if year:
        data = data[data['Date Added'].dt.year == year]
    author_counts = Counter(data['Author'])
    authors_df = pd.DataFrame(author_counts.most_common(10), columns=['Author', 'Count'])
    fig = px.bar(authors_df, x='Count', y='Author', title=f'Most Common Authors {"in " + str(year) if year else ""}',
                 orientation='h', color_discrete_sequence=["lightpink"])
    return fig

# Function for distribution of books by publication year
def plot_books_by_publication_year(data):
    fig = px.histogram(data, x='Year Published', title='Distribution of Books by Publication Year',
                       color_discrete_sequence=["lightgreen"])
    return fig

# Function for cumulative books plot
def plot_cumulative_books(data, year=None):
    if year:
        data = data[data['Date Added'].dt.year == year]
    data_sorted = data.sort_values('Date Added')
    data_sorted['Cumulative Books'] = range(1, len(data_sorted) + 1)
    fig = px.line(data_sorted, x='Date Added', y='Cumulative Books', 
                  title=f'Cumulative Number of Books Added Over Time {"in " + str(year) if year else ""}',
                  color_discrete_sequence=['lightblue'])
    return fig

# Function for the distribution of book lengths
def plot_book_lengths(data):
    valid_page_data = data[data['Number of Pages'].notna() & (data['Number of Pages'] > 0)]
    fig = px.histogram(valid_page_data, x='Number of Pages', title='Distribution of Book Lengths (Number of Pages)',
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

# Sidebar for file upload
with st.sidebar:
    uploaded_file = st.file_uploader("Upload your Goodreads CSV", type="csv")

if uploaded_file is not None:
    data = load_data(uploaded_file)

    # Book Ratings Plot
    st.subheader("Distribution of Book Ratings")
    fig1 = plot_book_ratings(data)
    st.plotly_chart(fig1)
    st.markdown("This histogram shows the distribution of your book ratings.")

    # Book Ratings Plot for 2023
    st.subheader("Distribution of Book Ratings in 2023")
    fig2 = plot_book_ratings(data, year=2023)
    st.plotly_chart(fig2)
    st.markdown("Here's how you rated books added in 2023.")

    # Most Common Authors - Side by side comparison
    col1, col2 = st.columns(2)

    with col1:
        st.subheader("Most Common Authors")
        fig3 = plot_common_authors(data)
        st.plotly_chart(fig3)
        st.markdown("These are your top authors based on the number of their books in your library.")

    with col2:
        st.subheader("Most Common Authors in 2023")
        fig4 = plot_common_authors(data, year=2023)
        st.plotly_chart(fig4)
        st.markdown("In 2023, these authors dominated your reading list.")

    # Books by Publication Year
    st.subheader("Distribution of Books by Publication Year")
    fig5 = plot_books_by_publication_year(data)
    st.plotly_chart(fig5)
    st.markdown("This chart reveals the publication years of the books in your collection.")

    # Cumulative Books Plot
    st.subheader("Cumulative Number of Books Added Over Time")
    fig6 = plot_cumulative_books(data)
    st.plotly_chart(fig6)
    st.markdown("Observe the growth of your library over time.")

    # Cumulative Books in 2023
    st.subheader("Cumulative Number of Books Added in 2023")
    fig7 = plot_cumulative_books(data, year=2023)
    st.plotly_chart(fig7)
    st.markdown("Here's how your collection expanded in 2023.")

    # Book Lengths Plot
    st.subheader("Distribution of Book Lengths")
    fig8 = plot_book_lengths(data)
    st.plotly_chart(fig8)
    st.markdown("This shows the range of book lengths you prefer.")

    # Read vs. Unread Books Plot
    st.subheader("Read vs. Unread Books")
    fig9 = plot_read_unread_books(data)
    st.plotly_chart(fig9)
    st.markdown("Here's the proportion of books you've read vs. those still on your to-read list.")

    # Read vs. Unread Books in 2023
    st.subheader("Read vs. Unread Books in 2023")
    fig10 = plot_read_unread_books(data, year=2023)
    st.plotly_chart(fig10)
    st.markdown("This is the read vs. unread breakdown for books added in 2023.")

# Run this code in your Python environment after installing plotly and streamlit using 'pip install plotly streamlit'
# You can start the app by running 'streamlit run your_script_name.py' in the terminal
