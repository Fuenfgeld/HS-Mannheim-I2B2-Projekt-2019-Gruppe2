import dash
# import dash_core_components as dcc
import dash_html_components as html

#import DB_Queries as db  # import from the file with the database query
# import plotly.graph_objs as go
import row_generator_tables as rg



d = dash
app = d.Dash( __name__,
    external_stylesheets=['https://maxcdn.bootstrapcdn.com/bootstrap/3.3.2/css/bootstrap.min.css',
                          'https://static.jstree.com/3.0.9/assets/dist/themes/default/style.min.css',

                          'assets/style.css'],
    external_scripts=['http://cdnjs.cloudflare.com/ajax/libs/jquery/2.1.3/jquery.min.js',
                      'https://cdnjs.cloudflare.com/ajax/libs/jstree/3.0.9/jstree.min.js',
                      'index.js'
                      ])

app.layout = html.Div([


    html.Div(id="jstree-tree")

], className="container" )



if __name__ == '__main__':
    app.run_server(debug=True)
