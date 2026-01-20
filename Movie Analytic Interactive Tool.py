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
st.set_page_config(page_title="Movie Analyst", page_icon="🎬", layout="wide")

st.markdown("""
<div style='text-align: center; padding: 20px;'>
    <h1 style='font-family: "Arial Black", sans-serif; font-size: 3.2em; font-weight: 900; color: #FF6B6B; text-shadow: 2px 2px 8px rgba(0,0,0,0.15); letter-spacing: 1px;'>
        🎬 Welcome to Movie Analyst!
    </h1>
    <p style='font-family: "Georgia", serif; font-size: 1.3em; color: #555; font-style: italic; margin-top: -15px; font-weight: 500; letter-spacing: 0.5px;'>
        Because movies are art — but their numbers tell stories too.
    </p>
</div>
""", unsafe_allow_html=True)

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

# Theme selector
theme = st.sidebar.radio("🌓 Choose Theme", options=["🌙 Dark Mode", "☀️ Light Mode"], index=1)

# Apply theme CSS
if theme == "🌙 Dark Mode":
    st.markdown("""
    <style>
    /* Dark Mode Styling */
    :root {
        --background-color: #1a1a1a !important;
        --text-color: #e0e0e0 !important;
        --card-background: #2d2d2d !important;
        --border-color: #404040 !important;
    }
    
    /* Main background */
    .main, body, .stApp {
        background-color: #1a1a1a !important;
        color: #e0e0e0 !important;
    }
    
    /* Text elements */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #e0e0e0 !important;
    }
    
    /* Metrics */
    .stMetric {
        background-color: #2d2d2d !important;
        padding: 15px !important;
        border-radius: 8px !important;
        border: 1px solid #404040 !important;
    }
    
    .stMetric label {
        color: #e0e0e0 !important;
    }
    
    .metric-label, .metric-value {
        color: #e0e0e0 !important;
    }
    
    /* Dataframes */
    .stDataFrame, .stDataFrameContainer {
        background-color: #2d2d2d !important;
    }
    
    [data-testid="stDataFrame"] {
        background-color: #2d2d2d !important;
    }
    
    /* Tabs */
    [data-testid="stTabs"] {
        background-color: #1a1a1a !important;
    }
    
    [role="tablist"] {
        background-color: #1a1a1a !important;
    }
    
    .stTabs [role="tab"] {
        color: #e0e0e0 !important;
        background-color: #2d2d2d !important;
    }
    
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #404040 !important;
        color: #e0e0e0 !important;
    }
    
    /* Input elements */
    .stTextInput input, .stTextInput textarea, .stSelectbox select {
        background-color: #2d2d2d !important;
        color: #e0e0e0 !important;
        border: 1px solid #404040 !important;
    }
    
    /* Slider */
    .stSlider {
        background-color: #1a1a1a !important;
    }
    
    /* Expander */
    .streamlit-expanderContent {
        background-color: #2d2d2d !important;
        color: #e0e0e0 !important;
    }
    
    /* Divider */
    hr {
        border-color: #404040 !important;
    }
    
    /* Info/Warning boxes */
    .stInfo, .stWarning, .stError, .stSuccess {
        background-color: #2d2d2d !important;
        color: #e0e0e0 !important;
        border: 1px solid #404040 !important;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: #252525 !important;
    }
    
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar label {
        color: #e0e0e0 !important;
    }
    
    /* Button */
    button, .stButton button {
        background-color: #404040 !important;
        color: #e0e0e0 !important;
        border: 1px solid #505050 !important;
    }
    
    button:hover, .stButton button:hover {
        background-color: #505050 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)
else:
    st.markdown("""
    <style>
    /* Light Mode Styling */
    :root {
        --background-color: #ffffff !important;
        --text-color: #1a1a1a !important;
        --card-background: #f5f5f5 !important;
        --border-color: #e0e0e0 !important;
    }
    
    /* Main background */
    .main, body, .stApp {
        background-color: #ffffff !important;
        color: #1a1a1a !important;
    }
    
    /* Text elements */
    h1, h2, h3, h4, h5, h6, p, span, div, label {
        color: #1a1a1a !important;
    }
    
    /* Metrics */
    .stMetric {
        background-color: #f5f5f5 !important;
        padding: 15px !important;
        border-radius: 8px !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    .stMetric label {
        color: #1a1a1a !important;
    }
    
    .metric-label, .metric-value {
        color: #1a1a1a !important;
    }
    
    /* Dataframes */
    .stDataFrame, .stDataFrameContainer {
        background-color: #ffffff !important;
    }
    
    [data-testid="stDataFrame"] {
        background-color: #ffffff !important;
    }
    
    /* Tabs */
    [data-testid="stTabs"] {
        background-color: #ffffff !important;
    }
    
    [role="tablist"] {
        background-color: #ffffff !important;
    }
    
    .stTabs [role="tab"] {
        color: #1a1a1a !important;
        background-color: #f0f0f0 !important;
    }
    
    .stTabs [role="tab"][aria-selected="true"] {
        background-color: #e0e0e0 !important;
        color: #1a1a1a !important;
    }
    
    /* Input elements */
    .stTextInput input, .stTextInput textarea, .stSelectbox select {
        background-color: #f5f5f5 !important;
        color: #1a1a1a !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* Slider */
    .stSlider {
        background-color: #ffffff !important;
    }
    
    /* Expander */
    .streamlit-expanderContent {
        background-color: #f5f5f5 !important;
        color: #1a1a1a !important;
    }
    
    /* Divider */
    hr {
        border-color: #e0e0e0 !important;
    }
    
    /* Info/Warning boxes */
    .stInfo, .stWarning, .stError, .stSuccess {
        background-color: #f0f0f0 !important;
        color: #1a1a1a !important;
        border: 1px solid #e0e0e0 !important;
    }
    
    /* Sidebar */
    .stSidebar {
        background-color: #f9f9f9 !important;
    }
    
    .stSidebar h1, .stSidebar h2, .stSidebar h3, .stSidebar p, .stSidebar label {
        color: #1a1a1a !important;
    }
    
    /* Button */
    button, .stButton button {
        background-color: #e0e0e0 !important;
        color: #1a1a1a !important;
        border: 1px solid #c0c0c0 !important;
    }
    
    button:hover, .stButton button:hover {
        background-color: #d0d0d0 !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

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

# search by actor name
search_actor = st.sidebar.text_input("🎭 Search by Lead Actor (partial match)", placeholder="e.g., Tom Hanks")

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

# apply actor search filter (check for common actor column names)
if search_actor:
    actor_columns = [col for col in filtered_df.columns if 'actor' in col.lower() or 'star' in col.lower()]
    if actor_columns:
        # Search across all actor-related columns
        actor_mask = pd.Series([False] * len(filtered_df), index=filtered_df.index)
        for col in actor_columns:
            actor_mask |= filtered_df[col].astype(str).str.contains(search_actor, case=False, na=False)
        filtered_df = filtered_df[actor_mask]
    else:
        st.sidebar.warning("No actor/star column found in dataset")
st.write(f"### Displaying {len(filtered_df)} movies")

# Display key metrics
col1, col2, col3 = st.columns(3)
with col1:
    st.metric("🎥 Total Movies", len(filtered_df))
with col2:
    genre_count = filtered_df['Genre'].nunique() if 'Genre' in filtered_df.columns else 0
    st.metric("🎭 Genres", genre_count)
with col3:
    if 'Gross' in filtered_df.columns and len(filtered_df) > 0:
        highest_gross_idx = filtered_df['Gross'].idxmax()
        highest_movie = filtered_df.loc[highest_gross_idx, 'Series_Title']
        st.metric("🏆 Highest Grossing Film", highest_movie)
    else:
        st.metric("🏆 Highest Grossing Film", "N/A")

st.divider()

# Create tabs for different views
tab1, tab2, tab3, tab4 = st.tabs(["📊 Movie Data", "🎬 Movie Details", "⭐ By Rating", "📈 Analytics"])

with tab1:
    st.subheader("📊 All Movies")
    # Display filtered data
    display_cols = [c for c in ('Series_Title', 'Genre', 'Released_Year', 'IMDB_Rating', 'Gross') if c in filtered_df.columns]
    if display_cols:
        st.dataframe(filtered_df[display_cols], use_container_width=True, height=400)
    else:
        st.info("No displayable columns found in the filtered data.")

with tab2:
    st.subheader("🎬 Movie Details & Summaries")
    if len(filtered_df) > 0:
        # Select a movie to view details with better styling
        col_left, col_right = st.columns([3, 1])
        
        with col_left:
            st.markdown("### 📽️ Choose a Movie")
        
        movie_titles = filtered_df['Series_Title'].tolist()
        selected_movie = st.selectbox("Select a Movie to View Details", options=movie_titles, key="movie_selector", label_visibility="collapsed")
        
        # Get the selected movie data
        movie_data = filtered_df[filtered_df['Series_Title'] == selected_movie].iloc[0]
        
        # Display movie summary in a formatted card-like structure
        st.markdown("---")
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown(f"## 🎬 {movie_data['Series_Title']}")
            st.markdown(f"**🎭 Genre:** `{movie_data['Genre']}`")
            st.markdown(f"**📅 Release Year:** `{int(movie_data['Released_Year'])}`")
        
        with col2:
            st.markdown(f"<div style='text-align: center; padding: 20px; background-color: #f0f2f6; border-radius: 10px;'>", unsafe_allow_html=True)
            st.markdown(f"### ⭐ {movie_data['IMDB_Rating']}/10")
            st.markdown(f"### 💰 ${movie_data['Gross']:,.0f}")
            st.markdown("</div>", unsafe_allow_html=True)
        
        # Additional movie statistics
        st.markdown("---")
        st.subheader("📊 Movie Summary")
        
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.metric("⭐ IMDB Rating", f"{movie_data['IMDB_Rating']:.1f}/10")
        with col2:
            st.metric("📅 Year", int(movie_data['Released_Year']))
        with col3:
            st.metric("🎬 Genre", movie_data['Genre'])
        
        # Revenue and votes information
        col1, col2 = st.columns(2)
        
        with col1:
            st.metric("💵 Box Office Gross", f"${movie_data['Gross']:,.0f}")
        with col2:
            st.metric("🗳️ Number of Votes", f"{int(movie_data['No_of_Votes']):,}" if 'No_of_Votes' in movie_data else "N/A")
        
        st.markdown("---")
        st.markdown("**Quick Summary**")
        st.info(f"'{selected_movie}' is a {movie_data['Genre']} film released in {int(movie_data['Released_Year'])} with an IMDB rating of {movie_data['IMDB_Rating']}/10. The film earned ${movie_data['Gross']:,.0f} at the box office.")
        
    else:
        st.warning("No movies to display. Adjust your filters to see movie details.")

with tab3:
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
                with st.expander(f"{category} - {len(category_df)} movies"):
                    display_cols_stars = [c for c in ('Series_Title', 'Genre', 'Released_Year', 'IMDB_Rating', 'Gross') if c in category_df.columns]
                    if display_cols_stars:
                        st.dataframe(category_df[display_cols_stars], use_container_width=True, hide_index=True)
    else:
        st.info("IMDB_Rating column not found in the dataset.")

with tab4:
    st.subheader("📈 Analytics & Visualizations")
    
    # Visualizations
    viz_col1, viz_col2 = st.columns(2)
    
    with viz_col1:
        st.markdown("#### Top 10 Genres by Movie Count")
        if 'Genre' in df.columns:
            df_genre = df['Genre'].dropna().str.split('|').explode()
            genre_counts = df_genre.value_counts().head(10)
            st.bar_chart(genre_counts)
        else:
            st.info("No genre data available to compute top genres.")
    
    with viz_col2:
        st.markdown("#### Top 10 Movies by Revenue")
        if 'Gross' in filtered_df.columns and 'Series_Title' in filtered_df.columns:
            top_movies = filtered_df[['Series_Title', 'Gross', 'IMDB_Rating']].sort_values(by='Gross', ascending=False).head(10)
            st.dataframe(top_movies, use_container_width=True, hide_index=True)
        else:
            st.info("'Series_Title' or 'Gross' column missing; cannot show top movies by revenue.")
    
    st.divider()
    
    # scatter plot for rating vs revenue
    st.markdown("#### Rating vs Revenue Scatter Plot")
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

    # Correlation heatmap
    st.markdown("#### Correlation Heatmap")
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

