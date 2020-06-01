import json
import pandas as pd
import numpy as np
import base64
import dash_html_components as html
import dash_bootstrap_components as dbc
import dash_core_components as dcc
import plotly.graph_objects as go
import plotly.figure_factory as ff
import dash


df = pd.read_csv("pts.hds.1D.csv",dtype={"node": str})
with open("pts.hds.1d.json") as geofile:
    geojson = json.load(geofile)
    i=1
i = 1

for feature in geojson["features"]:
    feature['id'] = str(i)
    i += 1
df['node'] = df['node'].astype(str)

times = df['time'].unique()
time = 1.0
temp_df = df.loc[df['time'] == time]

data = [dict(
            type='choropleth', # type of map-plot
            colorscale = 'jet',
            autocolorscale = False,
            locations = df['node'], # the column with the ID
            z = df['hds'].astype(float), # the variable I want to color-code
            geojson = geojson,
            text = df['hds'], # hover text
            marker = dict(     # for the lines separating states
                        line = dict(
                                  color = 'rgb(255,255,255)',
                                  width = 2) ),              
            colorbar = dict(
                        title = "Head (ft)")
            )
       ]

data_slider = []
for i, time in enumerate(times):
    temp_df = df.loc[df['time'] == time]

    data_slider.append(dict(
            type='choroplethmapbox', # type of map-plot
            colorscale = 'jet',
            autocolorscale = False,
            locations = temp_df['node'], # the column with the ID
            z = temp_df['hds'].astype(float), # the variable I want to color-code
            geojson = geojson,
            text = temp_df['node'], # hover text              
            colorbar = dict(
                        title = "Head (ft)")
            )
       )

layout = dict(
        title = f'Time: {time}',
        geo = dict(
            scope='usa',
            projection=dict( type='albers usa'),
            center=dict(lat=30.2883, lon=-97.7444), 
            ),
             )

steps = []
for i, time in enumerate(times):
    step = dict(method='restyle',
                args=['visible', [False] * len(data_slider)],
                label='Time: {}'.format(time))
    step['args'][1][i] = True
    steps.append(step)

sliders = [dict(active=0,
                pad={"t": 1},
                steps=steps)]    

layout = dict(geo=dict(scope='usa',
                        projection={'type': 'albers usa'},
                        center=dict(lat=30.2883, lon=-97.7444),
                        showrivers=True),
              sliders=sliders
              )
accesstoken = 'pk.eyJ1Ijoicm9zc2t1c2giLCJhIjoiY2thdmhxOW93MmpibzJ3cDE3bnl5NTR5dCJ9.hr8_Nmw9PNvYtRZUcM5UUg'
layout_mapbox = dict(autosize=True,
              mapbox=dict(
                  accesstoken=accesstoken,
                  bearing=0,
                  center=dict(lat=30.2883, lon=-97.7444),
                  pitch=0,
                  style = "carto-positron",
                  zoom=15
                  ),
              sliders=sliders,
              hovermode='closest'
              )

fig = dict(data=data_slider, layout=layout_mapbox)
fig = go.Figure(fig)

##################################################################

external_stylesheets = [dbc.themes.BOOTSTRAP]
image_filename = 'PearlStreetAnalyticsLogo.png' 
encoded_image = base64.b64encode(open(image_filename, 'rb').read())

app = dash.Dash(__name__, external_stylesheets=external_stylesheets)
server = app.server
app.title = "MODFLOW Demo"

app.layout = html.Div([
  dbc.Row([
    dbc.Col(
      html.H2(
        children="Dashboard Example: MODFLOW Model With Time-Slider",
        style={
               "margin-top": 10,
               "margin-left": 10}), 
      width=9),

    dbc.Col(
      html.Img(
          src='data:image/png;base64,{}'.format(encoded_image.decode()),
          style={
              'float': 'right',
              'margin': 10}), 
      width=3)]),

   dbc.Row( 
    dbc.Col(
      dcc.Graph(id="fig",figure=fig), 
      width=12))])

if __name__ == '__main__':
    app.run_server()

