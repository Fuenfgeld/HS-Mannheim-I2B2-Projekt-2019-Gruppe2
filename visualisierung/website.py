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


# test

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

connection = connect.create_connection()
baum1 = tie.treedictionary_aus_pickle_importieren()
baum2 = html.Ul(listtree.treedictionary_aus_pickle_importieren())


df = log.all_patients()

app = dash.Dash( __name__,
    external_stylesheets=['https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css',
                          'https://static.jstree.com/3.0.9/assets/dist/themes/default/style.min.css'],
    external_scripts=['http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js',
                      'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.0.9/jstree.min.js'
                      ])
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

sunburst_data = baum1

x_bis_9= ((df['age_in_years_num']).lt(9)).sum()
x_bis_17= (((df['age_in_years_num']).ge(10))&((df['age_in_years_num']).le(17))).sum()
x_bis_34=(((df['age_in_years_num']).ge(18))&((df['age_in_years_num']).le(34))).sum()
x_bis_44=(((df['age_in_years_num']).ge(35))&((df['age_in_years_num']).le(44))).sum()
x_bis_54=(((df['age_in_years_num']).ge(45))&((df['age_in_years_num']).le(54))).sum()
x_bis_64=(((df['age_in_years_num']).ge(55))&((df['age_in_years_num']).le(64))).sum()
x_bis_74=(((df['age_in_years_num']).ge(65))&((df['age_in_years_num']).le(74))).sum()
x_bis_84=(((df['age_in_years_num']).ge(75))&((df['age_in_years_num']).le(84))).sum()
x_gr_gl_65=((df['age_in_years_num']).ge(65)).sum()
x_gr_gl_85=((df['age_in_years_num']).ge(85)).sum()


#print((((df['age_in_years_num']).ge(10))&((df['age_in_years_num']).le(18))).sum())
#print('lll')
#print(((df['age_in_years_num']).lt(10)).sum())
#print(((df['age_in_years_num']).le(18)).sum())

#age_in_years_num_values_count = df['age_in_years_num'].value_counts()
#age_in_years_num_values = age_in_years_num_values_count.keys().tolist()
#age_in_years_num_counts = age_in_years_num_values_count.tolist()





app.layout = html.Div([
    html.H1(children='IndiGraph', style={'textAlign': 'center', 'color': '#0E23BF', 'backgroundColor': '#AED6F1'}),
 html.Div(className='Navigation', style={'position': 'absolute', 'top': '236px'}, children= html.Div(className = 'container', id= 'jstree-tree')),

    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Navigation', id="tab_nav", children=[
            html.Div([
                dcc.Upload(
                    id='upload-data',
                    className='DragAndDrop',
                    children=html.Div(['Drag and Drop']),
                    multiple=True
                )
            ], style={'textAlign': 'center'}),
            html.Div(className='Sunburst', children=html.Div(children=Sunburst(id='sunburst', data=sunburst_data, height = 800, width= 900),
                                                             style={'margin': '10px'}), ),
            html.Div(className='Search', children=
            dcc.Input(
                placeholder='Search',
                type='text',
                style={'textAlign': 'center'},
                size= 69
            )),
           html.Div(className='Navigation', children=html.Div()
  ),
            html.Div(className='NumberOfPatients', children=['Number of patients: ', df['patient_num'].count()]),
            html.Div(className='NavSex',
                     children=[
                               dcc.Graph(
                                   id='sex',
                                   figure=go.Figure(
                                       data=[go.Pie(labels=['Male', 'Female'],
                                                    values=df['sex_cd'].value_counts())],
                                   layout = go.Layout(title='Gender', height=320)))
                               ]),
            html.Div(className='NavAge',
                     children=[
                               dcc.Graph(
                                   id='age',
                                   figure={
                                       'data': [{
                                           'x': ['0-9', '10-17', '18-34', '35-44', '45-54', '55-64', '65-74', '75-84', '>=65', '>=85'], 'y': [x_bis_9, x_bis_17, x_bis_34, x_bis_44, x_bis_54, x_bis_64, x_bis_74, x_bis_84, x_gr_gl_65, x_gr_gl_85],
                                           'type': 'bar'
                                       }],
                                       'layout': {
                                           'height': 290,
                                           'width': 470,
                                           'title': 'Age'
                                       }
                                   }
                               )
                               ]),
        ]),
        dcc.Tab(label='Diagram', id= "tab_dia", children=[
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
                        figure={'data': [{'x': ['0-9', '10-17', '18-34', '35-44', '45-54', '55-64', '65-74', '75-84', '>=65', '>=85'], 'y': [x_bis_9, x_bis_17, x_bis_34, x_bis_44, x_bis_54, x_bis_64, x_bis_74, x_bis_84, x_gr_gl_65, x_gr_gl_85], 'type': 'bar'}],
                                'layout': {'title': 'Age'
                    }})
                 ], style={'display': 'block'}  # <-- This is the line that will be changed by the checklist callback
                ),

            html.Div([
                dcc.Graph(
                    id='diagramm-geschlecht',
                    figure=go.Figure(
                        data=[go.Pie(labels=['Male', 'Female'],
                                     values=df['sex_cd'].value_counts())],
                        layout=go.Layout(title='Gender')))
            ], style={'display': 'block', 'textAlign': 'center'}),

                html.Div([
                    dcc.Graph(
                        id='diagramm-sd',
                        figure={'data': [{'x': [10, 20, 30, 40], 'y': [10, 20, 30, 40], 'type': 'bar'}],
                                'layout': {'title': 'Secondary Diagnosis'
                                           }})
                ], style={'display': 'block'}  # <-- This is the line that will be changed by the checklist callback
                )
                     ]),




            html.Div(className='Search', children=
            dcc.Input(
                placeholder='Search',
                type='text',
                style={'textAlign': 'center'},
                size= 67
            )),
           html.Div(className='Navigation', children= html.Div()),
            html.Div(className='Types',  children=['Types ',
                                                  dcc.Checklist(
                                                      id='checklistAge',
                                                      options=[{'label': 'Age', 'value': 'on'}],
                                                      values=['on']),
                                                  dcc.Checklist(
                                                      id='checklistGender',
                                                      options=[{'label': 'Gender', 'value': 'on'}],
                                                      values=['on']),
                                                   dcc.Checklist(
                                                      id='checklistSD',
                                                      options=[{'label': 'Secondary Diagnosis', 'value': 'on'}],
                                                      values=['on'])




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


@app.callback(
        Output(component_id='diagramm-sd', component_property='style'),
        [Input(component_id='checklistSD', component_property='values')])
def show_hide_element(visibility_state):
        if visibility_state == ['on']:
            return {'display': 'block'}
        else:
            return {'display': 'none'}



if __name__ == '__main__':


    app.run_server(debug=False)
