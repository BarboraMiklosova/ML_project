"""
Interactive Plotly Dash App for Ingredients Data Visualization
Features:
- Linked scatter plot, histogram, and box plot
- Cross-filtering: select points in one chart to filter others
- Interactive filters for nutrient ranges and categories
"""

import pandas as pd
import numpy as np
from dash import Dash, dcc, html, callback, Input, Output
import plotly.express as px
import plotly.graph_objects as go

# ============================================================================
# DATA LOADING & CLEANING
# ============================================================================

def load_and_clean_data():
    """Load and clean ingredients dataset"""
    df = pd.read_csv('ingredients.csv', sep=';', skiprows=1)
    
    # Columns to clean
    cols_to_clean = ['Energy_kcal', 'Protein_g', 'Fat_g', 'Carb_g', 'Sugar_g', 'Sodium_mg']
    df_clean = df.copy()
    
    # Remove negative values and extreme outliers (above 99th percentile)
    for col in cols_to_clean:
        upper_limit = df[col].quantile(0.99)
        df_clean = df_clean[(df_clean[col] >= 0) & (df_clean[col] <= upper_limit)]
    
    return df_clean

def categorize_food(desc):
    """Simple categorization logic based on keywords"""
    desc = str(desc).lower()
    if 'meat' in desc or 'pork' in desc or 'beef' in desc or 'lamb' in desc: 
        return 'Meat'
    if 'veg' in desc or 'fruit' in desc or 'leaf' in desc: 
        return 'Veg/Fruit'
    if 'cereal' in desc or 'bread' in desc or 'flour' in desc: 
        return 'Grains'
    if 'soup' in desc: 
        return 'Soups'
    if 'fish' in desc or 'mackerel' in desc or 'seafood' in desc: 
        return 'Seafood'
    if 'oil' in desc or 'butter' in desc: 
        return 'Fats/Oils'
    if 'cookie' in desc or 'candy' in desc or 'chocolate' in desc: 
        return 'Sweets'
    return 'Other'

# Load data
df = load_and_clean_data()
df['Category'] = df['Descrip'].apply(categorize_food)

# ============================================================================
# DASH APP
# ============================================================================

app = Dash(__name__)

