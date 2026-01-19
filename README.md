# 🎬 Movie Analytics Interactive Dashboard

A powerful and interactive Streamlit-based dashboard for analyzing and visualizing movie data with advanced filtering, real-time statistics, and comprehensive visualizations.

---

## ✨ Features

### 🎯 **Interactive Filtering System**
- **Genre Selection**: Filter movies by specific genres
- **Year Range Slider**: Select movies from custom time periods (📅)
- **Title Search**: Find movies by partial title matching (🔍)
- **Combined Filters**: All filters work together for precise queries

### 📊 **Real-Time Metrics Dashboard**
- 🎥 **Total Movies**: Dynamic count of filtered movies
- ⭐ **Average Rating**: Real-time IMDB rating calculation
- 💰 **Total Gross Revenue**: Combined box office earnings
- 🎭 **Genre Diversity**: Unique genre count

### ⭐ **Star Rating Categorization**
Automatic segmentation of movies into 5 rating tiers:

| Category | Rating Range | Icon | Count Metric |
|----------|--------------|------|--------------|
| **Masterpiece** | 9.0-10.0 | 🏆 | Highest rated |
| **Excellent** | 8.0-8.9 | ✨ | Highly acclaimed |
| **Great** | 7.0-7.9 | 👍 | Well-received |
| **Good** | 6.0-6.9 | 👌 | Decent quality |
| **Average** | 0-5.9 | 📽️ | Lower rated |

Each category includes:
- Movie count metrics with emoji indicators
- Sortable data tables (sorted by rating)
- Detailed movie information (title, genre, year, rating, revenue)

### 📈 **Data Visualizations**
1. **Top 10 Genres Bar Chart**: Visual ranking of most common genres
2. **Rating vs Revenue Scatter Plot**: 
   - Shows correlation between ratings and box office performance
   - Color-coded by genre for easy comparison
3. **Correlation Heatmap**: 
   - Displays relationships between numeric features
   - Color-coded correlation strength (coolwarm palette)

### 🏆 **Top Performers**
- Table of highest-grossing movies in filtered results
- Displays top 10 movies by revenue
- Includes revenue and rating for quick analysis

---

## 🚀 Quick Start

### Prerequisites
- **Python**: 3.8 or higher
- **pip**: Python package manager

### Installation

**Step 1: Clone Repository**
```bash
git clone https://github.com/Tronnnnnnnnnn/Movie-Analytic-Interactive-tool.git
cd Movie-Analytic-Interactive-tool
```

**Step 2: Create Virtual Environment (Recommended)**

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

macOS/Linux:
```bash
python -m venv venv
source venv/bin/activate
```

**Step 3: Install Dependencies**
```bash
pip install -r requirements.txt
```

### Running the Application

```bash
streamlit run "Movie Analytic Interactive Tool.py"
```

The app automatically opens at `http://localhost:8501` in your default browser.

---

## 📊 Dataset Structure

**File**: `movies.csv` (Required - place in same directory as Python file)

### Columns Reference

| Column | Type | Range | Description |
|--------|------|-------|-------------|
| `Series_Title` | String | N/A | Movie title |
| `Genre` | String | Primary only | Main genre classification |
| `Released_Year` | Integer | 1900-2024 | Release year |
| `IMDB_Rating` | Float | 0.0-10.0 | IMDB user rating |
| `Gross` | Float | Varies | Box office revenue (USD) |
| `No_of_Votes` | Integer | N/A | Number of IMDB votes |

### Data Preparation
- CSV must have headers matching column names above
- Numeric columns (Year, Rating, Gross) are automatically cleaned
- Rows with missing critical data are filtered out
- Comma-separated values in Gross column are handled automatically

---

## 📦 Dependencies

All dependencies are automatically installed via `requirements.txt`:

```
pandas          # Data manipulation and analysis
streamlit       # Web app framework
matplotlib      # Plotting library
seaborn         # Statistical visualization
numpy           # Numerical computing
```

### Optional: VS Code Setup
- Linter warnings for imports can be suppressed with `.vscode/settings.json`
- Settings are pre-configured in the repository

---

## 🏗️ Project Structure

```
Movie-Analytic-Interactive-tool/
│
├── 📄 Movie Analytic Interactive Tool.py    # Main application (245 lines)
├── 📊 movies.csv                            # Dataset (required)
├── 📋 requirements.txt                      # Dependencies
├── 📖 README.md                             # Documentation (this file)
├── 🚫 .gitignore                            # Git ignore rules
│
└── 📁 .vscode/                              # VS Code configuration
    └── settings.json                        # Pylance settings
```

---

## 🔧 Technical Architecture

### Core Functionality

**Data Loading**
- Automatic absolute path resolution for CSV file
- Graceful error handling with user-friendly messages
- Streamlit caching for performance optimization

**Data Processing**
```python
# Automatic column mapping
Series_Title → title
Genre → genre  
Released_Year → year
IMDB_Rating → rating
Gross → revenue
```

