import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_sunburst import Sunburst
import tree_dictionary_import_export as tie
from logik import db_abfragen as log
from logik import age
from logik import kohortenabfrage
from logik import liste
from datenhaltung import connection as connect
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State

#nur alternative website

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
    html.Div(id='hidden', style={'display':'none'}),
    html.H1(className='IndiGraph', children='IndiGraph'),
    html.Div(
        className="DragAndDrop", children=[
            dcc.Input(
                id="firstarg",
                type="text",
                style={'display': 'inline-block', 'height' : '30px', 'text-align' : 'center'}
            ),
            dcc.Input(
                id="connector",
                value= "",
                type="text",
                readOnly = 'readOnly',
                style={'display': 'inline-block', 'height' : '30px', 'text-align' : 'center'}
            ),
            dcc.Input(
                id="secondarg",
                type="text",
                style={'display': 'inline-block', 'height' : '30px', 'text-align' : 'center'}
            ),
        ]),
    html.Button(
        id="run",
        children="RUN",
        style={
            'height': '30px'}
    ),
    html.Div(className='Navigation', style={'text-align': 'left', 'position': 'absolute', 'top': '280px'},
             children=html.Div(className='container', id='jstree-tree')),
    dcc.Tabs(id='tabs', children=[
        dcc.Tab(label='Navigation', children=[
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
            html.Div(id='data', className='NumberOfPatients',
                     children=['Number of patients: ', df['patient_num'].count()]
                     ),
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
                                     'x': ['0-9', '10-17', '18-34', '35-44', '45-54', '55-64', '65-74', '75-84', '>=65',
                                           '>=85'],
                                     'y': [age.x_bis_9, age.x_bis_17, age.x_bis_34, age.x_bis_44, age.x_bis_54,
                                           age.x_bis_64, age.x_bis_74, age.x_bis_84, age.x_gr_gl_65, age.x_gr_gl_85],
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
                html.Button(id='save', className='Save', children='Save'),
                html.Button(id='load', className='Load', children='Load')
            ])
        ], style={'font-size': '20px', }),
        dcc.Tab(label='Diagram', children=[
            html.Div(className='Dia', children=[
                # Create Div to place a conditionally visible element inside
                html.Div([
                    dcc.Graph(
                        id='diagramm-alter',
                        figure={'data': [{'x': ['0-9', '10-17', '18-34', '35-44', '45-54', '55-64', '65-74', '75-84',
                                                '>=65', '>=85'],
                                          'y': [age.x_bis_9, age.x_bis_17, age.x_bis_34, age.x_bis_44, age.x_bis_54,
                                                age.x_bis_64, age.x_bis_74, age.x_bis_84, age.x_gr_gl_65,
                                                age.x_gr_gl_85],
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

@app.callback(
    Output(component_id='connector', component_property='value'),
    [Input(component_id='run', component_property='n_clicks')],
    [State(component_id='firstarg', component_property='value'),
     State(component_id='secondarg', component_property='value')])
def update_list(n_clicks, value1, value2):
    the_list = liste.The_List()
    the_list.make_list(value1)
    the_list.make_list(value2)
    if not value1 and not value2:
        print("null")
        return "Kein Kriterium"
    elif not value2 or not value1:
        print("eins")
        koho = kohortenabfrage.Kohortenabfrage(the_list.get_list(), [""])
        return ""
    else:
        print("zwei")
        koho = kohortenabfrage.Kohortenabfrage(the_list.get_list(), ["AND"])
        return ("AND")









if __name__ == '__main__':
    app.run_server(debug=False)
