import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px
import pandas as pd

# Load the dataset
df = pd.read_csv('cars_2024.csv')

# Initialize the Dash app
app = dash.Dash(__name__)

# Layout of the dashboard
app.layout = html.Div([
    html.H1("Vehicle Sales Dashboard"),
    html.Label("Select State:"),
    dcc.Dropdown(
        id='state-dropdown',
        options=[{'label': state, 'value': state} for state in df['state'].unique()],
        value=df['state'].unique()[0]
    ),
    html.Label("Select Vehicle Type:"),
    dcc.Dropdown(
        id='type-dropdown',
        options=[{'label': vtype, 'value': vtype} for vtype in df['type'].unique()],
        value=df['type'].unique()[0]
    ),
    dcc.Graph(id='sales-graph')
])

# Callback to update the graph based on dropdown selections
@app.callback(
    Output('sales-graph', 'figure'),
    [Input('state-dropdown', 'value'),
     Input('type-dropdown', 'value')]
)
def update_graph(selected_state, selected_type):
    filtered_df = df[(df['state'] == selected_state) & (df['type'] == selected_type)]
    fig = px.bar(filtered_df, x='date_reg', y='model', color='maker', barmode='group')
    return fig

# Run the app
if __name__ == '__main__':
    app.run_server(debug=True)
