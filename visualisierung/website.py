import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_sunburst import Sunburst
from datenhaltung import connection as connect
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from logik import kohortenabfrage as kh
import tree_dictionary_import_export as tie
from logik import querystack

baum1 = tie.treedictionary_aus_pickle_importieren('baum_mit_shortcode')
qs = querystack.Querystack.getInstance()
wurzel = baum1.knotenliste_mit_baum[0][0]


def create_data_from_node(path):
    if (path == []):
        data = {
            'name': wurzel.shortcode,
            'children': [{
                'name': i.shortcode,
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
        while baum1.knotenliste_mit_baum[len(path)][index].shortcode != path[-1]:
            #    print(baum.knotenliste_mit_baum[len(path)][index].text)

            index += 1;
        zwischenwurzel = baum1.knotenliste_mit_baum[len(path)][index]

        if not zwischenwurzel.children:

            data = {
                'name': zwischenwurzel.shortcode,
                'size': zwischenwurzel.size

            }

        else:
            data = {
                'name': zwischenwurzel.shortcode,
                'children': [{
                    'name': i.shortcode,
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
            'name': wurzel.shortcode,
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
app.title = "IndiGraph"
app.layout = html.Div([

    dcc.Input(className="drop", id="upload-data",
              style={'height': '60px', 'width': '100%', 'border-style': 'dashed', 'line-height': '60px',
                     'text-align': 'center', 'margin': '10px', 'border-width': '1px', 'border-radius': '5px',
                     'border-color': 'blue', 'fonz-size': '20px'}),

    html.Div(className='Search', children=[
        dcc.Input(
            id="search-input",
            className='search-input',
            type='text',
            style={'textAlign': 'center', 'width': '70%'},
        ),
        html.Button(id="search",title="search"),
        html.Button(id="reset", title="reset",
        )], style={'top': '120px', 'position': 'absolute'}),
    html.Div(className='Navigation', style={'text-align': 'left', 'position': 'absolute', 'top': '160px'},
             children=html.Div(className='container', id='jstree-tree')),
    html.Div(html.Button(id='save', title="save")),
    html.Div(html.Button(id='load', title="load")),
    html.Div(html.Button(id='run', title="run")),
    dcc.Tabs(className='Tabs', id='tabs', children=[
        dcc.Tab(label='Navigation', children=[
            html.Div(className='Sunburst',
                     children=html.Div(
                         children=[
                             html.Div(className='path', id='output'),
                             html.Button(
                                 id="add",title="add"),
                             Sunburst(id='sunburst', data=create_data_from_node([]), height=650, width=800,
                                      selectedPath=[])],
                         style={'position': 'absolute', 'margin-left': '35px', 'margin-top': '10px'}), ),
            html.Div(className='Search', children=html.Div()),
            html.Div(className='Navigation', children=html.Div()),
            html.Div(className='NumberOfPatients', id="count",
                     children=['Count: ', qs.bottom().kohortengröße, ' (', qs.bottom().kohortengröße_prozent, '%)']),
            html.Div(className='NavSex',
                     children=[
                         dcc.Graph(
                             id='sex',
                             figure=go.Figure(
                                 data=[go.Pie(labels=['Male', 'Female'],
                                              values=qs.bottom().geschlecht_value_counts,
                                              marker=dict(colors=['#5CABFF', '#4875E8']))],
                                 layout=go.Layout(title={
                                     'text': 'Gender',
                                     'x': 0.49,
                                     'y': 0.75

                                 }, height=300)))
                     ]),
            html.Div(className='NavAge',
                     children=[
                         dcc.Graph(
                             id='age',
                             figure=go.Figure(
                                 data=[go.Bar(x=qs.bottom().x_achse_altersverteilung,
                                              y=qs.bottom().y_achse_altersverteilung,
                                              text=qs.bottom().y_achse_altersverteilung,
                                              textposition='auto',
                                              marker=dict(color=['#4F5EFF', '#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF',
                                                                 '#8BCAF5'])
                                              )],
                                 layout=go.Layout(title={
                                     'text': 'Age',
                                     'x': 0.49,
                                     'y': 0.70

                                 }, height=300, xaxis=dict(title='Age groups'),
                                     yaxis=dict(title='Number of patients'))))
                     ]),

        ], style={'font-size': '20px', }
                ),
        dcc.Tab(className='TabDia', label='Diagram', children=[
            html.Div(className='DiaBar', children=[

                html.Div(style={'text-align' : 'center'}, id= 'count2',
                    children=['Count: ', qs.bottom().kohortengröße, ' (', qs.bottom().kohortengröße_prozent, '%)']),

                html.Div(className='alterBar', children=[
                    dcc.Graph(
                        id='diagramm-alter',
                        figure=go.Figure(
                            data=[go.Bar(x=qs.bottom().x_achse_altersverteilung,
                                         y=qs.bottom().y_achse_altersverteilung,
                                         text=qs.bottom().y_achse_altersverteilung,
                                         textposition='auto',
                                        hoverinfo='none',
                                         marker=dict(
                                             color=['#4F5EFF', '#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5'])
                                         )],
                            layout=go.Layout(title={
                                'text': 'Age',
                                'x': 0.49,
                                'y': 0.85

                            }, xaxis=dict(title='Age groups'), yaxis=dict(title='Number of patients'))))
                ], style={'display': 'block'}),

                html.Div(className='sdBar', children=[

                    dcc.Graph(
                        id='diagramm-sd',
                        figure=go.Figure(
                            data=[go.Bar(x=qs.bottom().nd_prozent_value_list,
                                         y=qs.bottom().nd_diagnose_value_list,
                                         text=qs.bottom().nd_prozent_value_list,
                                         textposition='auto',
                                         orientation='h',
                                            hoverinfo='none',
                                         marker=dict(
                                             color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF',
                                                    '#8093E8', '#9998FF', '#957CEB', '#BE8CFF']))],
                            layout=go.Layout(title='Secondary Diagnosis', xaxis=dict(title='Number of patients in %'), margin=go.layout.Margin(l=400, r= 20

    ),
                                             yaxis=go.layout.YAxis(automargin=True, autorange="reversed",
                                                                   ))))
                ], style={'display': 'block'}),
            ]),

            html.Div(className='DiaPie', children=[

                html.Div(className='genderPie', children=[
                    dcc.Graph(
                        id='diagramm-geschlecht',
                        figure=go.Figure(
                            data=[go.Pie(labels=['Male', 'Female'],
                                         values=qs.bottom().geschlecht_value_counts,
                                         marker=dict(colors=['#5CABFF', ' #4875E8']))],
                            layout=go.Layout(title={
                                'text': 'Gender',
                                'x': 0.49,
                                'y': 0.80

                            }, height=330)))
                ], style={'display': 'block', 'textAlign': 'center'}),

                html.Div(className='racePie', children=[
                    dcc.Graph(
                        id='diagramm-racepie',
                        figure=go.Figure(
                            data=[go.Pie(labels=qs.bottom().racex,
                                         values=qs.bottom().racey,
                                         marker=dict(colors=['#4F5EFF', '#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF']))],
                            layout=go.Layout(title={
                                'text': 'Race',
                                'x': 0.49,
                                'y': 0.80

                            }, height=330, autosize=True)))
                ], style={'display': 'block', 'textAlign': 'center'}),

                html.Div(className='sprachePie', children=[
                    dcc.Graph(
                        id='diagramm-sprachepie',
                        figure=go.Figure(
                            data=[go.Pie(labels=qs.bottom().sprachex,
                                         values=qs.bottom().sprachey,
                                         marker=dict(colors=['#4F5EFF', ' #5CABFF', '#37E7FF']))],
                            layout=go.Layout(title='Language',
                                             legend={"x": 0.49, "y": 0.80}, height=330)))
                ], style={'display': 'block', 'textAlign': 'center', }),

            ]),

            html.Div(className='Search', children=html.Div()),
            # html.Div(className='Navigation', children=html.Div()),
            html.Div(className='Types', children=[html.H1("Types", style={"font-size" : '30px', 'color' : '#4875E8', 'margin-left' : '10px'}),
                                                  dcc.Checklist(
                                                      id='checklistAge',
                                                      options=[{'label': 'Age', 'value': 'on'}],
                                                      values=['on']),
                                                  dcc.Checklist(
                                                      id='checklistSd',
                                                      options=[{'label': 'Secondary Diagnosis', 'value': 'on'}],
                                                      values=['on']),
                                                  dcc.Checklist(
                                                      id='checklistGender',
                                                      options=[{'label': 'Gender', 'value': 'on'}],
                                                      values=['on']),
                                                  dcc.Checklist(
                                                      id='checklistRace',
                                                      options=[{'label': 'Race', 'value': 'on'}],
                                                      values=['on']),
                                                  dcc.Checklist(
                                                      id='checklistSprache',
                                                      options=[{'label': 'Language', 'value': 'on'}],
                                                      values=['on']),

                                                  ]),

        ], style={'font-size': '20px'}),
    ]),
])


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


@app.callback(
    Output(component_id='diagramm-alter', component_property='style'),
    [Input(component_id='checklistAge', component_property='values')])
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


@app.callback(Output('search-input', 'value'), [Input('reset', 'n_clicks')])
def reset_input(n_clicks):
    if (n_clicks is not None):
        return ""


@app.callback(Output(component_id='upload-data', component_property='value'),
              [Input(component_id='add', component_property='n_clicks')],
              [State(component_id='sunburst', component_property='selectedPath'),
               State(component_id='upload-data', component_property='value')])
def kriterium_sunburst_adden(n_clicks, selectedPath, value_vorher):
    if value_vorher:
        return f"""{value_vorher} AND {selectedPath[-1]}"""
    elif selectedPath:
        return selectedPath[-1]


@app.callback([Output(component_id='count', component_property='children'),
               Output(component_id='count2', component_property='children'),
               Output(component_id='sex', component_property='figure'),
               Output(component_id='age', component_property='figure'),
               Output(component_id='diagramm-alter', component_property='figure'),
               Output(component_id='diagramm-geschlecht', component_property='figure'),
               Output(component_id='diagramm-sd', component_property='figure'),
               Output(component_id='diagramm-racepie', component_property='figure'),
               Output(component_id='diagramm-sprachepie', component_property='figure')
               ],
              [Input(component_id='upload-data', component_property='value')])
def update_graphs(abfrage):
    print(abfrage)
    qs = querystack.Querystack.getInstance()
    if abfrage:

        try:
            kh.Kohortenabfrage.umwandeln_in_fullname(abfrage=abfrage, baum=baum1)

        except IndexError:
            return ('Ungültige Eingabe. Ergebnisse sind von vorheriger Abfrage'), \
                   {'data': [go.Pie(labels=['Male', 'Female'],
                                    values=qs.peek().geschlecht_value_counts,
                                    marker=dict(colors=['#5CABFF', '#4875E8']))],
                    'layout': go.Layout(title={
                        'text': 'Gender',
                        'x': 0.49,
                        'y': 0.75

                    }, height=300)}, \
                   {'data': [go.Bar(x=qs.peek().x_achse_altersverteilung,
                                    y=qs.peek().y_achse_altersverteilung,
                                    text=qs.peek().y_achse_altersverteilung,
                                    textposition='auto',
                                    hoverinfo='none',
                                    marker=dict(
                                        color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF',
                                               '#8093E8', '#9998FF', '#957CEB', '#BE8CFF'])
                                    )],
                    'layout': go.Layout(title={
                        'text': 'Age',
                        'x': 0.49,
                        'y': 0.70

                    }, height=300, xaxis=dict(title='Age groups'),
                        yaxis=dict(title='Number of patients'))

                    }, \
                   {'data': [go.Bar(x=qs.peek().x_achse_altersverteilung,
                                    y=qs.peek().y_achse_altersverteilung,
                                    text=qs.peek().y_achse_altersverteilung,
                                    textposition='auto',
                                    hoverinfo='none',
                                    marker=dict(
                                        color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF',
                                               '#8093E8', '#9998FF', '#957CEB', '#BE8CFF'])
                                    )],
                    'layout': go.Layout(title='Age', xaxis=dict(title='Age groups'),
                                        yaxis=dict(title='Number of patients'))}, \
                   {'data': [go.Pie(labels=['Male', 'Female'],
                                    values=qs.peek().geschlecht_value_counts,
                                    marker=dict(colors=['#5CABFF', '#4875E8']))],
                    'layout': go.Layout(title='Gender', legend={"x": 1, "y": 0.7})
                    }, \
                   {'data': [go.Bar(x=qs.peek().nd_prozent_value_list,
                                    y=qs.peek().nd_diagnose_value_list,
                                    text=qs.peek().nd_prozent_value_list,
                                    textposition='auto',
                                    hoverinfo='none',
                                    orientation='h',
                                    marker=dict(
                                        color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF',
                                               '#8093E8', '#9998FF', '#957CEB', '#BE8CFF']))],
                    'layout': go.Layout(title='Secondary Diagnosis', xaxis=dict(title='Number of patients in %'), margin=go.layout.Margin(l=400, r= 20),
                                        yaxis=go.layout.YAxis(automargin=True, autorange="reversed", ))
                    }, \
                   {'data': [go.Pie(labels=qs.peek().racex,
                                    values=qs.peek().racey,
                                    marker=dict(colors=['#4F5EFF', '#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF']))],
                    'layout': go.Layout(title='Race', legend={"x": 1, "y": 0.7})
                    }, \
                   {'data': [go.Pie(labels=qs.peek().sprachex,
                                    values=qs.peek().sprachey,
                                    marker=dict(colors=['#4F5EFF', ' #5CABFF', '#37E7FF']))],
                    'layout': go.Layout(title='Language',
                                        legend={"x": 1.2, "y": 0.7})
                    }
        return ('Count: ', qs.peek().kohortengröße, ' (', qs.peek().kohortengröße_prozent, '%)'), \
               ('Count: ', qs.peek().kohortengröße, ' (', qs.peek().kohortengröße_prozent, '%)'), \
               {'data': [go.Pie(labels=['Male', 'Female'],
                                values=qs.peek().geschlecht_value_counts,
                                marker=dict(colors=['#5CABFF', ' #4875E8']))],
                'layout': go.Layout(title={
                    'text': 'Gender',
                    'x': 0.49,
                    'y': 0.75

                }, height=300)}, \
               {'data': [go.Bar(x=qs.peek().x_achse_altersverteilung,
                                y=qs.peek().y_achse_altersverteilung,
                                text=qs.peek().y_achse_altersverteilung,
                                textposition='auto',
                                hoverinfo='none',
                                marker=dict(
                                    color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF', '#8093E8',
                                           '#9998FF', '#957CEB', '#BE8CFF'])
                                )],
                'layout': go.Layout(title={
                    'text': 'Age',
                    'x': 0.49,
                    'y': 0.70

                }, height=300, xaxis=dict(title='Age groups'),
                    yaxis=dict(title='Number of patients'))

                }, \
               {'data': [go.Bar(x=qs.peek().x_achse_altersverteilung,
                                y=qs.peek().y_achse_altersverteilung,
                                text=qs.peek().y_achse_altersverteilung,
                                textposition='auto',
                                hoverinfo='none',
                                marker=dict(
                                    color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF', '#8093E8',
                                           '#9998FF', '#957CEB', '#BE8CFF'])
                                )],
                'layout': go.Layout(title='Age', xaxis=dict(title='Age groups'),
                                    yaxis=dict(title='Number of patients'))}, \
               {'data': [go.Pie(labels=['Male', 'Female'],
                                values=qs.peek().geschlecht_value_counts,
                                marker=dict(colors=['#5CABFF', ' #4875E8']))],
                'layout': go.Layout(title='Gender', legend={"x": 1, "y": 0.7})
                }, \
               {'data': [go.Bar(x=qs.peek().nd_prozent_value_list,
                                y=qs.peek().nd_diagnose_value_list,
                                text=qs.peek().nd_prozent_value_list,
                                textposition='auto',
                                hoverinfo='none',
                                orientation='h',
                                marker=dict(
                                    color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF', '#8093E8',
                                           '#9998FF', '#957CEB', '#BE8CFF']))],
                'layout': go.Layout(title='Secondary Diagnosis', xaxis=dict(title='Number of patients in %'),margin=go.layout.Margin(l=400, r= 20),
                                    yaxis=go.layout.YAxis(automargin=True, autorange="reversed", ))
                }, \
               {'data': [go.Pie(labels=qs.peek().racex,
                                values=qs.peek().racey,
                                marker=dict(colors=['#4F5EFF', '#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF']))],
                'layout': go.Layout(title='Race', legend={"x": 1, "y": 0.7})
                }, \
               {'data': [go.Pie(labels=qs.peek().sprachex,
                                values=qs.peek().sprachey,
                                marker=dict(colors=['#4F5EFF', ' #5CABFF', '#37E7FF']))],
                'layout': go.Layout(title='Language',
                                    legend={"x": 1, "y": 0.7})
                }

    return ('Count: ', qs.bottom().kohortengröße, ' (', qs.bottom().kohortengröße_prozent, '%)'), \
           ('Count: ', qs.peek().kohortengröße, ' (', qs.peek().kohortengröße_prozent, '%)'), \
           {
        'data': [go.Pie(labels=['Male', 'Female'],
                        values=qs.bottom().geschlecht_value_counts,
                        marker=dict(colors=['#5CABFF', ' #4875E8']))],
        'layout': go.Layout(title={
            'text': 'Gender',
            'x': 0.49,
            'y': 0.75

        }, height=300)}, \
           {'data': [go.Bar(x=qs.bottom().x_achse_altersverteilung,
                            y=qs.bottom().y_achse_altersverteilung,
                            text=qs.bottom().y_achse_altersverteilung,
                            textposition='auto',
                            marker=dict(
                                color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF', '#8093E8',
                                       '#9998FF', '#957CEB', '#BE8CFF'])
                            )],
            'layout': go.Layout(title={
                'text': 'Age',
                'x': 0.49,
                'y': 0.70

            }, height=300, xaxis=dict(title='Age groups'),
                yaxis=dict(title='Number of patients'))

            }, \
           {'data': [go.Bar(x=qs.bottom().x_achse_altersverteilung,
                            y=qs.bottom().y_achse_altersverteilung,
                            text=qs.bottom().y_achse_altersverteilung,
                            textposition='auto',
                            marker=dict(
                                color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF', '#8093E8',
                                       '#9998FF', '#957CEB', '#BE8CFF'])
                            )],
            'layout': go.Layout(title='Age', xaxis=dict(title='Age groups'),
                                yaxis=dict(title='Number of patients'))}, \
           {'data': [go.Pie(labels=['Male', 'Female'],
                            values=qs.bottom().geschlecht_value_counts,
                            marker=dict(colors=['#5CABFF', ' #4875E8']))],
            'layout': go.Layout(title='Gender', legend={"x": 1, "y": 0.7})
            }, \
           {'data': [go.Bar(x=qs.bottom().nd_prozent_value_list,
                            y=qs.bottom().nd_diagnose_value_list,
                            text=qs.bottom().nd_prozent_value_list,
                            textposition='outside',
                            orientation='h',
                            marker=dict(
                                color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF', '#8093E8',
                                       '#9998FF', '#957CEB', '#BE8CFF']))],
            'layout': go.Layout(title='Secondary Diagnosis', xaxis=dict(title='Number of patients in %'),margin=go.layout.Margin(l=400, r= 20),
                                yaxis=go.layout.YAxis(automargin=True, autorange="reversed",
                                                      ))}, \
           {'data': [go.Pie(labels=qs.bottom().racex,
                            values=qs.bottom().racey,
                            marker=dict(colors=['#4F5EFF', '#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF']))],
            'layout': go.Layout(title='Race',  legend={"x": 1, "y": 0.7})
            }, \
           {'data': [go.Pie(labels=qs.bottom().sprachex,
                            values=qs.bottom().sprachey,
                            marker=dict(colors=['#4F5EFF', ' #5CABFF', '#37E7FF']))],
            'layout': go.Layout(title='Language',
                                legend={"x": 1
                                    , "y": 0.7})
            }


if __name__ == '__main__':
    app.run_server(debug=False)