import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_sunburst import Sunburst
import tree_dictionary_import_export as tie
from logik import db_abfragen as log
from logik import age
from datenhaltung import connection as connect
import plotly.graph_objs as go
from dash.dependencies import Input, Output

#dnd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

connection = connect.create_connection()
baum1 = tie.treedictionary_aus_pickle_importieren()
df = log.all_patients()

app = dash.Dash('__name__',
                external_stylesheets=['https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css',
                                      'https://static.jstree.com/3.0.9/assets/dist/themes/default/style.min.css',
                                      ],

                external_scripts=['http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js',
                                  'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.0.9/jstree.min.js',

                                  ])
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

sunburst_data = baum1



age_in_years_num_values_count = df['age_in_years_num'].value_counts()
age_in_years_num_values = age_in_years_num_values_count.keys().tolist()
age_in_years_num_counts = age_in_years_num_values_count.tolist()

app.layout = html.Div([
    html.H1(className='IndiGraph', children='IndiGraph'),
html.Div(className="drop",
                     style={'height' : '60px', 'width' : '100%', 'border-style': 'dashed', 'line-height' : '60px', 'text-align' : 'center', 'margin' : '10px', 'border-width' : '1px', 'border-radius' : '5px', 'border-color' : 'blue', 'fonz-size' : '20px' }),
    html.Div(className='Navigation', style={'text-align': 'left', 'position': 'absolute', 'top': '250px'},
             children=html.Div(className='container', id='jstree-tree')),
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Navigation', children=[
            # html.Div(className='jstree-drop', children=[
            #     dcc.Upload(
            #         id='upload-data',
            #         className='DragAndDrop',
            #         children=html.Div(['Drag and Drop']),
            #         multiple=True
            #     ),
            #     html.Div(id='output-data-upload')
            # ], style={'textAlign': 'center'}),

            html.Div(className='Sunburst',
                     children=html.Div(children=Sunburst(id='sunburst', data=sunburst_data, height=800, width=800),
                                       style={'marginTop': '100px'}), ),
            html.Div(className='Search', children=
            dcc.Input(
                id="search-input",
                placeholder='Search',
                type='text',
                style={'textAlign': 'center'},
            )),
            html.Div(className='Navigation', children=html.Div()),
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
                                     'x': ['0-9', '10-17', '18-34', '35-44', '45-54', '55-64', '65-74', '75-84', '>=65', '>=85'],
                                     'y': [age.x_bis_9, age.x_bis_17, age.x_bis_34, age.x_bis_44, age.x_bis_54, age.x_bis_64, age.x_bis_74, age.x_bis_84, age.x_gr_gl_65, age.x_gr_gl_85],
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
            html.Div(className='Save_Load', children=[
                html.Button(id='save', className='Save', children=['Save']),
                html.Button(id='load', className='Load', children='Load')
            ])
        ], style={'font-size': '20px', }),
        dcc.Tab(label='Diagram', children=[
            html.Div(className='Dia', children=[
                # Create Div to place a conditionally visible element inside
                html.Div([
                    dcc.Graph(
                        id='diagramm-alter',
                        figure={'data': [{'x': ['0-9', '10-17', '18-34', '35-44', '45-54', '55-64', '65-74', '75-84', '>=65', '>=85'],
                                          'y': [age.x_bis_9, age.x_bis_17, age.x_bis_34, age.x_bis_44, age.x_bis_54, age.x_bis_64, age.x_bis_74, age.x_bis_84, age.x_gr_gl_65, age.x_gr_gl_85],
                                          'type': 'bar'}],
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
            html.Div(className='Navigation', children=html.Div()),
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
            html.Div(className='Save_Load', children=[
                html.Button(id='save2', className='Save', children='Save'),
                html.Button(id='load2', className='Load', children='Load')
            ])
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


# @app.callback(Output('output-data-upload', component_property='children'),
#               [Input('upload-data', 'contents')])
# def update_output(list_of_contents):
#     if list_of_contents is not None:
#         children = 'Hallo!'
#         return children


if __name__ == '__main__':
    app.run_server(debug=False)