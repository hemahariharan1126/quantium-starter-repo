import dash
from dash import dcc, html
import plotly.graph_objs as go
import pandas as pd
from datetime import datetime

# Read the output data
df = pd.read_csv('output.csv')

# Convert date column to datetime and sort
df['date'] = pd.to_datetime(df['date'])
df = df.sort_values('date')

# Group by date and sum sales
daily_sales = df.groupby('date')['sales'].sum().reset_index()

# Initialize the Dash app
app = dash.Dash(__name__)

# Define the layout
app.layout = html.Div([
    html.H1("Pink Morsel Sales Visualization", 
            style={'textAlign': 'center', 'color': '#2c3e50', 'marginTop': '20px'}),
    
    dcc.Graph(
        id='sales-chart',
        figure={
            'data': [
                go.Scatter(
                    x=daily_sales['date'],
                    y=daily_sales['sales'],
                    mode='lines+markers',
                    name='Daily Sales',
                    line=dict(color='#3498db', width=2),
                    marker=dict(size=6)
                )
            ],
            'layout': go.Layout(
                title='Pink Morsel Sales Over Time',
                xaxis={'title': 'Date'},
                yaxis={'title': 'Sales ($)'},
                hovermode='closest',
                plot_bgcolor='#ecf0f1',
                shapes=[
                    # Add vertical line for price increase date (Jan 15, 2021)
                    dict(
                        type='line',
                        x0='2021-01-15',
                        x1='2021-01-15',
                        y0=0,
                        y1=1,
                        yref='paper',
                        line=dict(color='red', width=2, dash='dash')
                    )
                ],
                annotations=[
                    dict(
                        x='2021-01-15',
                        y=0.95,
                        yref='paper',
                        text='Price Increase',
                        showarrow=True,
                        arrowhead=2,
                        ax=0,
                        ay=-40
                    )
                ]
            )
        }
    )
])

if __name__ == '__main__':
    app.run_server(debug=True)
