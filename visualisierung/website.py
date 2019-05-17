import dash
import psycopg2 as psy
import pandas as pd
import dash_html_components as html
import dash_core_components as dcc
from dash_sunburst import Sunburst
import tree_dictionary_import_export as tie
import listtree_dictionary_import_export as listtree
from logik import db_abfragen as log
from datenhaltung import connection as connect
import plotly.graph_objs as go
from dash.dependencies import Input, Output

# test

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

connection = connect.create_connection()
baum1 = tie.treedictionary_aus_pickle_importieren()
baum2 = html.Ul(listtree.treedictionary_aus_pickle_importieren())
df = log.all_patients()

app = dash.Dash('')
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

sunburst_data = baum1

app.layout = html.Div([
    html.H1(children='IndiGraph', style={'textAlign': 'center', 'color': '#0E23BF', 'backgroundColor': '#AED6F1'}),
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Navigation', children=[
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    className='DragAndDrop',
                    children=html.Div(['Drag and Drop']),
                    multiple=True
                )
            ], style={'textAlign': 'center'}),
            html.Div(className='Sunburst', children=html.Div(children=Sunburst(id='sunburst', data=sunburst_data),
                                                             style={'margin': '200px'}), ),
            html.Div(className='Search', children=
            dcc.Input(
                placeholder='Search',
                type='text',
                style={'textAlign': 'center'}
            )),
            html.Div(className='Navigation', children=['Navigation']),
            html.Div(className='NumberOfPatients', children=['Number of patients: ', df['patient_num'].count()]),
            html.Div(className='NavSex',
                     children=['Sex',
                               dcc.Graph(
                                   id='sex',
                                   figure={
                                       'data': [{
                                           'x': df['sex_cd'],
                                           'y': [10, 20, 30, 40, 50],
                                           'type': 'bar'
                                       }]

                                   }
                               )
                               ]),
            html.Div(className='NavAge',
                     children=['Age',
                               dcc.Graph(
                                   id='age',
                                   figure={
                                       'data': [{
                                           'x': df['age_in_years_num'],
                                           'y': [10, 20, 30, 40, 50, 60, 70, 80],
                                           'type': 'bar'
                                       }]
                                   }
                               )
                               ]),
        ]),
        dcc.Tab(label='Diagram', children=[
            html.Div([
                dcc.Upload(
                    id='upload-data2',
                    className='DragAndDrop',
                    children=html.Div(['Drag and Drop']),
                    multiple=True
                )
            ], style={'textAlign': 'center'}),
            html.Div(className='Dia', children=[
                # Create Div to place a conditionally visible element inside
                html.Div([
                    html.H4(children="Age", style={'textAlign': 'center'}),
                    dcc.Graph(
                        id='diagramm-alter',
                        figure={'data': [{'x': [20, 30, 40], 'y': [10, 20, 30, 40, 50, 60, 70, 80], 'type': 'bar'}]})
                ], style={'display': 'block'}  # <-- This is the line that will be changed by the checklist callback
                ),
                html.H4(children='Gender', style={'textAlign': 'center'}),
                dcc.Graph(
                    id='diagramm-geschlecht',
                    figure=go.Figure(
                        data=[go.Pie(labels=['Male', 'Female'],
                                     values=[20, 80])]))
            ], style={'display': 'block', 'textAlign': 'center'}),
            html.Div(className='Search', children=
            dcc.Input(
                placeholder='Search',
                type='text'
            )),
            html.Div(className='Navigation', children=['Navigation']),
            html.Div(className='Types', children=['Types ',
                                                  dcc.Checklist(
                                                      id='checklistAge',
                                                      options=[{'label': 'Age', 'value': 'on'}],
                                                      values=['on']),
                                                  dcc.Checklist(
                                                      id='checklistGender',
                                                      options=[{'label': 'Gender', 'value': 'on'}],
                                                      values=['on']),
                                                  ]),
        ]),
    ]),
])


@app.callback(
    Output(component_id='diagramm-alter', component_property='style'),
    [Input(component_id='checklistAge', component_property='values')])
def show_hide_element(visibility_state):
    if visibility_state == ['on']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='diagramm-geschlecht', component_property='style'),
    [Input(component_id='checklistGender', component_property='values')])
def show_hide_element(visibility_state):
    if visibility_state == ['on']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


if __name__ == '__main__':
    app.run_server(debug=False)
