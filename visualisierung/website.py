import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_sunburst import Sunburst
from datenhaltung import connection as connect
import plotly.graph_objs as go
from dash.dependencies import Input, Output, State
from logik import kohortenabfrage as kh
from logik import querystack
from visualisierung import sunburst_limiter as limit
from visualisierung import builder
import tree_dictionary_import_export as tie
from logik import querystack
import visdcc
import pandas as pd
import dash_table

baum1 = tie.treedictionary_aus_pickle_importieren('baum_mit_shortcode')
qs = querystack.Querystack.getInstance()
connection = connect.create_connection()
cur = connection.cursor()
external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']
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
    dcc.ConfirmDialog(
        id='confirm',
        message='Do you want to save this query?',
    ),
    dcc.ConfirmDialog(
        id='saved',
        message='Saved.',
    ),
    visdcc.Run_js(id='runscript'),
    visdcc.Run_js(id='treescript'),
    html.Div(id='aktuellerKnoten', style={'display': 'none'}),
    visdcc.Run_js(id='addscript', run=
    '''var addbutton=document.getElementById('add');
    addbutton.addEventListener('click',inputverändern);

    function inputverändern(){

    var aktuellerKnoten = document.getElementById('aktuellerKnoten').innerHTML;
    //alert(aktuellerKnoten);

    //var selectedPath = document.getElementById('sunburst').selectedPath;
    //alert(selectedPath);

    var bisherigeEingabe = document.getElementById('upload-data').value;

    //if ((/^\s*$/).test(bisherigeEingabe)) {
    //    document.getElementById('upload-data').value=aktuellerKnoten;
    //}


    //alert(document.getElementById('upload-data').value);

    //else{
    document.getElementById('upload-data').value=document.getElementById('upload-data').value+" "+aktuellerKnoten;
    //}



    }



    '''),

    visdcc.Run_js(id='andscript', run=
    '''

    var andbutton = document.getElementById('and');
    andbutton.addEventListener('click',andhinzufügen);

    function andhinzufügen(){
    let bisherigeEingabe = document.getElementById('upload-data').value; 

    document.getElementById('run').focus();
    bisherigeEingabe = document.getElementById('upload-data').value;  
    document.getElementById('upload-data').value=bisherigeEingabe+" AND";

    }
    '''),

    visdcc.Run_js(id='orscript', run='''

        var orbutton = document.getElementById('or');
        orbutton.addEventListener('click',orhinzufügen);

        function orhinzufügen(){
        document.getElementById('run').focus();
        document.getElementById('upload-data').value=document.getElementById('upload-data').value+" OR";
        }
        '''),

    visdcc.Run_js(id='notscript', run='''
        var notbutton = document.getElementById('not');
        notbutton.addEventListener('click',nothinzufügen);

        function nothinzufügen(){
        document.getElementById('run').focus();
        document.getElementById('upload-data').value=document.getElementById('upload-data').value+" NOT";

        }
        '''),

    visdcc.Run_js(id='clearscript', run='''
        var clearbutton= document.getElementById('clear');
        clearbutton.addEventListener('click',clearall);

        function clearall(){
        document.getElementById('upload-data').value='';
        }

        '''),

    dcc.Input(className="drop", id="upload-data",
              ),

    dcc.Input(
            id="search-input",
            className='search-input',
            type='text',

        ),

    html.Div(html.Button(className = 'button-search', id ='search' )
             ),

    html.Div(html.Button(className="buttonClear", id='clear'),
             ),

    html.Div(html.Button(className="button-reset", id ='reset'),
             ),

    html.Div(className='Tree',
             children=html.Div(className='container', id='jstree-tree')),

    html.Div(html.Button(id='save')
             ),

    html.Div(html.Button(id='load'),
             ),

    html.Div(html.Button(id='run'),
             ),
html.Div(html.Button('AND', className="and", id='and'),

             ),
html.Div(html.Button('OR', className="or", id='or'),
             ),
