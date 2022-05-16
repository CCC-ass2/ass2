import streamlit as st
import plotly.graph_objects as go
from plotly.subplots import make_subplots
import os
import requests
import json
import pandas as pd
from pages.backup_page1.dataprocess import gr_work, melHour
import json

f = open('config.json')
localhost = json.load(f)['IP']

# read data
fname = 'pages/backup_page1/data.json'
if not os.path.isfile(fname):
    r = requests.get(f'http://{localhost}:8000/page1data').json()
    with open(fname, 'w') as fp:
        json.dump(r, fp)
else:
    with open(fname, 'rb') as f:
        r = json.load(f)
city1 = pd.DataFrame(r['city1'])
city2 = pd.DataFrame(r['city2'])
city3 = pd.DataFrame(r['city3'])
mel1 = pd.DataFrame(r['mel1'])
mel2 = pd.DataFrame(r['mel2'])
mel3 = pd.DataFrame(r['mel3'])
mel_week = pd.DataFrame(r['mel_week'])
mel_hour = pd.DataFrame(r['mel_hour'])

WeekMarkers = ['Mon', 'Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
HourMarkers = ["{0:02d}".format(i) for i in range(24)]


def display():
    st.title('Stress Analysis on Twitter & Unemployment Rate')
    st.write('This scenario mainly attempts to explore the correlation between the time people tend to tweet and the unemployment rate in different regions. The regions we chose to analyse are between four greater cities: Adelaide, Melbourne, Sydney and Brisbane, and the local government area within the Greater Melbourne. Two time dimensions are considered, the hour level and the weekday/weekend level.')

    with st.expander('Tweets & Employment Rate'):
        st.subheader("Number of Tweets (for each 10 thousands people) VS Unemployment Rate")
        st.plotly_chart(greater_mel_twts(city1, mel1))

    with st.expander('Weekday & Weekend'):
        st.subheader('Average Number of Tweets on Weekdays VS Weekend')
        st.plotly_chart(greater_mel_weekday(city2, mel2))

    with st.expander('Working Time & Non-working Time'):
        a1, a2, a3 = st.columns(3)
        c1, c2, c3, c4, c5, c6 = st.columns(6)
        a1.text('Working time')
        a2.text('Off-duty time')
        a3.text('Late night')
        s1 = int(c1.text_input('Start', value=9))
        e1 = int(c2.text_input('End', value=18))
        s2 = int(c3.text_input('Start ', value=19))
        e2 = int(c4.text_input('End ', value=23))
        s3 = int(c5.text_input('Start  ', value=0))
        e3 = int(c6.text_input('End  ', 5))
        city_3 = gr_work(city3, s1, e1, s2, e2, s3, e3)
        mel_3 = melHour(mel3, s1, e1, s2, e2, s3, e3)
        st.plotly_chart(greater_mel_workhour(city_3, mel_3))


# twitter amount VS unemployment
def greater_mel_twts(city1, mel1):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Greater Cities", "Cities in Greater Melbourne (Top 10)"), specs=[[{'secondary_y': True}, {'secondary_y': True}]])

    # graph1
    city1 = city1.sort_values('unemployment', ascending=False)
    fig.add_trace(go.Bar(x=city1['city'], y=city1['count'], marker_color='#bea0a3', name='Num of Tweets'),secondary_y=False,
                  row=1, col=1)
    fig.update_traces(width=0.5)

    fig.add_trace(go.Scatter(x=city1['city'], y=city1['unemployment'],mode='lines+markers+text',
                             marker_color='#e2afa4', name='Unemployment Rate', text=city1['unemployment'],
                             textposition="top center"),secondary_y=True,
                  row=1, col=1)

    fig.update_yaxes(autorange="reversed", secondary_y=True, row=1, col=1)
    fig.update_yaxes(title_text="Tweet number/(10 thousands people)", secondary_y=False, row=1, col=1)
    fig.update_yaxes(title_text="Unemployment rate (%)", secondary_y=True, row=1, col=1)

    # grpah 2
    if len(mel1) > 10:
        mel1 = mel1.sort_values('count', ascending=False)[:10]
    mel1 = mel1.sort_values('unemployment', ascending=False)
    fig.add_trace(go.Bar(x=mel1['district'], y=mel1['count'], marker_color='#91AEAC', name='Num of Tweets'),secondary_y=False,
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=mel1['district'], y=mel1['unemployment'],mode='lines+markers+text', text=mel1['unemployment'], textposition="top center",
                             marker_color='#8abcbe', name='Unemployment Rate'),secondary_y=True,
                  row=1, col=2)

    fig.update_yaxes(title_text="Tweet number/(10 thousands people)", secondary_y=False, row=1, col=2)
    fig.update_yaxes(range=[0, sorted(mel1['count'], reverse=True)[1]*2.5],secondary_y=False, row=1, col=2)
    fig.update_yaxes(title_text="Unemployment rate (%)", secondary_y=True, row=1, col=2)

    fig.update_layout(height=500, width=1000,
                      # title_text="Number of Tweets for each 10 thousands people VS Unemployment Rate",
                      paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')

    return fig


# weekday VS weekend
def greater_mel_weekday(city2, mel2):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Greater Cities", "Cities in Greater Melbourne (Top 10)"), specs=[[{'secondary_y': True}, {'secondary_y': True}]])

    # graph 1
    city2 = city2.sort_values('unemployment', ascending=False)
    fig.add_trace(go.Scatter(x=city2['city'], y=city2['weekday'], marker_color='#bac94a', mode='lines+markers+text',
                             name='Weekday', text=[round(i,2) for i in city2['weekday']], textposition="top center"),
                  secondary_y=False, row=1, col=1)
    fig.add_trace(go.Scatter(x=city2['city'], y=city2['weekend'], marker_color='#dfc243', mode='lines+markers+text',
                             name='Weekend', text=[round(i,2) for i in city2['weekend']], textposition="top center"),
                  secondary_y=True, row=1, col=1)
    fig.add_trace(go.Bar(x=city2['city'], y=city2['unemployment'], marker_color='#90bc8c',name='unemployment'),
                  secondary_y=False, row=1, col=1)

    fig.update_layout(barmode='group', bargap=0.3,)
    fig.update_yaxes(title_text="Tweet number/(10 thousands people)", secondary_y=True, row=1, col=1)
    fig.update_yaxes(title_text="Unemployment rate (%)", secondary_y=False, row=1, col=1)
    fig.update_yaxes(range=[0, sorted(city2['weekend'], reverse=True)[0] * 2.5], secondary_y=True, row=1, col=1)

    # graph 2
    if len(mel2) > 10:
        mel2 = mel2.sort_values('weekday', ascending=False)[:10]
    mel2 = mel2.sort_values('unemployment', ascending=False)
    fig.add_trace(go.Bar(x=mel2['district'], y=mel2['weekday'], marker_color='#91AEAC',name='Weekday'),secondary_y=False,
                  row=1, col=2)
    fig.add_trace(go.Bar(x=mel2['district'], y=mel2['weekend'], marker_color='#ecd59f', name='Weekend'),secondary_y=False,
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=mel2['district'], y=mel2['unemployment'],mode='lines+text+markers', text=mel2['unemployment'],
    textposition="top center", marker_color='#8abcbe',name='unemployment'),secondary_y=True,
                  row=1, col=2)

    fig.update_yaxes(title_text="Tweet number/(10 thousands people)", secondary_y=False, row=1, col=2)
    fig.update_yaxes(range=[0, sorted(mel2['weekday'], reverse=True)[1]*2.5],secondary_y=False, row=1, col=2)
    fig.update_yaxes(title_text="Unemployment rate (%)", secondary_y=True, row=1, col=2)

    fig.update_layout(height=500, width=1000,
                      paper_bgcolor='rgba(0,0,0,0)',
                      plot_bgcolor='rgba(0,0,0,0)')

    return fig


