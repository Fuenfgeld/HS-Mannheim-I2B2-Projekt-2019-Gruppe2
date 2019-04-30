from django.shortcuts import render
from django.http import HttpResponse
import pandas as pd

# Create your views here.

def index(request):
    return render(
        request,
        "mep/index.html"
        )

def sex(request):
    dataframe = pd.read_csv("beispieldaten_patienten.csv", sep = ";")
    count = dataframe.groupby('Sex').size()
    data = count.tolist()
    labels = ['F', 'M']
    colors = ["#FF4136", "#0074D9"]

    return render(
        request, 
        "mep/chart.html",
        {
            'title' : "Geschlecht",
            'labels': labels,
            'data': data,
            'colors': colors,
            }

        )

def race(request):
    dataframe = pd.read_csv("beispieldaten_patienten.csv", sep = ";")
    count = dataframe.groupby('Race').size()
    data = count.tolist()
    labels = ['asian', 'black', 'hispanic', 'indian', 'white']
    colors = ["#08088A", "#0101DF", "#2E64FE", "#58ACFA", "#A9D0F5"]

    return render(
        request, 
        "mep/chart.html",
        {
            'title' : "Ethnie",
            'labels': labels,
            'data': data,
            'colors': colors,
            }

        )

def nationality(request):
    dataframe = pd.read_csv("beispieldaten_patienten.csv", sep = ";")
    count = dataframe.groupby('Nationality').size()
    data = count.tolist()
    labels = ['english', 'german', 'spanish']
    colors = ["#088A08", "#00FF00", "#A9F5A9"]

    return render(
        request, 
        "mep/chart.html",
        {
            'title' : "Nationalitaet",
            'labels': labels,
            'data': data,
            'colors': colors,
            }

        )

def relationship(request):
    dataframe = pd.read_csv("beispieldaten_patienten.csv", sep = ";")
    count = dataframe.groupby('Relationship status').size()
    data = count.tolist()
    labels = [ 'divorced', 'married', 'single',  'widow']
    colors = ["#8A0808", "#DF0101", "#FA5858", "#F5A9A9"]

    return render(
        request, 
        "mep/chart.html",
        {
            'title' : "Beziehungsstatus",
            'labels': labels,
            'data': data,
            'colors': colors,
            }

        )

def religion(request):
    dataframe = pd.read_csv("beispieldaten_patienten.csv", sep = ";")
    count = dataframe.groupby('Religion').size()
    data = count.tolist()
    labels = ['agnostic', 'atheist', 'christian', 'jewish',  'muslim', 'roman catholic']
    colors = ["#380B61", "#5F04B4", "#4000FF", "#5882FA", "#BCA9F5", "#E6E0F8"]


    return render(
        request, 
        "mep/chart.html",
        {
            'title' : "Religioese Orienterung",
            'labels': labels,
            'data': data,
            'colors': colors,
            }

        )

def income(request):
    dataframe = pd.read_csv("beispieldaten_patienten.csv", sep = ";")
    count = dataframe.groupby('Income').size()
    data = count.tolist()
    labels = ['high', 'low', 'medium']
    colors = ["#FFFF00", "#F3F781", "#F5F6CE"]

    return render(
        request, 
        "mep/chart.html",
        {
            'title' : "Einkommen",
            'labels': labels,
            'data': data,
            'colors': colors,
            }

        )