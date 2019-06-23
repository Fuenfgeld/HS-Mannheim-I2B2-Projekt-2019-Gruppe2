import plotly.graph_objs as go
from logik import querystack
qs = querystack.Querystack.getInstance()
def builder_error():
    return ('Ungültige Eingabe. Ergebnisse sind von vorheriger Abfrage'), \
           ('Count: ', qs.peek().kohortengröße, ' (', qs.peek().kohortengröße_prozent, '%)'), \
           ('Count: ', qs.peek().kohortengröße, ' (', qs.peek().kohortengröße_prozent, '%)'), \
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
            'layout': go.Layout(title='Secondary Diagnosis', xaxis=dict(title='Number of patients in %'),
                                margin=go.layout.Margin(l=400, r=20),
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

def builder_peek():
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
           'layout': go.Layout(title='Secondary Diagnosis', xaxis=dict(title='Number of patients in %'),
                               margin=go.layout.Margin(l=400, r=20),
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

def builder_bottom():
    return ('Count: ', qs.bottom().kohortengröße, ' (', qs.bottom().kohortengröße_prozent, '%)'), \
           ('Count: ', qs.bottom().kohortengröße, ' (', qs.peek().kohortengröße_prozent, '%)'), \
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
           {'data': [go.Bar(x=qs.bottom().x_achse_altersverteilung,
                            y=qs.bottom().y_achse_altersverteilung,
                            text=qs.bottom().y_achse_altersverteilung,
                            textposition='auto',
                            hoverinfo='none',
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
                            textposition='auto',
                            hoverinfo='none',
                            orientation='h',
                            marker=dict(
                                color=['#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF', '#8BCAF5', '#75AAFF', '#8093E8',
                                       '#9998FF', '#957CEB', '#BE8CFF']))],
            'layout': go.Layout(title='Secondary Diagnosis', xaxis=dict(title='Number of patients in %'),
                                margin=go.layout.Margin(l=400, r=20),
                                yaxis=go.layout.YAxis(automargin=True, autorange="reversed",
                                                      ))}, \
           {'data': [go.Pie(labels=qs.bottom().racex,
                            values=qs.bottom().racey,
                            marker=dict(colors=['#4F5EFF', '#4875E8', ' #5CABFF', '#48B5E8', '#37E7FF']))],
            'layout': go.Layout(title='Race', legend={"x": 1, "y": 0.7})
            }, \
           {'data': [go.Pie(labels=qs.bottom().sprachex,
                            values=qs.bottom().sprachey,
                            marker=dict(colors=['#4F5EFF', ' #5CABFF', '#37E7FF']))],
            'layout': go.Layout(title='Language',
                                legend={"x": 1
                                    , "y": 0.7})
            }

