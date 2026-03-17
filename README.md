# Food Ingredients Interactive Data Visualization

## Team Members
Barbora Hudačková, Barbora Miklošová

## Overview
This project provides an interactive exploratory data analysis of food ingredients data using a Plotly Dash web application. The app allows users to visualize and explore nutritional data from `ingredients.csv` through linked interactive charts including scatter plots, histograms, box plots, and correlation heatmaps.

## Features
- **Interactive Scatter Plot**: Protein vs Fat content, colored by energy (kcal)
- **Histogram**: Energy distribution with filtering
- **Box Plot**: Protein distribution by food categories
- **Correlation Heatmap**: Relationships between major nutrients
- **Cross-filtering**: Select points in one chart to filter others
- **Dynamic Filters**: Adjust protein and energy ranges, filter by category


## Prerequisites
- Python 3.x
- A virtual environment with all packages from `requirements.txt` installed
=======
## Requirements
- Python 3.7+
- Dependencies listed in `requirements.txt` (install with `pip install -r requirements.txt`)

## Setup
1. **Create a virtual environment** (recommended):
   ```bash
   python -m venv .venv
   ```

2. **Activate the environment**:
   - On Windows:
     ```bash
     .venv\Scripts\activate
     ```
   - On macOS/Linux:
     ```bash
     source .venv/bin/activate
     ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
>>>>>>> 711c908eaf681e7424f649ac1b29433943697b28

## Running the Application
1. Ensure the virtual environment is activated
2. Run the Dash app:
   ```bash
   python app.py
   ```

3. The app will start and display output similar to:
   ```
   Starting Dash app at http://127.0.0.1:8050/
   Press Ctrl+C to quit
   ```

4. Open your web browser and navigate to `http://127.0.0.1:8050/`

## How to Use the App
- **Filters**: Use the sliders to set ranges for protein and energy content. Select a food category from the dropdown.
- **Interactive Charts**:
  - Click and drag on the scatter plot to select points
  - Selected points will highlight in blue and filter the other charts
  - Hover over points for detailed information
- **Info Box**: Shows total, filtered, and selected food counts
- **Charts Update**: All charts update in real-time based on your selections and filters

## Data
- **Source**: `ingredients.csv` (semicolon-delimited)
- **Cleaning**: The app automatically removes negative values and extreme outliers (above 99th percentile) for nutritional columns
- **Categorization**: Foods are automatically categorized based on description keywords

## Files
- `app.py` - Main Dash application
- `ingredients.csv` - Dataset
- `requirements.txt` - Python dependencies
<<<<<<< HEAD
=======
- `data_viz.ipynb` - Jupyter notebook with additional visualizations
- `univariate_analysis.ipynb` - Univariate analysis notebook
>>>>>>> 711c908eaf681e7424f649ac1b29433943697b28

## Notes
- The CSV uses semicolons as delimiters: `pd.read_csv('ingredients.csv', sep=';')`
- Some fields may contain missing values; the app handles data cleaning automatically
<<<<<<< HEAD

=======
- For development, run with `python app.py` in debug mode (included by default)
>>>>>>> 711c908eaf681e7424f649ac1b29433943697b28
