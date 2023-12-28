import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
import datetime

# Function to load data
def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    # Perform any necessary data preprocessing here
    data['Date Added'] = pd.to_datetime(data['Date Added'], errors='coerce')
    return data

# Function for cumulative books plot using plotly
def plot_cumulative_books(data):
    data_sorted = data.sort_values('Date Added')
    data_sorted['Cumulative Books'] = range(1, len(data_sorted) + 1)
    fig = px.line(data_sorted, x='Date Added', y='Cumulative Books', 
                  title='Cumulative Number of Books Added Over Time',
                  labels={'Date Added': 'Date', 'Cumulative Books': 'Total Number of Books'})
    return fig

# Function for the distribution of book lengths using plotly
def plot_book_lengths(data):
    valid_page_data = data[data['Number of Pages'].notna() & (data['Number of Pages'] > 0)]
    fig = px.histogram(valid_page_data, x='Number of Pages', 
                       title='Distribution of Book Lengths (Number of Pages)',
                       labels={'Number of Pages': 'Number of Pages'})
    return fig

# Main Streamlit app
st.title("Goodreads Library Analysis")

uploaded_file = st.file_uploader("Upload your Goodreads CSV", type="csv")
if uploaded_file is not None:
    data = load_data(uploaded_file)

    # Cumulative Books Plot
    st.subheader("Cumulative Number of Books Added Over Time")
    fig1 = plot_cumulative_books(data)
    st.plotly_chart(fig1)
    st.markdown("### Insight")
    st.write("Your reading journey over time shows...")

    # Distribution of Book Lengths
    st.subheader("Distribution of Book Lengths")
    fig2 = plot_book_lengths(data)
    st.plotly_chart(fig2)
    st.markdown("### Insight")
    st.write("The variety of book lengths in your library indicates...")

    # Add other plots and insights here

    # Example of a dynamic insight
    current_year = datetime.datetime.now().year
    books_this_year = data[data['Date Added'].dt.year == current_year]
    st.write(f"You've added {len(books_this_year)} books to your library in {current_year}!")

# Run this code in your Python environment after installing plotly and streamlit using 'pip install plotly streamlit'
# You can start the app by running 'streamlit run your_script_name.py' in the terminal
