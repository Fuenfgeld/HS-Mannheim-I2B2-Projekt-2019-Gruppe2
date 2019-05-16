import dash
import psycopg2 as psy
import pandas as pd
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
import plotly.graph_objs as go
import treestructuresidenavigation as tsn
from dash_sunburst import Sunburst
import tree_dictionary_import_export as tie
import listtree_dictionary_import_export as listtree
connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
cursor = connection.cursor()
df = pd.read_sql_query("Select *From i2b2demodata.patient_dimension", con=connection)

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

baum = tie.treedictionary_aus_pickle_importieren()
baumliste = html.Ul(listtree.treedictionary_aus_pickle_importieren())

app = dash.Dash('')
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

sunburst_data = baum

app.layout = html.Div([
    html.H1(children = 'IndiGraph', style = {'textAlign' : 'center', 'color' : '#0E23BF', 'backgroundColor':'#AED6F1'}),
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Navigation', children=[
            html.Div([
                dcc.Upload(
                    id = 'upload-data',
                    children= html.Div(['Drag and Drop']),
                    style= {'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'},
                    multiple=True
                 )
            ]),
            html.Div(children = html.Div(children=[Sunburst(id='sun', data=sunburst_data)], style= {'margin' : '200px'}),
                     style={'height' : '800px', 'width': '70%', 'float': 'right', 'borderStyle' : 'solid'}),
            html.Div(children=
                     dcc.Input(
                         placeholder= 'Search',
                         type = 'text',
                     )
                     ,style={'height' : '25px', 'width': '29%', 'borderStyle' : 'solid'}),
            html.Div(className= 'Div3', children=['Navigation', baumliste],
                     style={'height' : '250px', 'width': '29%', 'border-left' : 'solid', 'border-right' : 'solid', 'border-bottom' : 'solid'}),
            html.Div(children=['Number of patients: ', df['patient_num'].count()],
                     style={'height' : '25px', 'width': '29%', 'border-left' : 'solid', 'border-right' : 'solid', 'border-bottom' : 'solid'}),
            html.Div(className= 'Div2',
                children=['Sex',
                        dcc.Graph(
                        id='graph-geschlecht2',
                        figure={
                         'data': [{
                            'x': df['sex_cd'],
                            'y': [10, 20, 30, 40, 50],
                            'type': 'bar'
                            }]

                        }
                    )
            ],
             style={'height' : '250px', 'width': '29%', 'border-left' : 'solid', 'border-right' : 'solid', 'border-bottom' : 'solid'}),
            html.Div(className= 'Div2',
                children=['Age',
                        dcc.Graph(
                         id='graph-alter',
                        figure={
                            'data':[{
                            'x':df['age_in_years_num'],
                            'y':[10,20,30,40,50,60,70,80],
                            'type':'bar'
                        }]
                    }
                )
            ],
            style={'height' : '250px', 'width': '29%', 'border-left' : 'solid', 'border-right' : 'solid', 'border-bottom' : 'solid'}),
         ]),
        dcc.Tab(label='Diagram', children=[
            html.Div([
                dcc.Upload(
                    id = 'upload-data2',
                    children= html.Div(['Drag and Drop']),
                    style= {'width': '100%',
                    'height': '60px',
                    'lineHeight': '60px',
                    'borderWidth': '1px',
                    'borderStyle': 'dashed',
                    'borderRadius': '5px',
                    'textAlign': 'center',
                    'margin': '10px'},
                    multiple=True
                 )
            ]),
            html.Div(className= 'Div3', children = [
                html.Div(children= ['Sex',
                        dcc.Graph(
                        id='graph-geschlecht',
                        figure={
                         'data': [{
                            'x': df['sex_cd'],
                            'y': [10, 20, 30, 40, 50],
                            'type': 'bar'
                            }]

                        }
                    )
            ]),
                html.Div(children= ['Age',
                        dcc.Graph(
                         id='graph-alter2',
                        figure={
                            'data':[{
                            'x':df['age_in_years_num'],
                            'y':[10,20,30,40,50,60,70,80],
                            'type':'bar'
                        }]
                    }
                )
            ])
            ],
                     style={'height' : '800px', 'width': '70%', 'float': 'right', 'borderStyle' : 'solid'}),
            html.Div(children=
                     dcc.Input(
                         placeholder= 'Search',
                         type= 'text'
                     ),
                     style={'height' : '25px', 'width': '29%', 'borderStyle' : 'solid'}),
            html.Div(className= 'Div3', children=['Navigation', baumliste],
                     style={'height' : '250px', 'width': '29%', 'border-left' : 'solid', 'border-right' : 'solid', 'border-bottom' : 'solid'}),
            html.Div(children=['Types '],
                     style={'height' : '525px', 'width': '29%', 'border-left' : 'solid', 'border-right' : 'solid', 'border-bottom' : 'solid'}),
        ]),
    ]),
])



if __name__ == '__main__':
    app.run_server(debug=False)
