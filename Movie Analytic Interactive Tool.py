#=========================================
# Movie Analytics Interactive Dashboard
#=========================================

# Import necessary libraries
import pandas as pd
import streamlit as st  # type: ignore
import os

# matplotlib/seaborn may not be available to linters; guard imports
try:
    import matplotlib.pyplot as plt  # type: ignore
    import seaborn as sns  # type: ignore
    plotting_available = True
except Exception:
    plt = None
    sns = None
    plotting_available = False

if plotting_available:
    sns.set(style="whitegrid")

# Custom page config for better UI
st.set_page_config(page_title="Movie Analytics", page_icon="🎬", layout="wide")

st.title("🎬 Movie Analytics Interactive Dashboard")

# Load dataset
@st.cache_data
def load_data():
    # use absolute path so streamlit can find the file regardless of where it's invoked from
    script_dir = os.path.dirname(os.path.abspath(__file__))
    csv_path = os.path.join(script_dir, 'movies.csv')
    try:
        df = pd.read_csv(csv_path)
    except FileNotFoundError:
        st.error(f"movies.csv not found at {csv_path}. Please ensure it's in the same directory as this app.")
        return pd.DataFrame()
    except Exception as e:
        st.error(f"Failed to load data: {e}")
        return pd.DataFrame()

    # clean data when possible
    # map expected columns to actual CSV columns
    column_mapping = {
        'title': 'Series_Title',
        'genre': 'Genre',
        'rating': 'IMDB_Rating',
        'Revenue': 'Gross',
        'year': 'Released_Year'
    }
    
    # coerce numeric columns safely
    for col in ('IMDB_Rating', 'Released_Year', 'Gross', 'No_of_Votes'):
        if col in df.columns:
            try:
                # for Gross, remove commas first
                if col == 'Gross':
                    df[col] = df[col].astype(str).str.replace(',', '', regex=False)
                df[col] = pd.to_numeric(df[col], errors='coerce')
            except Exception:
                pass

    required = [c for c in ('Series_Title', 'Genre', 'IMDB_Rating', 'Gross') if c in df.columns]
    if required:
        df = df.dropna(subset=required)

    return df


df = load_data()

# stop early if data couldn't be loaded
if df.empty:
    st.stop()

# streamlit sidebar for user inputs
st.sidebar.header("🎯 Filter Movies")
selected_genre = st.sidebar.selectbox("🎭 Select Genre", options=['All'] + list(df['Genre'].unique()) if 'Genre' in df.columns else ['All'])

# compute year bounds once and reuse
if 'Released_Year' in df.columns:
    year_vals = df['Released_Year'].dropna()
    year_min = int(year_vals.min()) if not year_vals.empty else None
    year_max = int(year_vals.max()) if not year_vals.empty else None
    selected_year = st.sidebar.slider("📅 Select Year Range", year_min, year_max, (year_min, year_max))
else:
    selected_year = (None, None)

# search by title
search_title = st.sidebar.text_input("🔍 Search by Title (partial match)", placeholder="e.g., Godfather")

# Filter data based on user input
if selected_genre == 'All':
    filtered_df = df.copy()
else:
    filtered_df = df[df['Genre'] == selected_genre]

if selected_year and selected_year[0] is not None:
    filtered_df = filtered_df[(filtered_df['Released_Year'] >= selected_year[0]) & (filtered_df['Released_Year'] <= selected_year[1])]

# apply title search filter
if search_title and 'Series_Title' in filtered_df.columns:
    filtered_df = filtered_df[filtered_df['Series_Title'].str.contains(search_title, case=False, na=False)]
st.write(f"### Displaying {len(filtered_df)} movies")

# Display key metrics
col1, col2, col3, col4 = st.columns(4)
with col1:
    st.metric("🎥 Total Movies", len(filtered_df))
with col2:
    avg_rating = filtered_df['IMDB_Rating'].mean() if 'IMDB_Rating' in filtered_df.columns else 0
    st.metric("⭐ Avg Rating", f"{avg_rating:.2f}" if avg_rating > 0 else "N/A")
with col3:
    total_gross = filtered_df['Gross'].sum() if 'Gross' in filtered_df.columns else 0
    st.metric("💰 Total Gross", f"${total_gross:,.0f}" if total_gross > 0 else "N/A")
with col4:
    genre_count = filtered_df['Genre'].nunique() if 'Genre' in filtered_df.columns else 0
    st.metric("🎭 Genres", genre_count)

st.divider()

# Display filtered data
st.subheader(f"📊 Filtered Movie Data ({len(filtered_df)} records)")
display_cols = [c for c in ('Series_Title', 'Genre', 'Released_Year', 'IMDB_Rating', 'Gross') if c in filtered_df.columns]
if display_cols:
    st.dataframe(filtered_df[display_cols], use_container_width=True, height=300)
else:
    st.info("No displayable columns found in the filtered data.")

st.divider()

