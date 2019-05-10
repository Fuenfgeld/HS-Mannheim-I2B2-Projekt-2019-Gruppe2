import dash
from dash.dependencies import Input, Output
import dash_core_components as dcc
import dash_html_components as html
import psycopg2 as psy
import pandas as pd
from dash_sunburst import Sunburst


connection = psy.connect(database="i2b2", user="i2b2", password="demouser", host="129.206.7.79", port="5432")
cursor = connection.cursor()

df = pd.read_sql_query(f"select distinct(patient_num) from i2b2demodata.observation_fact where concept_cd in (select concept_cd from i2b2demodata.concept_dimension where concept_path like '_Diagnosis')", con=connection)
df.name='Neurolgic Disorders'
print(df)
df_neurologic_eye=pd.read_sql_query("select distinct(patient_num) from i2b2demodata.observation_fact where concept_cd in (select concept_cd from i2b2demodata.concept_dimension where concept_path like '%Neurologic Disorders%Eye%')",con=connection)
df_neurologic_eye.name='neurologic Eye'
df_neurolgoic_infectious=pd.read_sql_query("select distinct(patient_num) from i2b2demodata.observation_fact where concept_cd in (select concept_cd from i2b2demodata.concept_dimension where concept_path like '%Neurologic Disorders%Infectious diseases%')", con=connection)
df_neurolgoic_infectious.name=' neurologic infectious'

app = dash.Dash('')

app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

sunburst_data = {
    'name': 'Ich bin eine Demonstration',
    'children': [
        {
            'name':'Vater1',
            'size':df.size,
            'children': [
                {'name': 'Kind11', 'size': df_neurologic_eye.size, 'children':[{'name': 'Enkel','size':5}]},
                {'name': 'Kind12', 'size': df_neurolgoic_infectious.size},
                {'name': 'Kind13', 'size': 4},
                {'name': 'Kind14', 'size': 1},
                {'name': 'Kind15', 'size': 5},
                {'name': 'Kind16', 'size': 2}
            ]
        },
        {
            'name': 'Vater2',
            'children': [
                {'name': 'Kind21', 'size': 3.5},
                {'name': 'Kind22', 'size': 2.5},
                {'name': 'Kind23', 'size': 1.5},
                {'name': 'Kind25', 'size': 8},
                {'name': 'Kind26', 'size': 1.7}
            ]
        },
        {'name': 'Vater ohne Kind1', 'size': 4.5},
        {'name': 'Vater ohne Kind2', 'size': 10},
        {'name': 'Vater ohne Kind3', 'size': 7.5},
        {
            'name': 'Vater3',
            'children': [
                {'name': 'Kind31', 'size': 9},
                {'name': 'Kind32', 'size': 3.2},
                {'name': 'Kind33', 'size': 4.7},
                {'name': 'Kind34', 'size': 7},
                {'name': 'Kind35', 'size': 5.5}
            ]
        },
        {
            'name': 'vater4',
            'children': [
                {'name': 'Kind41', 'size': 5.7},
                {'name': 'Kind42', 'size': 3.8},
                {'name': 'Kind43', 'size': 4.7},
                {'name': 'Kind44', 'size': 5.3}
            ]
        },
        {'name': 'vater ohne kind 4', 'size': 11}
    ]
}

app.layout = html.Div([
    html.Div(
        [Sunburst(id='sun', data=sunburst_data)],
        style={'width': '49%', 'display': 'inline-block', 'float': 'left'}),
    dcc.Graph(
        id='graph',
        style={'width': '49%', 'display': 'inline-block', 'float': 'left'}),
    html.Div(id='output', style={'clear': 'both'})
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
                'size': [(v*v + 100)**0.5 for v in y],
                'opacity': 0.5
            },
            'mode': 'markers+text',
            'cliponaxis': False
        }],
        'layout': layout
    }

if __name__ == '__main__':
    app.run_server(debug=True)