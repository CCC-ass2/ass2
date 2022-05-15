import streamlit as st
import plotly.graph_objects as go
import os.path
import pandas as pd
from plotly.subplots import make_subplots
import requests
import json

f = open('config.json')
localhost = json.load(f)['IP']

# read in data
fname = "pages/backup_page2/data.json"
if not os.path.isfile(fname):
    r = requests.get(f'http://{localhost}:8000/page2data').json()
    with open(fname, 'w') as fp:
        json.dump(r, fp)
with open(fname, 'rb') as f:
    r = json.load(f)

df = r['top10']
df2 = pd.DataFrame.from_dict(r['twitter_analysis'])


def display():
    st.header('Emoji & Tag Usage')
    st.text('Amount and frequency to use emoji and tags by people in different regions')

    with st.expander("Top 10 Emoji"):
        select = st.selectbox('Select Greater City:', ['Adelaide', 'Brisbane', 'Melbourne', 'Sydney'], index=2)
        col1, col2 = st.columns(2)
        col1.plotly_chart(emo_bar(df, select))

        col2.subheader(f'Top 10 emoji at {select}')
        col2.table(emo_table(df, select))

    with st.expander("Emoji & Tag use in Twitter"):
        st.plotly_chart(twitter_bar(df2))


def emo_bar(df, city):
    df2 = pd.DataFrame(df[city])
    fig = go.Figure([go.Bar(x=df2['emoji'], y=df2["freq"],
                            marker_color=['#c5a8d2', '#dcb1c9', '#EEB9BD', '#EDB9BD', '#FAD2D2', '#E5CFD1', '#C4CAD6', '#97ABBF', '#8393B4', '#8391A7'])])
    fig.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                      xaxis_title="Emoji",
                      yaxis_title="Frequency",
                      title=f"Top 10 emoji at {city}",
                      font=dict(size=18),
                      height=500, width=500)
    return fig

def emo_table(df, city):
    ddf = pd.DataFrame(df[city])
    ddf.insert(0, 'Top #', range(1, len(ddf)+1))
    return ddf

def twitter_bar(df2):
    fig = make_subplots(
        rows=2, cols=2,
        subplot_titles=("Total number of twitters", "Word Length per twitter", "Emoji Frequency per twitter", "Tag Frequency per twitter"), )

    text = [str(i) for i in df2['Number of twitters']]
    fig.add_trace(go.Scatter(x=df2['City'], y=df2['Number of twitters'], mode="lines+text", text=text, marker_color='#90bc8c'), row=1, col=1)
    fig.add_trace(go.Scatter(x=df2['City'], y=df2['Word Length'], mode="lines+text", text=text, marker_color='#90bc8c'), row=1, col=2)
    fig.add_trace(go.Scatter(x=df2['City'], y=df2['Emoji Frequency'], mode="lines+text", text=text, marker_color='#90bc8c'), row=2, col=1)
    fig.add_trace(go.Scatter(x=df2['City'], y=df2['Tag Frequency'], mode="lines+text", text=text, marker_color='#90bc8c'), row=2, col=2)

    fig.update_xaxes(title_text="City", row=1, col=1)
    fig.update_xaxes(title_text="City", row=1, col=2)
    fig.update_xaxes(title_text="City", row=2, col=1)
    fig.update_xaxes(title_text="City", row=2, col=2)

    fig.update_yaxes(title_text="Number of twitters", row=1, col=1)
    fig.update_yaxes(title_text="Word Length", row=1, col=2)
    fig.update_yaxes(title_text="Emoji Frequency", row=2, col=1)
    fig.update_yaxes(title_text="Tag Frequency", row=2, col=2)

    fig.update_layout(height=700, width=1000,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)',
                      showlegend=False)
    return fig


