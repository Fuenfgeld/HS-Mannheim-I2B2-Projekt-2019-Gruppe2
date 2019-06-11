import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_sunburst import Sunburst
from datenhaltung import connection as connect
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from logik import kohortenabfrage as kh

# Farbschema

import tree_dictionary_import_export as tie

baum1 = tie.treedictionary_aus_pickle_importieren('baum_mit_var_text')

wurzel = baum1.knotenliste_mit_baum[0][0]


def create_data_from_node(path):
    if (path == []):
        data = {
            'name': wurzel.text,
            'children': [{
                'name': i.text,
                'size': i.size,
                # 'children':[{
                #   'name' : j.text,
                #   'size' : j.size
                #  }for j in i.children] #Dieser Bereich könnte einen weiteren äußeren Ring hinzufürgen
            } for i in wurzel.children]
        }

    else:
        index = 0
        # print('Angeklickt' +str(path[-1]))
        # print(len(path))
        while baum1.knotenliste_mit_baum[len(path)][index].text != path[-1]:
            #    print(baum.knotenliste_mit_baum[len(path)][index].text)

            index += 1;
        zwischenwurzel = baum1.knotenliste_mit_baum[len(path)][index]

        if not zwischenwurzel.children:

            data = {
                'name': zwischenwurzel.text,
                'size': zwischenwurzel.size

            }

        else:
            data = {
                'name': zwischenwurzel.text,
                'children': [{
                    'name': i.text,
                    'size': i.size,
                    # 'children': [{
                    #   'name': j.text,
                    #    'size': j.size
                    # }for j in i.children]#Dieser Bereich könnte eine zweiten äußeren Ring realisieren

                } for i in zwischenwurzel.children]
            }

    for name in reversed(path[:-1]):
        data = {
            'name': name,
            'children': [data]
        }
    if len(path):
        data = {
            'name': wurzel.text,
            'children': [data]
        }

    return data


external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

connection = connect.create_connection()

app = dash.Dash('__name__',
                external_stylesheets=['https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css',
                                      'https://static.jstree.com/3.0.9/assets/dist/themes/default/style.min.css',

                                      ],

                external_scripts=['http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js',
                                  'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.0.9/jstree.min.js',

                                  ])
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

# sunburst_data = baum1