# work time VS non-working time
def greater_mel_workhour(city3, mel3):
    fig = make_subplots(
        rows=1, cols=2,
        subplot_titles=("Greater Cities", "Cities in Greater Melbourne (Top 10)"), specs=[[{'secondary_y': True}, {'secondary_y': True}]])

    # graph 1
    city3 = city3.sort_values('unemployment', ascending=False)
    fig.add_trace(go.Bar(x=city3['city'], y=city3['work'], marker_color='#a16fb2',name="Working time"),secondary_y=False,
                  row=1, col=1)
    fig.add_trace(go.Bar(x=city3['city'], y=city3['after work'], marker_color='#d19282',name="After working"),secondary_y=False,
                  row=1, col=1)
    fig.add_trace(go.Bar(x=city3['city'], y=city3['late night'], marker_color='#ed7953',name="Late night"),secondary_y=False,
                  row=1, col=1)
    fig.update_layout(barmode='group')

    fig.add_trace(go.Scatter(x=city3['city'], y=city3['unemployment'],mode='lines+markers+text', marker_color='#a39396',
                             name="Unemployment Rate", text=city3['unemployment'], textposition="top center"),secondary_y=True,
                  row=1, col=1)

    fig.update_yaxes(autorange="reversed", secondary_y=True, row=1, col=1)
    fig.update_yaxes(title_text="Tweet number/(10 thousands people)", secondary_y=False, row=1, col=1)
    fig.update_yaxes(title_text="Unemployment rate (%)", secondary_y=True, row=1, col=1)

    # graph 2
    if len(mel3) > 10:
        mel3 = mel3.sort_values('work', ascending=False)[:10]
    mel3 = mel3.sort_values('unemployment', ascending=False)
    fig.add_trace(go.Bar(x=mel3['district'], y=mel3['work'], marker_color='#d9b5ca',name="Working time"),secondary_y=False,
                  row=1, col=2)
    fig.add_trace(go.Bar(x=mel3['district'], y=mel3['after work'], marker_color='#d09890',name="After working"),secondary_y=False,
                  row=1, col=2)
    fig.add_trace(go.Bar(x=mel3['district'], y=mel3['late night'], marker_color='#bd3786',name="Late night"),secondary_y=False,
                  row=1, col=2)
    fig.add_trace(go.Scatter(x=mel3['district'], y=mel3['unemployment'],mode='lines+text+markers', marker_color='#dc787a',
                             name="Unemployment Rate", text=mel3['unemployment'], textposition="top center"),secondary_y=True,
                  row=1, col=2)

    fig.update_yaxes(range=[0, sorted(mel3['late night'], reverse=True)[0] * 1.4], secondary_y=False, row=1, col=2)
    fig.update_yaxes(title_text="Tweet number/(10 thousands people)", secondary_y=False, row=1, col=2)
    fig.update_yaxes(title_text="Unemployment rate (%)", secondary_y=True, row=1, col=2)

    fig.update_layout(height=500, width=1000,
                      # title_text="Working time VS Off-duty Time",
                      paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)')

    return fig