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

#test

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
    html.H1(children = 'IndiGraph', style = {'textAlign' : 'center', 'color' : '#0E23BF', 'backgroundColor':'#AED6F1'}),
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Navigation', children=[
            html.Div([
                dcc.Upload(
                    id = 'upload-data',
                    className= 'DragAndDrop',
                    children= html.Div(['Drag and Drop']),
                    multiple=True
                 )
            ], style= {'textAlign' : 'center'}),
            html.Div(className= 'Sunburst', children = html.Div(children=[Sunburst(id='sun', data=sunburst_data)], style= {'margin' : '200px'}),),
            html.Div(className= 'Search', children=
                     dcc.Input(
                         placeholder= 'Search',
                         type = 'text',
                         style= {'textAlign' : 'center'}
                     )),
            html.Div(className= 'Navigation', children=['Navigation', baum2]),
            html.Div(className= 'NumberOfPatients', children=['Number of patients: ', df['patient_num'].count()]),
            html.Div(className= 'NavSex',
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
            html.Div(className= 'NavAge',
                children=['Age',
                        dcc.Graph(
                         id='age',
                        figure={
                            'data':[{
                            'x':df['age_in_years_num'],
                            'y':[10,20,30,40,50,60,70,80],
                            'type':'bar'
                        }]
                    }
                )
            ]),
         ]),
        dcc.Tab(label='Diagram', children=[
            html.Div([
                dcc.Upload(
                    id = 'upload-data2',
                    className= 'DragAndDrop',
                    children= html.Div(['Drag and Drop']),
                    multiple=True
                 )
            ], style= {'textAlign' : 'center'}),
            html.Div(className= 'Dia', children = [
                html.Div(children= ['Sex',
                        dcc.Graph(
                        id='sex2',
                        figure={
                         'data': [{
                            'x': df['sex_cd'],
                            'y': [10, 20, 30, 40, 50],
                            'type': 'bar'
                            }]

                        }
                    )
            ], style= {'textAlign' : 'center'}),
                html.Div(children= ['Age',
                        dcc.Graph(
                         id='age2',
                        figure={
                            'data':[{
                            'x':df['age_in_years_num'],
                            'y':[10,20,30,40,50,60,70,80],
                            'type':'bar'
                        }]
                    }
                )
            ], style= {'textAlign' : 'center'})
            ]),
            html.Div(className= 'Search', children=
                     dcc.Input(
                         placeholder= 'Search',
                         type= 'text'
                     )),
            html.Div(className= 'Navigation', children=['Navigation', baum2]),
            html.Div(className= 'Types', children='Types '),
        ]),
    ]),
])



if __name__ == '__main__':
    app.run_server(debug=False)
