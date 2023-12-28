pip install matplotlib

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
import datetime

# Function to load data
def load_data(uploaded_file):
    data = pd.read_csv(uploaded_file)
    # Perform any necessary data preprocessing here
    data['Date Added'] = pd.to_datetime(data['Date Added'], errors='coerce')
    return data

# Function for cumulative books plot
def plot_cumulative_books(data):
    data_sorted = data.sort_values('Date Added')
    data_sorted['Cumulative Books'] = range(1, len(data_sorted) + 1)
    plt.figure(figsize=(12, 6))
    plt.plot(data_sorted['Date Added'], data_sorted['Cumulative Books'])
    plt.title('Cumulative Number of Books Added Over Time')
    plt.xlabel('Date')
    plt.ylabel('Total Number of Books')
    plt.grid(True)

# Function for the distribution of book lengths
def plot_book_lengths(data):
    valid_page_data = data[data['Number of Pages'].notna() & (data['Number of Pages'] > 0)]
    plt.figure(figsize=(12, 6))
    sns.histplot(valid_page_data['Number of Pages'], bins=30, kde=True)
    plt.title('Distribution of Book Lengths (Number of Pages)')
    plt.xlabel('Number of Pages')
    plt.ylabel('Number of Books')
    plt.grid(True)

# Main Streamlit app
st.title("Goodreads Library Analysis")

uploaded_file = st.file_uploader("Upload your Goodreads CSV", type="csv")
if uploaded_file is not None:
    data = load_data(uploaded_file)

    # Cumulative Books Plot
    st.subheader("Cumulative Number of Books Added Over Time")
    plot_cumulative_books(data)
    st.pyplot(plt)
    st.markdown("### Insight")
    st.write("Your reading journey over time shows...")

    # Distribution of Book Lengths
    st.subheader("Distribution of Book Lengths")
    plot_book_lengths(data)
    st.pyplot(plt)
    st.markdown("### Insight")
    st.write("The variety of book lengths in your library indicates...")

    # Add other plots and insights here

    # Example of a dynamic insight
    current_year = datetime.datetime.now().year
    books_this_year = data[data['Date Added'].dt.year == current_year]
    st.write(f"You've added {len(books_this_year)} books to your library in {current_year}!")

# Run this code in your Python environment after installing streamlit using 'pip install streamlit'
# You can start the app by running 'streamlit run your_script_name.py' in the terminal