# Movies segmented by Star Rating
st.subheader("⭐ Movies Segmented by Star Rating")
if 'IMDB_Rating' in filtered_df.columns:
    # Define star categories
    def categorize_stars(rating):
        if rating >= 9:
            return "⭐⭐⭐⭐⭐ Masterpiece (9.0-10.0)"
        elif rating >= 8:
            return "⭐⭐⭐⭐ Excellent (8.0-8.9)"
        elif rating >= 7:
            return "⭐⭐⭐ Great (7.0-7.9)"
        elif rating >= 6:
            return "⭐⭐ Good (6.0-6.9)"
        else:
            return "⭐ Average (0-5.9)"
    
    filtered_df['Star_Category'] = filtered_df['IMDB_Rating'].apply(categorize_stars)
    
    # Display star category statistics
    star_stats = filtered_df['Star_Category'].value_counts().sort_index(ascending=False)
    col1, col2, col3, col4, col5 = st.columns(5)
    
    categories = ["⭐⭐⭐⭐⭐ Masterpiece (9.0-10.0)", "⭐⭐⭐⭐ Excellent (8.0-8.9)", 
                  "⭐⭐⭐ Great (7.0-7.9)", "⭐⭐ Good (6.0-6.9)", "⭐ Average (0-5.9)"]
    
    with col1:
        count = (filtered_df['Star_Category'] == categories[0]).sum()
        st.metric("🏆 Masterpiece", count)
    with col2:
        count = (filtered_df['Star_Category'] == categories[1]).sum()
        st.metric("✨ Excellent", count)
    with col3:
        count = (filtered_df['Star_Category'] == categories[2]).sum()
        st.metric("👍 Great", count)
    with col4:
        count = (filtered_df['Star_Category'] == categories[3]).sum()
        st.metric("👌 Good", count)
    with col5:
        count = (filtered_df['Star_Category'] == categories[4]).sum()
        st.metric("📽️ Average", count)
    
    st.divider()
    
    # Display movies for each star category
    for category in ["⭐⭐⭐⭐⭐ Masterpiece (9.0-10.0)", "⭐⭐⭐⭐ Excellent (8.0-8.9)", 
                     "⭐⭐⭐ Great (7.0-7.9)", "⭐⭐ Good (6.0-6.9)", "⭐ Average (0-5.9)"]:
        category_df = filtered_df[filtered_df['Star_Category'] == category].sort_values('IMDB_Rating', ascending=False)
        
        if len(category_df) > 0:
            st.write(f"**{category}** - {len(category_df)} movies")
            display_cols_stars = [c for c in ('Series_Title', 'Genre', 'Released_Year', 'IMDB_Rating', 'Gross') if c in category_df.columns]
            if display_cols_stars:
                st.dataframe(category_df[display_cols_stars], use_container_width=True, height=150, hide_index=True)
            st.write("")
else:
    st.info("IMDB_Rating column not found in the dataset.")

# Visualizations
st.subheader("Top 10 Genres by Movie Count")
if 'Genre' in df.columns:
    df_genre = df['Genre'].dropna().str.split('|').explode()
    genre_counts = df_genre.value_counts().head(10)
    st.bar_chart(genre_counts)
else:
    st.info("No genre data available to compute top genres.")

# scatter plot for rating vs revenue
st.subheader("Rating vs Revenue Scatter")
if plotting_available and {'IMDB_Rating', 'Gross'}.issubset(filtered_df.columns):
    try:
        fig, ax = plt.subplots(figsize=(10, 6))
        hue = 'Genre' if 'Genre' in filtered_df.columns else None
        sns.scatterplot(data=filtered_df, x='IMDB_Rating', y='Gross', hue=hue, palette='tab10', ax=ax, s=100)
        ax.set_xlabel("IMDB Rating", fontsize=12, fontweight='bold')
        ax.set_ylabel("Gross Revenue", fontsize=12, fontweight='bold')
        ax.set_title("Rating vs Revenue", fontsize=14, fontweight='bold')
        st.pyplot(fig, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to render scatter plot: {e}")
else:
    st.info("Scatter plot requires numeric 'IMDB_Rating' and 'Gross' columns and matplotlib/seaborn installed.")

st.divider()

#Correlation heatmap
st.subheader("Correlation Heatmap")
if plotting_available:
    try:
        numeric = filtered_df.select_dtypes(include=['number'])
        corr = numeric.corr()
        if corr.shape[0] < 2:
            st.info("Not enough numeric data to compute correlations.")
        else:
            fig2, ax = plt.subplots(figsize=(8, 6))
            sns.heatmap(corr, annot=True, cmap='coolwarm', ax=ax, cbar_kws={'label': 'Correlation'})
            ax.set_title("Feature Correlations", fontsize=14, fontweight='bold')
            st.pyplot(fig2, use_container_width=True)
    except Exception as e:
        st.error(f"Failed to render heatmap: {e}")
else:
    st.warning("matplotlib/seaborn not available. Install with: pip install matplotlib seaborn")

st.divider()

# top 10 movies by revenue
st.subheader("🏆 Top 10 Movies by Revenue")
if 'Gross' in filtered_df.columns and 'Series_Title' in filtered_df.columns:
    top_movies = filtered_df[['Series_Title', 'Gross', 'IMDB_Rating']].sort_values(by='Gross', ascending=False).head(10)
    st.dataframe(top_movies, use_container_width=True, hide_index=True)
else:
    st.info("'Series_Title' or 'Gross' column missing; cannot show top movies by revenue.")

