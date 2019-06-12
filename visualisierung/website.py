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
from logik import Kohortenabfrage as kh
import pandas as pd

#dnd

external_stylesheets = ['https://codepen.io/chriddyp/pen/bWLwgP.css']

connection = connect.create_connection()
baum1 = tie.treedictionary_aus_pickle_importieren('baum_mit_var_text')
df = log.all_patients()



wurzel=baum1.knotenliste_mit_baum[0][0]

def create_data_from_node(path):

    if (path==[]) :
        data = {
            'name' : wurzel.text,
            'children' : [{
                'name' : i.text,
                'size' : i.size,
               # 'children':[{
                #   'name' : j.text,
                #   'size' : j.size
              #  }for j in i.children] #Dieser Bereich könnte einen weiteren äußeren Ring hinzufürgen
            }for i in wurzel.children]
        }

    else :
        index=0
        #print('Angeklickt' +str(path[-1]))
        #print(len(path))
        while baum1.knotenliste_mit_baum[len(path)][index].text != path[-1]:
        #    print(baum.knotenliste_mit_baum[len(path)][index].text)

            index+=1;
        zwischenwurzel=baum1.knotenliste_mit_baum[len(path)][index]


        if not zwischenwurzel.children:

            data = {
                'name' : zwischenwurzel.text,
                'size' : zwischenwurzel.size

            }

        else:
            data = {
                'name' : zwischenwurzel.text,
                'children' : [{
                    'name' : i.text,
                    'size' : i.size,
                   # 'children': [{
                    #   'name': j.text,
                    #    'size': j.size
                   # }for j in i.children]#Dieser Bereich könnte eine zweiten äußeren Ring realisieren

                }for i in zwischenwurzel.children]
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



app = dash.Dash('__name__',
                external_stylesheets=['https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css',
                                      'https://static.jstree.com/3.0.9/assets/dist/themes/default/style.min.css',

                                      ],

                external_scripts=['http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js',
                                  'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.0.9/jstree.min.js',

                                  ])
app.scripts.config.serve_locally = True
app.css.config.serve_locally = True

#sunburst_data = baum1

app.layout = html.Div([

html.Div(className="drop",
                     style={'height' : '60px', 'width' : '100%', 'border-style': 'dashed', 'line-height' : '60px', 'text-align' : 'center', 'margin' : '10px', 'border-width' : '1px', 'border-radius' : '5px', 'border-color' : 'blue', 'fonz-size' : '20px' }),
    html.Div(className='Navigation', style={'text-align': 'left', 'position': 'absolute', 'top': '160px'},
             children=html.Div(className='container', id='jstree-tree')),

html.Div( html.Button('Save', id='save')
            ),

html.Div(html.Button('Load', id='load'),
            ),

html.Div(html.Button('Run',id='run'),
),

    dcc.Tabs(className= 'Tabs', id='tabs', children=[
        dcc.Tab( label='Navigation', children=[
            html.Div(className='Sunburst',
                     children=html.Div(children=Sunburst(id='sunburst', data=create_data_from_node([]), height=650, width=600, selectedPath =[]),
                                       style={'position': 'absolute', 'top': '175px', 'left': '670px'}), ),
            html.Div (className='path',id='output'),
            html.Div(className='Search', children=
            dcc.Input(
                id="search-input",
                placeholder='Search',
                type='text',
                style={'textAlign': 'center'},
            )),
            html.Div(className='Navigation', children=html.Div()),
            html.Div(className='NumberOfPatients', children=['Number of patients: ', kh.frage1.kohortengröße]),
            html.Div(className='NavSex',
                     children=[
                         dcc.Graph(
                             id='sex',
                             figure=go.Figure(
                                 data=[go.Pie(labels=['Male', 'Female'],
                                              values=kh.frage1.geschlecht_value_counts)],
                                 layout=go.Layout(title= {
                                   'text':  'Gender',
                                     'x': 0.49,
                                     'y': 0.75

                                 }, height=300)))
                     ]),
            html.Div(className='NavAge',
                     children=[
                    dcc.Graph(
                        id='id',
                        figure=go.Figure(
                            data=[go.Bar (x = kh.frage1.x_achse_altersverteilung,
                                         y = kh.frage1.y_achse_altersverteilung,
                                        text=kh.frage1.y_achse_altersverteilung,
                                         textposition = 'inside',
                                        )],
                            layout=go.Layout(title= {
                                   'text':  'Age',
                                     'x': 0.49,
                                     'y': 0.70

                                 }, height=300, xaxis=dict( title='Age groups'), yaxis=dict( title='Number of patients'))))
                ]),

       ], style={'font-size': '20px', }
                  ),
        dcc.Tab(className='TabDia', label='Diagram', children=[
            html.Div(className='DiaBar', children=[


                html.Div(children=['Number of patients: ', kh.frage1.kohortengröße]),

                 html.Div(className = 'alterBar', children =[
                    dcc.Graph(
                        id='diagramm-alter',
                        figure=go.Figure(
                            data=[go.Bar (x = kh.frage1.x_achse_altersverteilung,
                                         y = kh.frage1.y_achse_altersverteilung,
                                        text=kh.frage1.y_achse_altersverteilung,
                                         textposition = 'inside',
                                        )],
                            layout=go.Layout(title= {
                                   'text':  'Age',
                                     'x': 0.49,
                                     'y': 0.85

                                 },  xaxis=dict( title='Age groups'), yaxis=dict( title='Number of patients'))))
                ], style={'display': 'block'}),


                html.Div(className = 'sdBar', children =[

                    dcc.Graph(
                        id='diagramm-sd',
                        figure=go.Figure(
                            data=[go.Bar (x = kh.frage1.nd_prozent_value_list,
                                         y = kh.frage1.nd_diagnose_value_list,
                                        text=kh.frage1.nd_prozent_value_list,
                                         textposition = 'outside',
                                          orientation = 'h',)],
                            layout=go.Layout(title= {
                                   'text':  'Secondary Diagnosis',
                                     'x': 0.49,
                                     'y': 0.85

                                 } , xaxis=dict( title='Number of patients in %'), margin=go.layout.Margin(l=400, r= 20

    ), yaxis=go.layout.YAxis(automargin=True, autorange="reversed")
                            )))
                ], style={'display': 'block'}),
            ]),


            html.Div(className='DiaPie', children=[

                html.Div(className = 'genderPie', children = [
                dcc.Graph(
                    id='diagramm-geschlecht',
                    figure=go.Figure(
                        data=[go.Pie(labels=['Male', 'Female'],
                                     values=kh.frage1.geschlecht_value_counts)],
                        layout=go.Layout(title= {
                                   'text':  'Gender',
                                     'x': 0.49,
                                     'y': 0.80

                                 },height = 330)))
            ], style={'display': 'block', 'textAlign': 'center'}),

            html.Div(className = 'racePie', children = [
                dcc.Graph(
                    id='diagramm-racepie',
                    figure=go.Figure(
                        data=[go.Pie(labels= kh.frage1.racex,
                                     values=kh.frage1.racey)],
                        layout=go.Layout(title= {
                                   'text':  'Race',
                                     'x': 0.49,
                                     'y': 0.80

                                 },height = 330, autosize = True)))
            ], style={'display': 'block', 'textAlign': 'center'}),

            html.Div(className = 'sprachePie', children = [
                    dcc.Graph(
                        id='diagramm-sprachepie',
                        figure=go.Figure(
                            data=[go.Pie(labels=kh.frage1.sprachex,
                                         values=kh.frage1.sprachey)],
                            layout=go.Layout(title= {
                                   'text':  'Language',
                                     'x': 0.49,
                                     'y': 0.80

                                 }, height = 330)))
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


# @app.callback(Output('output-data-upload', component_property='children'),
#               [Input('upload-data', 'contents')])
# def update_output(list_of_contents):
#     if list_of_contents is not None:
#         children = 'Hallo!'
#         return children


if __name__ == '__main__':
    app.run_server(debug=False)