app.layout = html.Div([
    dcc.Input(className="drop", id="upload-data",
              style={'height': '60px', 'width': '100%', 'border-style': 'dashed', 'line-height': '60px',
                     'text-align': 'center', 'margin': '10px', 'border-width': '1px', 'border-radius': '5px',
                     'border-color': 'blue', 'fonz-size': '20px'}),
    html.Div(className='Navigation', style={'text-align': 'left', 'position': 'absolute', 'top': '185px'},
             children=html.Div(className='container', id='jstree-tree')),
    dcc.Tabs(className='Tabs', id='tabs', children=[
        dcc.Tab(label='Navigation', children=[
            html.Div(className='Sunburst',
                     children=html.Div(
                         children=Sunburst(id='sunburst', data=create_data_from_node([]), height=800, width=800,
                                           selectedPath=[]),
                         style={'position': 'absolute', 'margin-top': '100px', 'margin-left': '35px'}), ),
            html.Div(className='path', id='output'),
            html.Div(className='Search', children=[
            dcc.Input(
                id="search-input",
                className='search-input',
                type='text',
                style={'textAlign': 'center'},
            ),
             html.Button(
                 id="search",
                 children="search"

             )]),
            html.Div(className='Navigation', children=html.Div()),
            html.Div(className='NumberOfPatients', children=['Number of patients: ', kh.frage1.kohortengröße]),
            html.Div(className='NavSex',
                     children=[
                         dcc.Graph(
                             id='sex',
                             figure=go.Figure(
                                 data=[go.Pie(labels=['Male', 'Female'],
                                              values=kh.frage1.geschlecht_value_counts,
                                              marker=dict(colors=['#5CABFF','#4875E8']) )],
                                 layout=go.Layout(title={
                                     'text': 'Gender',
                                     'x': 0.49,
                                     'y': 0.75

                                 }, height=300)))
                     ]),
            html.Div(className='NavAge',
                     children=[
                         dcc.Graph(
                             id='id',
                             figure=go.Figure(
                                 data=[go.Bar(x=kh.frage1.x_achse_altersverteilung,
                                              y=kh.frage1.y_achse_altersverteilung,
                                              text=kh.frage1.y_achse_altersverteilung,
                                              textposition='auto',
                                              marker = dict(color=['#4F5EFF','#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5'])
                                              )],
                                 layout=go.Layout(title={
                                     'text': 'Age',
                                     'x': 0.49,
                                     'y': 0.70

                                 }, height=300, xaxis=dict(title='Age groups'),
                                     yaxis=dict(title='Number of patients'))))
                     ]),
            html.Div(className='Save_Load', children=[
                html.Button(id='save', className='Save', children=['Save']),
                html.Button(id='load', className='Load', children='Load')
            ])
        ], style={'font-size': '20px', }
                ),
        dcc.Tab(className='TabDia', label='Diagram', children=[
            html.Div(className='Dia', children=[

                html.Div([
                    dcc.Graph(
                        id='diagramm-alter',
                        figure=go.Figure(
                            data=[go.Bar(x=kh.frage1.x_achse_altersverteilung,
                                         y=kh.frage1.y_achse_altersverteilung,
                                         text=kh.frage1.y_achse_altersverteilung,
                                         textposition='auto',
                                         marker = dict(color=['#4F5EFF','#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5'])
                                         )],
                            layout=go.Layout(title='Age', xaxis=dict(title='Age groups'),
                                             yaxis=dict(title='Number of patients'))))
                ], style={'display': 'block'}),
                html.Div(className='GeschlechtDia', children=[
                    dcc.Graph(
                        id='diagramm-geschlecht',
                        figure=go.Figure(
                            data=[go.Pie(labels=['Male', 'Female'],
                                         values=kh.frage1.geschlecht_value_counts,
                                         marker=dict(colors=['#5CABFF', ' #4875E8']))],
                            layout=go.Layout(title='Gender', margin={"l": 300, "r": 300}, legend={"x": 0.9, "y": 0.7})))
                ], style={'display': 'block', 'textAlign': 'center'}),

                html.Div([
                    dcc.Graph(
                        id='diagramm-sd',
                        figure=go.Figure(
                            data=[go.Bar(x=kh.frage1.nd_prozent_value_list,
                                         y=kh.frage1.nd_diagnose_value_list,
                                         text=kh.frage1.nd_prozent_value_list,
                                         textposition='outside',
                                         orientation='h',
                                         marker = dict(color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF', '#8093E8', '#9998FF', '#957CEB', '#BE8CFF' ]))],
                            layout=go.Layout(title='Secondary Diagnosis', xaxis=dict(title='Number of patients in %'),
                                             yaxis=go.layout.YAxis(automargin=True, autorange="reversed",
                                                                   ))))
                ], style={'display': 'block'}),
                html.Div(className='race', children=[
                    dcc.Graph(
                        id='diagramm-racepie',
                        figure=go.Figure(
                            data=[go.Pie(labels=kh.frage1.racex,
                                         values=kh.frage1.racey,
                                         marker=dict(colors=['#4F5EFF','#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF']))],
                            layout=go.Layout(title='Race', margin={"l": 300, "r": 300}, legend={"x": 0.9, "y": 0.7})))
                ], style={'display': 'block', 'textAlign': 'center'}),

                html.Div(className='sprache', children=[
                    dcc.Graph(
                        id='diagramm-sprachepie',
                        figure=go.Figure(
                            data=[go.Pie(labels=kh.frage1.sprachex,
                                         values=kh.frage1.sprachey,
                                         marker=dict(colors=['#4F5EFF', ' #5CABFF', '#37E7FF']))],
                            layout=go.Layout(title='Language', margin={"l": 300, "r": 300},
                                             legend={"x": 0.9, "y": 0.7})))
                ], style={'display': 'block', 'textAlign': 'center', }),

            ]),

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
                                                  dcc.Checklist(
                                                      id='checklistSd',
                                                      options=[{'label': 'Secondary Diagnosis', 'value': 'on'}],
                                                      values=['on']),
                                                  dcc.Checklist(
                                                      id='checklistSprache',
                                                      options=[{'label': 'Language', 'value': 'on'}],
                                                      values=['on']),
                                                  dcc.Checklist(
                                                      id='checklistRace',
                                                      options=[{'label': 'Race', 'value': 'on'}],
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
    Output(component_id='diagramm-sd', component_property='style'),
    [Input(component_id='checklistSd', component_property='values')])
def show_hide_element(visibility_state):
    if visibility_state == ['on']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='diagramm-sprachepie', component_property='style'),
    [Input(component_id='checklistSprache', component_property='values')])
def show_hide_element(visibility_state):
    if visibility_state == ['on']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(
    Output(component_id='diagramm-racepie', component_property='style'),
    [Input(component_id='checklistRace', component_property='values')])
def show_hide_element(visibility_state):
    if visibility_state == ['on']:
        return {'display': 'block'}
    else:
        return {'display': 'none'}


@app.callback(Output('sunburst', 'data'), [Input('sunburst', 'selectedPath')])
def display_sun(selectedPath):
    # print(selectedPath)
    return create_data_from_node(path=selectedPath)


@app.callback(Output('output', 'children'), [Input('sunburst', 'selectedPath')])
def display_selected(selected_path):
    return 'Path: {}'.format('->'.join(selected_path or []) or 'Diagnoses')


if __name__ == '__main__':
    app.run_server(debug=False)
