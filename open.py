import plotly.plotly as py
import plotly.graph_objs as go
import pandas as pd

filename = '15-8-2018--8-44.csv'

flight = pd.read_csv(filename)

print(flight)

df = pd.read_csv('https://raw.githubusercontent.com/plotly/datasets/master/2011_february_us_airport_traffic.csv')
df.head()

print(flight['Latitude (Degrees)'].values)

lat = flight['Latitude (Degrees)'].values
lon = flight['Longitude (Degrees)'].values
alt = flight['Altitude GPS'].values



#mapbox_access_token = 'pk.eyJ1IjoiZjMxMTU5ODIiLCJhIjoiY2pteDUyY3RpMHE5cDNwcXZvM211MmtveCJ9.qecPblbn_ChwDrcJGlwnrg'
mapbox_access_token = 'pk.eyJ1IjoiZjM4MTA4MTkiLCJhIjoiY2pteWl6eXMwMXhsdTNwbzhpcDZkZzYwNCJ9.DYWpw7DRbNpNpe1nkr6qLw'

data = [
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
    return 3.*flight['Distance From Start (straight line)'].values[-1],

layout = go.Layout(
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
)

fig = dict(data=data, layout=layout)

py.iplot(fig, filename='Montreal Mapbox')

