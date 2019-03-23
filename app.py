# -*- coding: utf-8 -*-
import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output
import json
import requests

API_KEY = "e0ccebfd4c07312069ca715fb6edbdb8"

with open('./city.list.json') as f:
    cities = json.load(f)


external_stylesheets = ['https://stackpath.bootstrapcdn.com/bootstrap/4.1.0/css/bootstrap.min.css']

prev_cities = []
prev_data = None

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)

server = app.server


app.layout = html.Div(className="container",children=[

    html.Div(className="row", children=html.H2(children=[
        html.H1(children='Weatherfy'),
        '''
        Weatherfy: Weather visualisation Dash application.
        '''
    ])),

    html.Div(className="row", children=[

        html.Div(className="col-md-3", children=[
            html.Label('Select cities'),
            dcc.Dropdown(
                className="w-100",
                id='cities-dropdown',
                options=[{'label': data["name"], 'value': data['id']} for data in cities],
                value=['6077243'],
                multi=True
            ),

            html.Label('Select metric'),
            dcc.RadioItems(
                id="metric-radio",
                className="form-group",
                value='celsius',
                style=[],
                options=[
                    {'label': u'°C \xA0 \xA0', 'value': 'celsius'},
                    {'label': u'°F ', 'value': 'fahrenheit'},
                ],
            ),

        ]),

        html.Div(className="col-md-9", children=[
            dcc.Graph(id='temperature-graph')

        ])

    ]),

    
])

@app.callback(
    Output('temperature-graph', 'figure'),
    [
        Input('cities-dropdown', 'value'),
        Input('metric-radio', 'value')]
    )
def update_figure(selected_cities, metric):

    celsius = metric == "celsius"
    global prev_data
    global prev_cities
    if (set(selected_cities) != set(prev_cities)):
        prev_data = selected_cities
        payload = {'id': ",".join([str(x) for x in selected_cities]), 'appid': API_KEY, 'units': 'metric'}
        r = requests.get("http://api.openweathermap.org/data/2.5/group", payload)
        prev_data = r.json()["list"]

    return {
        'data': [ 
        {
        'x': [u"Temp (°" + ("C" if celsius else "F") +")"], 
        'y': [(w["main"]["temp"] if celsius else (w["main"]["temp"] * 9/5) + 32)], 
        'hoverinfo': 'text',
        'text': "%.2f °" % (w["main"]["temp"] if celsius else (w["main"]["temp"] * 9/5) + 32) + ("C" if celsius else "F") +"" + "<br>" + w["weather"][0]["description"],
        'type': 'bar', 
        'name': w["name"]}
        for w in prev_data
        ],
        'layout': {
            'title': 'Dash Data Visualization'
        }
    }


if __name__ == '__main__':
    app.run_server(debug=True)