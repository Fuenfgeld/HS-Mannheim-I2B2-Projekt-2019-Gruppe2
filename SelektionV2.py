import dash
import psycopg2 as psy
import pandas as pd
from dash.dependencies import Input, Output
import dash_html_components as html
import dash_core_components as dcc
from dash_sunburst import Sunburst
import trees2
import DB_Queries as db  # import from the file with the database query
import row_generator_tables as rg
connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.79", port="5432")
cursor = connection.cursor()
df = pd.read_sql_query("Select *From i2b2demodata.patient_dimension", con=connection)

jsonbaum=trees2.erstellen_dict_baumstruktur()

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']



app = dash.Dash('')

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

sunburst_data = jsonbaum
app.layout = html.Div([

    html.Div([
    html.H1('I2B2 Ersatz'),
    dcc.Tabs(id="tab-navigation-graph", value='tab-navigation-graphen', children=[
        dcc.Tab(label='Navigation', value='tab-navigation-graphen'),
        dcc.Tab(label='Graph', value='tab-graph'),
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
    )], style={'display':'flex', 'float':'right'}),
    dcc.Input(
        placeholder='Zukünftige Suchleiste',
        type='text',
        value=''
    ),html.Div([
        html.Ul(rg.add_list_items(db.get_icd_level_query_df(1)))
    ]),
        ]),
html.Div(
        [Sunburst(id='sun', data=sunburst_data)],
        style={'width': '49%', 'display': 'flex', 'float': 'right'}),

    dcc.Graph(
        id='graph',
        style={'width': '49%', 'display': 'flex', 'float': 'left'}),
    html.Div(id='output', style={'clear': 'both'}),
    html.Div(id='tabs-content-example')


])


@app.callback(Output('tabs-content-example', 'children'),
              [Input('tab-navigation-graph', 'value')])
def render_content(tab):
    if tab == 'tab-navigation-graphen':
        return html.Div([


            html.H3('Grundgesamtheit'),
            html.Div([
                html.H4('Patientenanzahl', style={'text-align':'left'}),
                html.H5(df['patient_num'].count()),
            ]),
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

           ]),
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
            ])
        ],style={'text-align':'left','width':'30%'})
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
        return 'You have selected path: {}'.format('->'.join(selected_path or []) or 'root')

@app.callback(Output('graph', 'figure'), [Input('sun', 'data'), Input('sun', 'selectedPath')])
def display_graph(data, selected_path):
        x = []
        y = []
        text = []
        color = []
        joined_selected = '->'.join(selected_path or [])

        SELECTED_COLOR = '#03c'
        SELECTED_CHILDREN_COLOR = '#8cf'
        SELECTED_PARENTS_COLOR = '#f80'
        DESELECTED_COLOR = '#ccc'

        def node_color(node_path):
            joined_node = '->'.join(node_path)
            if joined_node == joined_selected:
                return SELECTED_COLOR
            if joined_node.startswith(joined_selected):
                return SELECTED_CHILDREN_COLOR
            if joined_selected.startswith(joined_node):
                return SELECTED_PARENTS_COLOR
            return DESELECTED_COLOR

        def append_point(child_count, size, node, node_path):
            x.append(child_count)
            y.append(size)
            text.append(node['name'])
            color.append(node_color(node_path))

        def crawl(node, node_path):
            if 'size' in node:
                append_point(1, node['size'], node, node_path)
                return (1, node['size'])
            else:
                node_count, node_size = 1, 0
                for child in node['children']:
                    this_count, this_size = crawl(child, node_path + [child['name']])
                    node_count += this_count
                    node_size += this_size
                append_point(node_count, node_size, node, node_path)
                return (node_count, node_size)

        crawl(data, [])

        layout = {
            'width': 500,
            'height': 500,
            'xaxis': {'title': 'Total Nodes', 'type': 'log'},
            'yaxis': {'title': 'Total Size', 'type': 'log'},
            'hovermode': 'closest'
        }

        return {
            'data': [{
                'x': x,
                'y': y,
                'text': text,
                'textposition': 'middle right',
                'marker': {
                    'color': color,
                    'size': [(v * v + 100) ** 0.5 for v in y],
                    'opacity': 0.5
                },
                'mode': 'markers+text',
                'cliponaxis': False
            }],
            'layout': layout
        }


if __name__ == '__main__':
    app.run_server(debug=True)