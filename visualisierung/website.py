import dash
import numpy as np
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

# test2

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

connection = connect.create_connection()
baum1 = tie.treedictionary_aus_pickle_importieren()
baum2 = html.Ul(listtree.treedictionary_aus_pickle_importieren())
df = log.all_patients()

app = dash.Dash('')
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

sunburst_data = baum1

age_in_years_num_values_count = df['age_in_years_num'].value_counts()
age_in_years_num_values = age_in_years_num_values_count.keys().tolist()
age_in_years_num_counts = age_in_years_num_values_count.tolist()

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
            html.Div(className='Sunburst',
                     children=html.Div(children=Sunburst(id='sunburst', data=sunburst_data, height=800, width=800),
                                       style={'marginTop': '100px'}), ),
            html.Div(className='Search', children=
            dcc.Input(
                placeholder='Search',
                type='text',
                style={'textAlign': 'center'},
            )),
            html.Div(className='Navigation', children=['Navigation']),
            html.Div(className='NumberOfPatients', children=['Number of patients: ', df['patient_num'].count()]),
            html.Div(className='NavSex',
                     children=[
                         dcc.Graph(
                             id='sex',
                             figure=go.Figure(
                                 data=[go.Pie(labels=['Male', 'Female'],
                                              values=df['sex_cd'].value_counts())],
                                 layout=go.Layout(title='Gender', height=320)))
                     ]),
            html.Div(className='NavAge',
                     children=[
                         dcc.Graph(
                             id='age',
                             figure={
                                 'data': [{
                                     'x': age_in_years_num_values,
                                     'y': age_in_years_num_counts,
                                     'type': 'bar'
                                 }],
                                 'layout': {
                                     'height': 310,
                                     'width': 470,
                                     'title': 'Age'
                                 }
                             }
                         )
                     ]),
            html.Div(className='Save_Load', children=['Save', 'Load'])
        ], style={'font-size': '20px', }),
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
                    dcc.Graph(
                        id='diagramm-alter',
                        figure={'data': [{'x': age_in_years_num_values, 'y': age_in_years_num_counts, 'type': 'bar'}],
                                'layout': {'title': 'Age'
                                           }})
                ], style={'display': 'block'}  # <-- This is the line that will be changed by the checklist callback
                ),
                dcc.Graph(
                    id='diagramm-geschlecht',
                    figure=go.Figure(
                        data=[go.Pie(labels=['Male', 'Female'],
                                     values=df['sex_cd'].value_counts())],
                        layout=go.Layout(title='Gender')))
            ], style={'display': 'block', 'textAlign': 'center'}),
            html.Div(className='Search', children=
            dcc.Input(
                placeholder='Search',
                type='text',
                style={'textAlign': 'center'},
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
        ], style={'font-size': '20px'}),
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
