Project: Ingredients Data Visual Exploration

Overview
- Interactive exploratory data analysis of `ingredients.csv` using Plotly. 

Requirements
- A python environment with installed dependencies (listed in `ingredients.csv`). 

Startup 
-  With environment activated, run  
```bash
python3 app.py
```
and follow the instruction there. It should output something like 
```bash 
Starting Dash app at http://127.0.0.1:8050/
```
so use the link to navigate to the interactive tool for data visualization.

Notes
- The CSV is semicolon-delimited; use `pd.read_csv('ingredients.csv', sep=';')`.
- Some numeric fields contain missing/empty values; the notebook includes cleaning steps.

