import numpy as np
import pandas as pd
import plotly.graph_objects as go
import dash
from dash import dcc, html  # <-- Naya tareeka (Imports fixed)
from dash.dependencies import Input, Output

# external CSS stylesheets
external_stylesheets = [
    {
        'href': 'https://stackpath.bootstrapcdn.com/bootstrap/4.1.3/css/bootstrap.min.css',
        'rel': 'stylesheet',
        'integrity': 'sha384-MCw98/SFnGE8fJT3GXwEOngsV7Zt27NXFoaoApmYm81iuXoPkFOJwJ8ERdknLPMO',
        'crossorigin': 'anonymous'
    }
]
patients = pd.read_csv('IndividualDetails.csv')
total = patients.shape[0]
Active = patients[patients['current_status'] == 'Hospitalized'].shape[0]
Recovered = patients[patients['current_status'] == 'Recovered'].shape[0]
Deaths = patients[patients['current_status'] == 'Deceased'].shape[0]

options = [
    {'label': 'All', 'value': 'All'},
    {'label': 'Hospitalized', 'value': 'Hospitalized'},
    {'label': 'Recovered', 'value': 'Recovered'},
    {'label': 'Deceased', 'value': 'Deceased'}
]

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.layout = html.Div([
    html.H1("Cornona Virus Pandemic", style={'color': '#fff', 'textAlign': 'center'}),

    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Total Cases", className='text-light'),
                    html.H4(total, className='text-light')
                ], className='card-body')
            ], className='card bg-danger')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Active Cases", className='text-light'),
                    html.H4(Active, className='text-light')
                ], className='card-body')
            ], className='card bg-info')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Recovered", className='text-light'),
                    html.H4(Recovered, className='text-light')
                ], className='card-body')
            ], className='card bg-warning')
        ], className='col-md-3'),
        html.Div([
            html.Div([
                html.Div([
                    html.H3("Deaths", className='text-light'),
                    html.H4(Deaths, className='text-light')
                ], className='card-body')
            ], className='card bg-success')
        ], className='col-md-3')

    ], className='row'),
    html.Div([], className='row'),
    html.Div([
        html.Div([
            html.Div([
                html.Div([
                    dcc.Dropdown(id='picker', options=options, value='All'),
                    dcc.Graph(id='bar')
                ], className='card-body')
            ], className='card')
        ], className='col-md-12')
    ], className='row'),
    html.Div([], className='row')

], className='container')


# Note: Iske neeche aap apna layout (app.layout) banayenge...

@app.callback(Output('bar', 'figure'), [Input('picker', 'value')])
def updated_graph(type):
    if type == 'All':
        pbar = patients['detected_state'].value_counts().reset_index()
        # Naye Pandas ke hisaab se columns ke naam sahi kiye
        pbar.columns = ['detected_state', 'count']

        return {
            'data': [
                # x par state ke naam aur y par unka count pass kiya
                go.Bar(x=pbar['detected_state'], y=pbar['count'])
            ],
            'layout': go.Layout(title="State Total Count (All Cases)")
        }
    else:
        npat = patients[patients['current_status'] == type]
        pbar = npat['detected_state'].value_counts().reset_index()
        # Naye Pandas ke hisaab se columns ke naam sahi kiye
        pbar.columns = ['detected_state', 'count']

        return {
            'data': [
                # x par state ke naam aur y par unka count pass kiya
                go.Bar(x=pbar['detected_state'], y=pbar['count'])
            ],
            'layout': go.Layout(title=f"State Total Count ({type})")
        }


if __name__ == "__main__":
    app.run(debug=True, port=8054)