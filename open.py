import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

import dash
import dash_core_components as dcc
import dash_html_components as html
from dash.dependencies import Input, Output

filename = '15-8-2018--8-44.csv'

flight = pd.read_csv(filename)

print(list(flight))

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
df.head()

lat = flight['Latitude (Degrees)'].values
lon = flight['Longitude (Degrees)'].values
alt = flight['Altitude GPS'].values

#mapbox_access_token = 'pk.eyJ1IjoiZjMxMTU5ODIiLCJhIjoiY2pteDUyY3RpMHE5cDNwcXZvM211MmtveCJ9.qecPblbn_ChwDrcJGlwnrg'
mapbox_access_token = 'pk.eyJ1IjoiZjM4MTA4MTkiLCJhIjoiY2pteWl6eXMwMXhsdTNwbzhpcDZkZzYwNCJ9.DYWpw7DRbNpNpe1nkr6qLw'

mapdata = [
    go.Scattermapbox(
        lat=lat,
        lon=lon,
        mode='markers',
        marker=dict(
            size=7
        ),
        text=alt,
        hoverinfo='text',
    )
]

def find_center_plot(lon,lat):
    center_lon = (max(lon)+min(lon))/2
    center_lat = (min(lat)+max(lat))/2
    print("center lon %f, max lon %f, first lon %f"%(center_lon, max(lon), lon[0]))
    return dict(lon=center_lon,lat=center_lat)

def find_zoom(flight):
    return (3.*flight['Distance From Start (straight line)'].values[-1])

maplayout = go.Layout(
    autosize=True,
    hovermode='closest',
    mapbox=dict(
        accesstoken=mapbox_access_token,
        bearing=0,
        center=find_center_plot(lon,lat),
        pitch=0,
        zoom=find_zoom(flight),
        style='mapbox://styles/f3810819/cjmyj0cf62ojr2rjmlk9iv859',
    ),
    margin=go.Margin(
        l=0,
        r=0,
        b=00,
        t=00,
    )
)

mapfig = dict(data=mapdata, layout=maplayout)

#py.iplot(fig, filename='Montreal Mapbox')

#### Altitude / Speed plots
plotdata = go.Scatter(
        x=flight['Datetime (UTC)'],
        y=flight['Altitude GPS'],
       ) 

## 


app = dash.Dash()

def create_dropdown(flight):
    retlist = []
    for i in list(flight):
        retlist.append({'label':i,'value':i})
    return retlist

app.layout = html.Div([
    dcc.Graph(
        id='my-map',
	figure=mapfig,
    ),
    dcc.Dropdown(
        id='my-dropdown',
        options=create_dropdown(flight),
        value='Altitude GPS',
    ),
    dcc.Graph(id='my-graph'),
])

print("coucou")

@app.callback(Output('my-graph','figure'), [Input('my-dropdown', 'value')])
def update_graph(selected_dropdown_value):
    return {
        'data': [{
            'x': flight['Elapsed Time'].values,
            'y': flight[selected_dropdown_value].values,
        }],
    	'margin' : [{
        'l':0,
        'r':0,
        'b':0,
        't':0,
    	}],
    }

if __name__ == '__main__':
    app.run_server(debug=True)