**Filtering Pipeline**
1. Genre filter (optional)
2. Year range filter (dual slider)
3. Title search filter (partial match, case-insensitive)
4. Category assignment (star ratings)

**Visualization Pipeline**
- Protected matplotlib/seaborn imports with fallback
- Exception handling for rendering failures
- Responsive design across screen sizes

### Error Handling

| Scenario | Handling | User Message |
|----------|----------|--------------|
| Missing CSV | Early exit with error | File location notice |
| Invalid data type | Safe coercion with NaN handling | Graceful fallback |
| Matplotlib unavailable | Fallback mode | Installation suggestion |
| Empty filters | Show 0 records | Informative message |

### Performance Optimizations
- ✅ `@st.cache_data` for efficient data loading
- ✅ Year bounds computed once, reused in slider
- ✅ Single boolean mask for multi-condition filtering
- ✅ Vectorized pandas operations
- ✅ Wide layout for better utilization

---

## 💡 Usage Guide

### Scenario 1: Discover Masterpiece Films
1. Open the app → Sidebar appears on left
2. Leave **Genre** as "All"
3. Leave **Year Range** as default
4. Scroll to **⭐ Masterpiece** section
5. View highest-rated movies

### Scenario 2: Analyze Recent Action Movies
1. Select **Genre**: "Action"
2. Adjust **Year Range**: 2020-2024
3. View metrics for recent action films
4. Check **Rating vs Revenue** chart
5. Identify top performers

### Scenario 3: Search Specific Movie
1. Type in **Title Search**: "Inception" (or partial: "Ince")
2. View filtered results
3. Check which rating category it belongs to
4. Compare with similar-rated films

### Scenario 4: Statistical Analysis
1. Apply desired filters
2. Scroll to **Correlation Heatmap**
3. Analyze relationships between rating, revenue, votes
4. Look for meaningful patterns

---

## 🌐 Deployment Options

### Option 1: Streamlit Cloud (Recommended - Free)

1. **Push to GitHub** (already done ✅)
2. **Visit** [share.streamlit.io](https://share.streamlit.io)
3. **Sign in** with GitHub
4. **Click** "New app"
5. **Select**:
   - Repository: `Movie-Analytic-Interactive-tool`
   - Branch: `main`
   - File: `Movie Analytic Interactive Tool.py`
6. **Click** "Deploy"
7. **Wait** 2-3 minutes for deployment
8. **Access** via unique Streamlit Cloud URL

### Option 2: Local Deployment

**Run locally with custom settings:**
```bash
streamlit run "Movie Analytic Interactive Tool.py" \
  --server.port 8501 \
  --server.address localhost
```

**Access**: `http://localhost:8501`

### Option 3: Docker Containerization

(Optional for advanced users)
- Create Dockerfile with Python base image
- Install dependencies from requirements.txt
- Expose port 8501

---

## 📝 Code Highlights

### Key Functions

**`load_data()`** - Smart data loading
```
• Absolute path resolution
• Try/except error handling  
• Automatic type conversion
• Missing value handling
```

**`categorize_stars()`** - Rating classification
```
• 5-tier categorization system
• Semantic emoji labels
• Range-based bucketing
```

**Filtering System** - Multi-condition filtering
```
• Genre selection
• Year range (dual slider)
• Title partial match
• Combined filter application
```

---

## 🐛 Troubleshooting

| Problem | Solution |
|---------|----------|
| ❌ `movies.csv not found` | Place CSV file in same directory as `.py` file |
| ❌ Module import errors | Run `pip install -r requirements.txt` in correct environment |
| ❌ No data displays | Check CSV column names match documentation |
| ❌ Plots don't render | Ensure matplotlib & seaborn installed; check requirements.txt |
| ❌ Slow performance | Delete `.streamlit/` cache folder, refresh app |
| ❌ Year slider missing | Verify `Released_Year` column in CSV |

---

## 📊 Example Metrics

With complete IMDB dataset (~1000 movies):
- **Average Rating**: ~7.2/10
- **Total Gross**: $50B+ USD
- **Genres**: 20+ unique types
- **Year Range**: 1900-2024

---

## 📄 License

MIT License - Free for personal and commercial use

---

## 👨‍💻 Author

**Harsha Anand Raj P**

---

## 🤝 Contributing

Contributions welcome! Options:
- 🐛 Report bugs via Issues
- 💡 Suggest features
- 🔄 Submit pull requests
- 📝 Improve documentation

---

## 📧 Contact & Support

- **GitHub**: [Tronnnnnnnnnn](https://github.com/Tronnnnnnnnnn)
- **Issues**: [Open an issue](https://github.com/Tronnnnnnnnnn/Movie-Analytic-Interactive-tool/issues)

---

## 🎉 Status

| Aspect | Status |
|--------|--------|
| Build | ✅ Passing |
| Tests | ✅ Verified |
| Deployment | ✅ Ready |
| Documentation | ✅ Complete |
| Version | 1.1.0 |
| Last Updated | January 2026 |

**Made with ❤️ for movie enthusiasts and data analysts**
