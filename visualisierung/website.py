import dash
import dash_html_components as html
import dash_core_components as dcc
from dash_sunburst import Sunburst
from datenhaltung import connection as connect
import plotly.graph_objs as go
from dash.dependencies import Input, Output
from logik import kohortenabfrage as kh


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

#sunburst_data = baum1

app.layout = html.Div([

html.Div(className="drop",
                     style={'height' : '60px', 'width' : '100%', 'border-style': 'dashed', 'line-height' : '60px', 'text-align' : 'center', 'margin' : '10px', 'border-width' : '1px', 'border-radius' : '5px', 'border-color' : 'blue', 'fonz-size' : '20px' }),
    html.Div(className='Navigation', style={'text-align': 'left', 'position': 'absolute', 'top': '160px'},
             children=html.Div(className='container', id='jstree-tree')),
    dcc.Tabs(className= 'Tabs', id='tabs', children=[
        dcc.Tab( label='Navigation', children=[
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
                     children=html.Div(children=Sunburst(id='sunburst', data=create_data_from_node([]), height=800, width=800, selectedPath =[]),
                                       style={'position': 'absolute', 'margin-top': '100px'}), ),

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
                                         textposition = 'auto',
                                        )],
                            layout=go.Layout(title= {
                                   'text':  'Age',
                                     'x': 0.49,
                                     'y': 0.70

                                 }, height=300, xaxis=dict( title='Age groups'), yaxis=dict( title='Number of patients'))))
                ]),
           html.Div(className='Save_Load', children=[
                html.Button(id='save', className='Save', children=['Save']),
               html.Button(id='load', className='Load', children='Load')
            ])
       ], style={'font-size': '20px', }
                  ),
        dcc.Tab(className='TabDia', label='Diagram', children=[
            html.Div(className='Dia', children=[
                # Create Div to place a conditionally visible element inside
                #html.Div([
                   # dcc.Graph(
                       # id='diagramm-alter',
                        #figure={'data': [{'x': kh.frage_test.x_achse_altersverteilung,
                                     #     'y': kh.frage_test.y_achse_altersverteilung,
                                     #     'text': kh.frage_test.y_achse_altersverteilung,
                                     #     'textposition': 'outside',
                                     #     'type': 'bar'}],
                              #  'layout': {'title': 'Age'
                                     #      }}),

                    html.Div( [
                    dcc.Graph(
                        id='diagramm-alter',
                        figure=go.Figure(
                            data=[go.Bar (x = kh.frage1.x_achse_altersverteilung,
                                         y = kh.frage1.y_achse_altersverteilung,
                                        text=kh.frage1.y_achse_altersverteilung,
                                         textposition = 'auto',
                                        )],
                            layout=go.Layout(title='Age', xaxis=dict( title='Age groups'), yaxis=dict( title='Number of patients'))))
                ], style={'display': 'block'}),


                html.Div(className = 'GeschlechtDia', children = [
                dcc.Graph(
                    id='diagramm-geschlecht',
                    figure=go.Figure(
                        data=[go.Pie(labels=['Male', 'Female'],
                                     values=kh.frage1.geschlecht_value_counts)],
                        layout=go.Layout(title='Gender', margin={"l": 300, "r": 300} ,legend={"x": 0.9, "y": 0.7})))
            ], style={'display': 'block', 'textAlign': 'center'}),

                html.Div([
                    dcc.Graph(
                        id='diagramm-sd',
                        figure=go.Figure(
                            data=[go.Bar (x = kh.frage1.nd_prozent_value_list,
                                         y = kh.frage1.nd_diagnose_value_list,
                                        text=kh.frage1.nd_prozent_value_list,
                                         textposition = 'outside',
                                          orientation = 'h',)],
                            layout=go.Layout(title='Secondary Diagnosis', xaxis=dict( title='Number of patients in %'), yaxis=go.layout.YAxis(automargin=True, autorange="reversed",
        ))))
                ], style={'display': 'block'}),

                #   html.Div([
                 #   dcc.Graph(
                   #     id='diagramm-sprache',
                    #    figure={'data': [{'x': sprachex,
                         #                 'y': sprachey,
                         #                 'text': sprachey,
                         #                 'textposition': 'outside',
                         #                 'type': 'bar'}],
                         #       'layout': {'title': 'Language'
           #                                }})
            #    ], style={'display': 'block'}  # <-- This is the line that will be changed by the checklist callback
             #   ),

              #  html.Div([
               #    dcc.Graph(
                #        id='diagramm-race',
                 #       figure={'data': [{'x': racex,
                  #                        'y': racey,
                   #                       'text': racey,
                    #                      'textposition': 'outside',
                     #                     'type': 'bar'}],
                      #          'layout': {'title': 'Race'
        #                                   }})
         #       ], style={'display': 'block'}  # <-- This is the line that will be changed by the checklist callback
          #      ),

                html.Div(className = 'race', children = [
                dcc.Graph(
                    id='diagramm-racepie',
                    figure=go.Figure(
                        data=[go.Pie(labels= kh.frage1.racex,
                                     values=kh.frage1.racey)],
                        layout=go.Layout(title='Race', margin={"l": 300, "r": 300},legend={"x": 0.9, "y": 0.7})))
            ], style={'display': 'block', 'textAlign': 'center'}),

                html.Div(className = 'sprache', children = [
                    dcc.Graph(
                        id='diagramm-sprachepie',
                        figure=go.Figure(
                            data=[go.Pie(labels=kh.frage1.sprachex,
                                         values=kh.frage1.sprachey)],
                            layout=go.Layout(title='Language', margin={"l": 300, "r": 300}, legend={"x": 0.9, "y": 0.7})))
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


# @app.callback(Output('output-data-upload', component_property='children'),
#               [Input('upload-data', 'contents')])
# def update_output(list_of_contents):
#     if list_of_contents is not None:
#         children = 'Hallo!'
#         return children


if __name__ == '__main__':
    app.run_server(debug=False)