html.Div(html.Button('NOT', className="not", id='not'),
             ),


    dcc.Tabs(className='Tabs', id='tabs', children=[
        dcc.Tab(label='Navigation', children=[
            html.Div(className='Sunburst',
                     children=html.Div(
                         children=[
                             html.Div(className='path', id='output'),
                             html.Button(
                                 id="add",
                                 # children="add",
                                 className="button-add"
                             ),
                             Sunburst(id='sunburst', data=create_data_from_node([]), height=650, width=800,
                                      selectedPath=[]),

                           html.Div(  dash_table.DataTable(
                                 id='table',
                                 columns=[{"name": "Shortcode", "id": "Shortcode"}, {"name": "Text", "id": "Text"}],
            style_data={'whiteSpace': 'normal'},
            content_style='grow',
            css=[{
                'selector': '.dash-cell div.dash-cell-value',
                'rule': 'display: inline; white-space: inherit; overflow: inherit; text-overflow: inherit;'
            }],
                                style_table={
                                    'width': '100%',
                                    'textAlign': 'left'
                                    },
                               style_cell_conditional=[
                                   {
                                       'textAlign': 'left'
                                   }
                               ]
                           ))],
                         # style={'position': 'relative', 'margin-left': '-30px'
                         #       '', 'margin-top': '-100px'}
                     ), ),

            html.Div(className='Search', children=html.Div()),
            #html.Div(className='Navigation', children=html.Div()),
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
                                              hoverinfo='none',
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

                html.Div(
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
                            layout=go.Layout(title='Secondary Diagnosis', xaxis=dict(title='Number of patients in %'),
                                             margin=go.layout.Margin(l=400, r=20

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
            html.Div(className='Types', children=['Types ',
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

@app.callback(Output('confirm', 'displayed'),
              [Input('save', 'n_clicks')])
def display_confirm(n_clicks):
    if(n_clicks is not None):
        return True
    return False

@app.callback(Output('saved', 'displayed'),
              [Input('confirm', 'submit_n_clicks')])
def display_saved(submit_n_clicks):
    if (submit_n_clicks is not None):
        kriterien_l = qs.peek().kriterien
        kriterien = ','.join(kriterien_l)
        print(kriterien)
        verknüpfungen_l =  qs.peek().verknüpfungen
        verknüpfungen = ','.join(verknüpfungen_l)
        print(verknüpfungen)
        cur.execute(f"""INSERT INTO saved (zeitpunkt, kriterien, verknüpfungen, kohortengröße) VALUES ('{qs.peek().zeitpunkt}' , '{kriterien}', '{verknüpfungen}', {qs.peek().kohortengröße})""")
        connection.commit()
        return True
    return False


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


@app.callback(Output('sunburst', 'data'),
              [Input('sunburst', 'selectedPath')])
def display_sun(selectedPath):
    # print(selectedPath)
    return limit.create_data_from_node(path=selectedPath)


@app.callback(Output('table', 'data'),
              [Input('sunburst', 'selectedPath')])
def update_table(selectedPath):
    print('verändere Tabelle')
    return create_table_from_node(path=selectedPath)


@app.callback([Output('output', 'children'),
               Output('aktuellerKnoten', 'children')],

              [Input('sunburst', 'selectedPath')])
def display_selected(selected_path):
    return 'Path: {}'.format('->'.join(selected_path or []) or 'Diagnoses'), \
           selected_path[-1]

@app.callback(Output(component_id='runscript', component_property='run'),
              [Input(component_id='run', component_property='n_clicks')])
def inputfeld_auslesen(clicks):
    if clicks == 0:
        return ''

    else:

        return '''
        setProps({
        'event':document.getElementById('upload-data').value
        })  
        //alert(document.getElementById('upload-data').value);    
        '''

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
            return builder.builder_error()
        return builder.builder_peek()
    return builder.builder_bottom()

if __name__ == '__main__':
    app.run_server(debug=False)