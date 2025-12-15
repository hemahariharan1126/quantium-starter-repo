import dash
from dash import dcc, html, Input, Output
import plotly.graph_objs as go
import pandas as pd

# Read the output data
df = pd.read_csv('output.csv')

# Convert date column to datetime and sort
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Initialize the Dash app
app = dash.Dash(__name__)

# Define custom CSS styling
app.layout = html.Div(style={
    'fontFamily': 'Arial, sans-serif',
    'backgroundColor': '#f5f7fa',
    'padding': '20px',
    'minHeight': '100vh'
}, children=[
    # Header
    html.Div([
        html.H1("Pink Morsel Sales Dashboard", 
                style={
                    'textAlign': 'center',
                    'color': '#2c3e50',
                    'marginBottom': '10px',
                    'fontSize': '2.5em',
                    'fontWeight': 'bold'
                }),
        html.P("Analyzing Sales Performance Before and After Price Increase",
               style={
                   'textAlign': 'center',
                   'color': '#7f8c8d',
                   'fontSize': '1.2em',
                   'marginBottom': '30px'
               })
    ]),
    
    # Controls Section
    html.Div([
        html.Label("Filter by Region:", 
                   style={
                       'fontSize': '1.1em',
                       'fontWeight': 'bold',
                       'color': '#34495e',
                       'marginBottom': '10px',
                       'display': 'block'
                   }),
        dcc.RadioItems(
            id='region-filter',
            options=[
                {'label': ' All Regions', 'value': 'all'},
                {'label': ' North', 'value': 'north'},
                {'label': ' East', 'value': 'east'},
                {'label': ' South', 'value': 'south'},
                {'label': ' West', 'value': 'west'}
            ],
            value='all',
            style={
                'fontSize': '1em',
                'color': '#2c3e50'
            },
            labelStyle={
                'display': 'inline-block',
                'marginRight': '20px',
                'padding': '8px 15px',
                'backgroundColor': 'white',
                'borderRadius': '5px',
                'boxShadow': '0 2px 4px rgba(0,0,0,0.1)',
                'cursor': 'pointer',
                'marginBottom': '10px'
            }
        )
    ], style={
        'backgroundColor': 'white',
        'padding': '25px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)',
        'marginBottom': '25px'
    }),
    
    # Graph Section
    html.Div([
        dcc.Graph(id='sales-chart')
    ], style={
        'backgroundColor': 'white',
        'padding': '25px',
        'borderRadius': '10px',
        'boxShadow': '0 4px 6px rgba(0,0,0,0.1)'
    })
])

# Callback to update graph based on region filter
@app.callback(
    Output('sales-chart', 'figure'),
    Input('region-filter', 'value')
)
def update_graph(selected_region):
    # Filter data based on selected region
    if selected_region == 'all':
        filtered_df = df
    else:
        filtered_df = df[df['region'] == selected_region]
    
    # Group by date and sum sales
    daily_sales = filtered_df.groupby('date')['sales'].sum().reset_index()
    
    # Create figure
    figure = {
        'data': [
            go.Scatter(
                x=daily_sales['date'],
                y=daily_sales['sales'],
                mode='lines+markers',
                name='Daily Sales',
                line=dict(color='#3498db', width=3),
                marker=dict(size=8, color='#2980b9'),
                hovertemplate='<b>Date</b>: %{x|%Y-%m-%d}<br><b>Sales</b>: $%{y:,.2f}<extra></extra>'
            )
        ],
        'layout': go.Layout(
            title=dict(
                text=f'Pink Morsel Sales Over Time - {selected_region.title() if selected_region != "all" else "All Regions"}',
                font=dict(size=22, color='#2c3e50', family='Arial, sans-serif')
            ),
            xaxis=dict(
                title='Date',
                titlefont=dict(size=16, color='#34495e'),
                gridcolor='#ecf0f1',
                showline=True,
                linecolor='#bdc3c7'
            ),
            yaxis=dict(
                title='Sales ($)',
                titlefont=dict(size=16, color='#34495e'),
                gridcolor='#ecf0f1',
                showline=True,
                linecolor='#bdc3c7'
            ),
            hovermode='closest',
            plot_bgcolor='#fafafa',
            paper_bgcolor='white',
            shapes=[
                # Add vertical line for price increase date (Jan 15, 2021)
                dict(
                    type='line',
                    x0='2021-01-15',
                    x1='2021-01-15',
                    y0=0,
                    y1=1,
                    yref='paper',
                    line=dict(color='#e74c3c', width=2, dash='dash')
                )
            ],
            annotations=[
                dict(
                    x='2021-01-15',
                    y=0.95,
                    yref='paper',
                    text='<b>Price Increase</b><br>Jan 15, 2021',
                    showarrow=True,
                    arrowhead=2,
                    arrowcolor='#e74c3c',
                    ax=0,
                    ay=-60,
                    font=dict(size=12, color='#e74c3c'),
                    bgcolor='rgba(231, 76, 60, 0.1)',
                    bordercolor='#e74c3c',
                    borderwidth=2,
                    borderpad=4
                )
            ],
            margin=dict(l=60, r=40, t=80, b=60)
        )
    }
    
    return figure

if __name__ == '__main__':
    app.run_server(debug=True)
