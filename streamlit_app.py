import streamlit as st
import pandas as pd
import plotly.express as px
from collections import Counter
from wordcloud import WordCloud
import matplotlib.pyplot as plt

# Path to the local example CSV file
example_csv_file = "goodreads_library_export.csv"

# Function to load data
def load_data(uploaded_file):
    if isinstance(uploaded_file, str):
        data = pd.read_csv(uploaded_file)
    else:
        # Assuming uploaded_file is a file-like object
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

# Function to generate a word cloud
def generate_wordcloud(data, title):
    text = ' '.join(data['Title'].dropna().tolist())
    wordcloud = WordCloud(width=800, height=400, background_color='white').generate(text)
    plt.figure(figsize=(10, 5))
    plt.imshow(wordcloud, interpolation='bilinear')
    plt.axis('off')
    plt.title(title, fontsize=18)
    return plt

# Customizing Streamlit's theme
st.set_page_config(page_title="Goodreads Wrapped", layout="wide")

# Main Streamlit app
st.title("Goodreads Wrapped")

# Instructions
st.markdown("""
    **Instructions:**
    1. Export your Goodreads library to a CSV file.
       - Go to 'My Books' on Goodreads.
       - Under 'Tools' on the left, click on 'Import and Export'.
       - Click 'Export Library' to generate your CSV file.
       - Download the CSV file once it's ready.
    2. Upload your CSV file here to see the visualizations.
    3. Explore various insights about your reading habits!
""")

# Sidebar for file upload and year selection
with st.sidebar:
    # Initialize uploaded_file to None
    uploaded_file = None

    # Option for users to select the dataset source
    dataset_source = st.radio(
        "Choose your dataset source",
        ('Upload my dataset', 'Use example dataset')
    )

    if dataset_source == 'Upload my dataset':
        uploaded_file = st.file_uploader("Upload your Goodreads CSV", type="csv")
        if uploaded_file is not None:
            data = load_data(uploaded_file)
    elif dataset_source == 'Use example dataset':
        # Load the dataset from the local example file
        data = load_data(example_csv_file)

    # Check if data is loaded for year selection
    if 'data' in locals():
        min_year = int(data['Date Added'].dt.year.min())
        max_year = int(data['Date Added'].dt.year.max())
        year = st.select_slider("Select Year", options=range(min_year, max_year + 1), value=max_year)

    st.markdown('<a href="https://github.com/gigikenneth/goodreads" target="_blank"><img src="https://cdn.jsdelivr.net/gh/devicons/devicon/icons/github/github-original.svg" width="30" height="30" alt="GitHub"></a>', unsafe_allow_html=True)
    st.sidebar.markdown('Made chaotically at 3am🌪️ by [Gigi](https://github.com/gigikenneth)')

# Visualization code 
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

    # Most Common Authors - Side by side comparison
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Most Common Authors")
        fig5 = plot_common_authors(data)
        st.plotly_chart(fig5)
    with col2:
        st.subheader(f"Most Common Authors in {year}")
        fig6 = plot_common_authors(data, year=year)
        st.plotly_chart(fig6)

    # Book Lengths Plot - Side by side comparison
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Distribution of Book Lengths")
        fig7 = plot_book_lengths(data)
        st.plotly_chart(fig7)
    with col2:
        st.subheader(f"Distribution of Book Lengths in {year}")
        fig8 = plot_book_lengths(data, year=year)
        st.plotly_chart(fig8)

    # Read vs. Unread Books Plot - Side by side comparison
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Read vs. Unread Books")
        fig9 = plot_read_unread_books(data)
        st.plotly_chart(fig9)
    with col2:
        st.subheader(f"Read vs. Unread Books in {year}")
        fig10 = plot_read_unread_books(data, year=year)
        st.plotly_chart(fig10)

    # Word Clouds - Side by side comparison
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("Word Cloud of Book Titles Read")
        read_books = data[data['Read Count'] > 0]
        fig_wc_all = generate_wordcloud(read_books, "All Time")
        st.pyplot(fig_wc_all)
    with col2:
        st.subheader(f"Word Cloud of Book Titles Read in {year}")
        read_books_year = read_books[read_books['Date Read'].dt.year == year]
        fig_wc_year = generate_wordcloud(read_books_year, f"In {year}")
        st.pyplot(fig_wc_year)