app.layout = html.Div([
    html.H1("Interactive Ingredients Visualization Dashboard", 
            style={'textAlign': 'center', 'marginBottom': 30}),
    
    # Info box
    html.Div(id='info-box', style={
        'textAlign': 'center',
        'fontSize': 14,
        'marginBottom': 20,
        'padding': 10,
        'backgroundColor': '#f0f0f0',
        'borderRadius': 5
    }),
    
    # Filters Section
    html.Div([
        html.H3("Filters", style={'marginBottom': 20}),
        html.Div([
            html.Div([
                html.Label("Protein Range (g):", style={'fontWeight': 'bold'}),
                dcc.RangeSlider(
                    id='protein-slider',
                    min=int(df['Protein_g'].min()),
                    max=int(df['Protein_g'].max()),
                    value=[0, int(df['Protein_g'].max())],
                    marks={
                        0: '0g',
                        int(df['Protein_g'].max()): f"{int(df['Protein_g'].max())}g"
                    },
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], style={'flex': '1', 'marginRight': 20}),
            
            html.Div([
                html.Label("Energy Range (kcal):", style={'fontWeight': 'bold'}),
                dcc.RangeSlider(
                    id='energy-slider',
                    min=int(df['Energy_kcal'].min()),
                    max=int(df['Energy_kcal'].max()),
                    value=[0, int(df['Energy_kcal'].max())],
                    marks={
                        0: '0',
                        int(df['Energy_kcal'].max()): f"{int(df['Energy_kcal'].max())}"
                    },
                    tooltip={"placement": "bottom", "always_visible": True}
                ),
            ], style={'flex': '1', 'marginRight': 20}),
            
            html.Div([
                html.Label("Category:", style={'fontWeight': 'bold'}),
                dcc.Dropdown(
                    id='category-dropdown',
                    options=[{'label': 'All', 'value': 'all'}] + 
                           [{'label': cat, 'value': cat} for cat in sorted(df['Category'].unique())],
                    value='all',
                    multi=False
                ),
            ], style={'flex': '1'}),
        ], style={'display': 'flex', 'gap': 20})
    ], style={
        'padding': 20,
        'backgroundColor': '#f9f9f9',
        'borderRadius': 5,
        'marginBottom': 30
    }),
    
    # Main Charts
    html.Div([
        # Top row: Scatter plot spans full width
        html.Div([
            dcc.Graph(id='scatter-plot')
        ], style={'marginBottom': 30}),
        
        # Middle row: Histogram and Box plot side by side
        html.Div([
            html.Div([
                dcc.Graph(id='histogram-energy')
            ], style={'flex': '1', 'marginRight': 10}),
            
            html.Div([
                dcc.Graph(id='boxplot-category')
            ], style={'flex': '1', 'marginLeft': 10}),
        ], style={'display': 'flex', 'gap': 20, 'marginBottom': 30}),
        
        # Bottom row: Correlation heatmap
        html.Div([
            dcc.Graph(id='correlation-heatmap')
        ]),
    ]),
    
    # Store for selected point indices
    dcc.Store(id='selected-points-store', data=[]),
])

# ============================================================================
# CALLBACKS FOR INTERACTIVITY
# ============================================================================

@callback(
    [Output('scatter-plot', 'figure'),
     Output('histogram-energy', 'figure'),
     Output('boxplot-category', 'figure'),
     Output('correlation-heatmap', 'figure'),
     Output('info-box', 'children')],
    [Input('protein-slider', 'value'),
     Input('energy-slider', 'value'),
     Input('category-dropdown', 'value'),
     Input('scatter-plot', 'selectedData')],
)
def update_all_charts(protein_range, energy_range, selected_category, selected_data):
    """Update all charts based on filters and selections"""
    
    # Apply range filters
    df_filtered = df[
        (df['Protein_g'] >= protein_range[0]) &
        (df['Protein_g'] <= protein_range[1]) &
        (df['Energy_kcal'] >= energy_range[0]) &
        (df['Energy_kcal'] <= energy_range[1])
    ].copy()
    
    # Apply category filter
    if selected_category != 'all':
        df_filtered = df_filtered[df_filtered['Category'] == selected_category]
    
    # Apply selection from scatter plot
    if selected_data and selected_data.get('points'):
        selected_indices = [point['customdata'] for point in selected_data.get('points', [])]
        df_selected = df_filtered[df_filtered.index.isin(selected_indices)]
    else:
        df_selected = df_filtered.copy()
    
    # Info message
    total_foods = len(df)
    filtered_foods = len(df_filtered)
    selected_foods = len(df_selected)
    info_text = f"Total foods: {total_foods} | Filtered: {filtered_foods} | Selected: {selected_foods}"
    
    # Create scatter plot (Protein vs Fat, colored by Energy)
    fig_scatter = px.scatter(
        df_filtered,
        x='Protein_g',
        y='Fat_g',
        color='Energy_kcal',
        hover_data=['Descrip', 'Energy_kcal', 'Protein_g', 'Fat_g'],
        title='Protein vs Fat (colored by Energy)',
        labels={'Protein_g': 'Protein (g)', 'Fat_g': 'Fat (g)', 'Energy_kcal': 'Energy (kcal)'},
        color_continuous_scale='YlOrRd',
        custom_data=[df_filtered.index],
    )
    fig_scatter.update_traces(marker=dict(size=8, opacity=0.6))
    
    # Highlight selected points
    if len(df_selected) < len(df_filtered):
        fig_scatter.add_trace(
            go.Scatter(
                x=df_selected['Protein_g'],
                y=df_selected['Fat_g'],
                mode='markers',
                marker=dict(size=10, color='rgba(0,0,255,0)', line=dict(color='darkblue', width=2)),
                hoverinfo='skip',
                showlegend=True,
                name='Selected',
            )
        )
    
    # Create histogram of Energy (showing both filtered and selected)
    fig_hist = go.Figure()
    
    # Histogram of filtered data
    fig_hist.add_trace(go.Histogram(
        x=df_filtered['Energy_kcal'],
        nbinsx=40,
        name='Filtered',
        marker_color='lightblue',
        opacity=0.7,
    ))
    
    # Histogram of selected data (overlaid)
    if len(df_selected) < len(df_filtered):
        fig_hist.add_trace(go.Histogram(
            x=df_selected['Energy_kcal'],
            nbinsx=40,
            name='Selected',
            marker_color='darkblue',
            opacity=0.8,
        ))
    
    fig_hist.update_layout(
        title='Energy Distribution',
        xaxis_title='Energy (kcal)',
        yaxis_title='Count',
        barmode='overlay',
        hovermode='x unified',
    )
    
    # Create box plot by category
    fig_box = px.box(
        df_selected if len(df_selected) < len(df_filtered) else df_filtered,
        x='Category',
        y='Protein_g',
        color='Category',
        title='Protein Distribution by Category',
        labels={'Protein_g': 'Protein (g)'},
        points='outliers',
        hover_data=['Descrip'],
    )
    
    # Create correlation heatmap
    cols_to_corr = ['Energy_kcal', 'Protein_g', 'Fat_g', 'Carb_g', 'Sugar_g', 'Sodium_mg']
    corr_matrix = df_selected[cols_to_corr].corr() if len(df_selected) > 0 else df_filtered[cols_to_corr].corr()
    
    fig_heatmap = px.imshow(
        corr_matrix,
        text_auto='.2f',
        aspect='auto',
        title='Correlation Heatmap of Major Nutrients (Selected Data)',
        color_continuous_scale='RdBu_r',
        labels=dict(color='Correlation'),
        zmin=-1,
        zmax=1,
    )
    
    return fig_scatter, fig_hist, fig_box, fig_heatmap, info_text

# ============================================================================
# RUN APP
# ============================================================================

if __name__ == '__main__':
    print("Starting Dash app at http://127.0.0.1:8050/")
    print("Press Ctrl+C to quit")
    app.run(debug=True)
