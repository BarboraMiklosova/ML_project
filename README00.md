Project: Ingredients Data Visual Exploration

Overview
- Interactive exploratory data analysis of `ingredients.csv` using Plotly.

Setup
1. Create and activate a Python environment (recommended):

```bash
python -m venv .venv
source .venv/bin/activate
```

2. Install dependencies:

```bash
pip install -r requirements.txt
```

Quick start
- Launch JupyterLab or Notebook in the project folder and open `data_viz.ipynb` (created notebook contains example plots):

```bash
jupyter lab
# or
jupyter notebook
```

Files
- `ingredients.csv` - dataset (semicolon-delimited).
- `requirements.txt` - Python dependencies. Install with !pip install -r requirements.txt
- `data_viz.ipynb` - notebook with data cleaning and interactive Plotly visualizations.

Notes
- The CSV is semicolon-delimited; use `pd.read_csv('ingredients.csv', sep=';')`.
- Some numeric fields contain missing/empty values; the notebook includes cleaning steps.

Next steps
- Run the notebook, inspect visuals, and tell me any plots or filters you'd like added.
