from flask import Flask

import dash
import dash_core_components as dcc
import dash_html_components as html
import pandas as pd
import plotly.graph_objs as go

flask_app = Flask(__name__)
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

df=pd.read_csv("C:/Users/felup/Desktop/i2b2demodata_patient_dimen.csv")
Geschlecht=df['gender']


app.layout = html.Div([
    html.Div([

        html.Div([
            dcc.Dropdown(
			id='x-dopdown',
			options=[
			{'label':'Adresse', 'value':'adress'},
			{'label': 'Gruppe', 'value':'race'}	],
			multi=True,
			value="",
			searchable=True
                
            ),
			
          
        ],
        style={'width': '49%', 'display': 'inline-block'}),

        html.Div([
            dcc.Dropdown(
			id='y-dopdown',
			options=[
			{'label':'Geschlecht', 'value':'gender'},
			{'label': 'Alter', 'value':'age'},
			{'label':'Religon', 'value':'religion'}],
			multi=True,
			value=""
                
            ),
           
            
        ], style={'width': '49%', 'float': 'right', 'display': 'inline-block'})
    ], style={
        'borderBottom': 'thin lightgrey solid',
        'backgroundColor': 'rgb(250, 250, 250)',
        'padding': '10px 5px'
    }),

    html.Div([
        dcc.Graph(
            id='Graph1'
     
        )
    ], style={'width': '49%', 'display': 'inline-block', 'padding': '0 20'}),
    html.Div([
        dcc.Graph(
		id='Graph2'
		),
        dcc.Graph(id='Graph3'),
    ], style={'display': 'inline-block', 'width': '49%'}),

 html.Div(dcc.Slider(
        id='slider',
        min=df['age'].min(),
        max=df['age'].max(),
        value=df['age'].max(),
    ),
	style={'id':'need' ,'width': '49%', 'padding': '0px 20px 20px 20px'})
])
@app.callback(
    dash.dependencies.Output('Graph1', 'figure'),
    [dash.dependencies.Input('x-dopdown', 'value')])
def update_graph_src(selector):
    data = []
    for daten in selector:
        data.append({'x': df[daten], 'y': [10,20,30],
                    'type': 'bar', 'name': daten})
    figure = {
        'data': data,
        'layout': {
            'title': 'Beispiel Graph',
            'xaxis' : dict(
                title=daten,
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                title='Anzahl',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'
            ))
        }
    }
    return figure
	
@app.callback(
    dash.dependencies.Output('Graph2', 'figure'),
    [dash.dependencies.Input('y-dopdown', 'value')])
def update_graph_src(selector):
    data = []
    for daten in selector:
        data.append({'x': [0,10,20,30,40,50,60,70,80], 'y': df[daten],
                    'type': 'line', 'name': daten})
    figure = {
        'data': data,
        'layout': {
            'title': 'Beispiel Graph 2',
            'xaxis' : dict(
                title=daten,
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                title='Anzahl',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'
            ))
        }
    }
    return figure
@app.callback(
    dash.dependencies.Output('Graph3', 'figure'),
    [dash.dependencies.Input('y-dopdown', 'value')])
def update_graph_src(selector):
    data = []
    for daten in selector:
        data.append({'x': df[daten], 'y': [10,20,30,40],
                    'type': 'bar', 'name': daten})
    figure = {
        'data': data,
        'layout': {
            'title': 'Beispiel Graph 3',
            'xaxis' : dict(
                title=daten,
                titlefont=dict(
                family='Courier New, monospace',
                size=20,
                color='#7f7f7f'
            )),
            'yaxis' : dict(
                title='anzahl',
                titlefont=dict(
                family='Helvetica, monospace',
                size=20,
                color='#7f7f7f'
            ))
        }
    }
    return figure


if __name__ == '__main__':
	app.run_server(debug=True, port=5000, host='127.0.0.1')
	app.run_server(debug=True)