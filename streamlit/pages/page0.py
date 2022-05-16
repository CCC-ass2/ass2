import pandas as pd
import plotly.express as px


token = 'pk.eyJ1IjoieWl4bGl1MSIsImEiOiJjbDJlbWdqZGowMjJnM2lwZ3hmNW13cXR5In0.U-oj9FlxDNa-PsCr45ygrQ'
df = pd.read_excel('data/page0.xlsx')


def map_plot():
    px.set_mapbox_access_token(token)
    fig = px.scatter_mapbox(df, lat="lat", lon="lon", size="tweet",
                            size_max=65, zoom=10, color_discrete_sequence=['#CD853F'])
    fig.update_layout(mapbox_style="light", mapbox_accesstoken=token,
                      mapbox_zoom=3.3, mapbox_center={"lat": -32.6980, "lon": 155.8807})
    style2 = ["open-street-map", "carto-positron", "carto-darkmatter", "stamen-terrain", "stamen-toner",
              "stamen-watercolor"]
    fig.update_layout(mapbox_style="open-street-map", mapbox_accesstoken=token)
    fig.update_layout(margin={"r": 0, "t": 0, "l": 0, "b": 0}, height=700, width=1400)
    return fig