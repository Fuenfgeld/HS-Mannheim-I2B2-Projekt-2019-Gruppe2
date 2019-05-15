import dash
import psycopg2 as psy
import pandas as pd
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from dash_sunburst import Sunburst
import trees2
import treestructuresidenavigation as tsn
import tree_dictionary_import_export as tie
connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.75", port="5432")
cursor = connection.cursor()
df = pd.read_sql_query("Select *From i2b2demodata.patient_dimension", con=connection)

#jsonbaum=trees2.erstellen_dict_baumstruktur()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

jsonbaum=tie.treedictionary_aus_pickle_importieren()



app = dash.Dash('')

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

sunburst_data = jsonbaum
app.layout = html.Div([

    html.Div([
    html.H1('IndiGraph'),
    dcc.Tabs(id="tab-navigation-graph", value='tab-navigation-graphen', children=[
        dcc.Tab(label='Navigation', value='tab-navigation-graphen'),
        dcc.Tab(label='Diagramm', value='tab-graph'),
    ]),
    html.Div([
    dcc.Upload(
        id='upload-data',
        children=html.Div([
            'Drag and Drop or ',
            html.A('Select Files')
        ]),
        style={
            'width': '100%',
            'height': '60px',
            'lineHeight': '60px',
            'borderWidth': '1px',
            'borderStyle': 'dashed',
            'borderRadius': '5px',
            'textAlign': 'center',
            'margin': '10px'
        },
        multiple=True
    )], style={'display':'flex', 'float':'right','margin':'4px'}),

    dcc.Input(
        placeholder='Zukünftige Suchleiste',
        type='text',
        value='',

    ),html.Div([
      html.Ul(tsn.add_groundlevel())
    ]),
        ]),
html.Div(
        [Sunburst(id='sun', data=sunburst_data)],
        style={'width': '49%', 'display': 'flex', 'float': 'right'}),

    html.Div(id='output', style={'clear': 'both'}),
    html.Div(id='tabs-content-example')


])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tab-navigation-graph', 'value')])
def render_content(tab):
    if tab == 'tab-navigation-graphen':
        return html.Div([


            html.H3('Grundgesamtheit', style={'border-width':'3px','border-style':'solid','margin-top':'15px'}),
            html.Div([
                html.H4('Patientenanzahl', style={'text-align':'left', }),
                html.H5(df['patient_num'].count()),
            ],style={'border-width':'3px','border-style':'solid'}),
            html.Div([
                html.H4('Altersverteilung'),
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

           ],style={'border-width':'3px','border-style':'solid'}),
            html.Div([
                html.H4('Geschlechterverteilung'),
                dcc.Graph(
                    id='graph-geschlecht',
                    figure={
                        'data':[{
                            'x':df['sex_cd'],
                            'y':[10,20,30,40,50],
                            'type':'bar'
                        }]

                }
                )
            ], style={'border-width':'3px','border-style':'solid'})
        ],style={'text-align':'left','width':'30%','margin-top':'-40%', 'border-width':'10px'})
    elif tab == 'tab-graph':
        return html.Div([
            html.H3('sowas anderes'),
            dcc.Checklist(
                options=[
                    {'label': 'Option1', 'value': 'Op1'},
                    {'label': 'Option2', 'value': 'Op2'},
                    {'label': 'Option3', 'value': 'Op3'}
                ],
                values=['Op1', 'Op2'],
                labelStyle={'display': 'inline-block'}
            ),
            dcc.Graph(
                id='graph-tab2',
                figure={
                    'data': [{
                        'x': df['age_in_years_num'],
                        'y': [10, 20, 30, 40, 50, 60, 70, 80],
                        'type': 'bar'
                    }]
                }
            )

        ])

@app.callback(Output('output', 'children'), [Input('sun', 'selectedPath')])
def display_selected(selected_path):
        layout={'width': '49%', 'display': 'flex', 'float': 'right'}
        return 'You have selected path: {}'.format('->'.join(selected_path or []) or 'root')




if __name__ == '__main__':
    app.run_server(debug=False)