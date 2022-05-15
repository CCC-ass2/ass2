import streamlit as st
import plotly.graph_objects as go
import numpy as np
from plotly.subplots import make_subplots
import requests
import pandas as pd
import json
import os

f = open('config.json')
localhost = json.load(f)['IP']

# read data
fname = 'pages/backup_page3/data.json'
if not os.path.isfile(fname):
    r = requests.get(f'http://{localhost}:8000/page3data').json()
    with open(fname, 'w') as fp:
        json.dump(r, fp)
else:
    with open(fname, 'rb') as f:
        r = json.load(f)
data = pd.DataFrame(r['data'])
data2 = pd.DataFrame(r['data2'])


# find all districts for each city
all_districts = {"Melbourne": list(data[data["city"] == "MELBOURNE"]["district"].unique()),
                 "Sydney": list(data[data["city"] == "SYDNEY"]["district"].unique()),
                 "Adelaide": list(data[data["city"] == "ADELAIDE"]["district"].unique()),
                 "Brisbane": list(data[data["city"] == "BRISBANE"]["district"].unique())}


# display on the page sentiment
def display():
    st.header('Sentiment Analysis on Covid 19')
    st.write("This scenario explore the correlation between people's attitude towards covid-19 with general hospital services availability within four greater areas, Adelaide, Sydney, Brisbane and Melbourne.")
    col1, col2 = st.columns([1, 2])
    city = col1.selectbox('Select Greater City: ', list(all_districts.keys()))    # select city
    district = col2.multiselect("Select LGA: ", all_districts[city], default=None)    # select districts according to selected city
    date_list = sorted(list(data2['date'].unique()))
    start_date, end_date = st.select_slider('Date: ', options=date_list, value=(date_list[0], date_list[-1]))

    st.plotly_chart(pie_chart(city, district, start_date, end_date))
    st.plotly_chart(hostability())


def pie_chart(city, district, start_date, end_date):
    # select the whole city if no specific district is selected
    if not district or 'Select' in district:
        df1 = data.copy()
        df1_1 = pd.pivot_table(df1, ('value'), index=['sentiment'], aggfunc=np.sum).reset_index()
        df1_1['district'] = 'All city'
    # select a specific district
    else:
        df1 = data.copy()
        df1_1 = pd.pivot_table(df1, ('value'), index=['sentiment', 'district'], aggfunc=np.sum).reset_index()
        df1_1 = df1_1[df1_1['district'].isin(list(district))]  # update

    if not district or "Select" in district:
        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'xy'}]],
                            subplot_titles=(
                                "Sentiment count for {}".format(city), "Time series change for {}".format(city),
                                "Health Industry statistics", "Hospital services statistics"))
    else:
        fig = make_subplots(rows=1, cols=2, specs=[[{'type': 'domain'}, {'type': 'xy'}]],
                            subplot_titles=(
                                "Sentiment count for district(s) {} in {}".format(', '.join(list(district)), city),
                                "Time series change for {}".format(city),
                            "Health Industry statistics", "Hospital services statistics"))

    # pie chart
    fig.add_trace(go.Pie(labels=df1_1['sentiment'], values=df1_1['value'], hole=.4,
                         marker_colors=['#9C8194', '#8393B4', '#EDB9BD']), row=1, col=1,)
    df2 = data2.copy()
    df2 = df2[(df2['city'] == str(city).upper()) & (df2['date']>=start_date) &(df2['date']<=end_date)]  # update
    df2 = pd.pivot_table(df2, ('value'), index=['sentiment', 'date'], aggfunc=np.sum).reset_index()

    # bar chart
    colors = ['lightpink', 'lightslategray', 'rosybrown']
    for j in range(len(df2['sentiment'].unique())):
        i = df2['sentiment'].unique()[j]
        df3 = df2.copy()
        df3 = df3[df3['sentiment'] == i]
        fig.add_trace(go.Bar(x=df3['date'], y=df3['value'], text=df3['value'], textposition='auto',
                             showlegend=False, name="2-{}".format(i), marker_color=colors[j]),
                      row=1, col=2)
    fig.update_layout(barmode='stack', legend_title_text='Sentiment',
                      width = 1000, paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
    return fig


# chart for hospital analysis
def hostability():
    with open("pages/backup_page3/Data/rai_services_indicators_lga_2011.json") as file:
        files = json.load(file)

    df = pd.DataFrame(files['features'])
    df['IGA_name'] = df['properties'].map(lambda x: x['lga_name'].split('(')[0])
    df['hs_rank'] = df['properties'].map(lambda x: x['hs_rank'])
    df['hs_access'] = df['properties'].map(lambda x: x['hs_meas'])
    df["hs_sd"] = df['properties'].map(lambda x: x['hs_sd'])
    df["numgp_service"] = df['properties'].map(lambda x: x['numgp_srv'])
    df["hs_employed"] = df['properties'].map(lambda x: x['ahs_empl'])
    df = df.drop(['type', 'id', 'properties'], axis=1)

    df = df[df['IGA_name'].isin(["Melbourne ", "Sydney ", "Brisbane ", "Adelaide "])]

    return health_industry(df)


def health_industry(df):
    fig = make_subplots(rows=1, cols=2, subplot_titles=("Health Industry statistics", "Hospital services statistics"),
                        specs=[[{'secondary_y': True}, {'secondary_y': True}]])
    # first pie
    fig.add_trace(go.Scatter(x=df['IGA_name'], y=df['numgp_service'], name="Number of GP services",
        marker_color='salmon'), secondary_y=False, row=1, col=1)
    fig.add_trace(go.Scatter(x=df['IGA_name'], y=df['hs_employed'],
                             name="Industry of employment (health and social services)",
                             marker_color='#8393B4'),
                  secondary_y=True, row=1, col=1)
    fig.update_layout(
        # title="Health Industry statistics",     # 主标题
        xaxis_title="LGA city",  # 2个坐标轴的标题
        yaxis_title="Count for GP service",
        font=dict(
            size=16,
            color="#7f7f7f"
        ),
        paper_bgcolor='rgba(0,0,0,0)',
        plot_bgcolor='rgba(0,0,0,0)'
    )
    fig.update_yaxes(title_text="Count for industry employment", secondary_y=True)

    # second pie
    colors = ['salmon', 'lightslategray', 'rosybrown']

    fig.add_trace(go.Scatter(x=df['IGA_name'], y=df['hs_sd'],
        name="Access to hospital services Standard Deviation",  # 第一个图例名称
        marker_color =colors[0]
    ), secondary_y=False, row=1, col=2)

    fig.add_trace(go.Scatter(
        x=df['IGA_name'],
        y=df['hs_rank'],
        name="Access to hospital services Ranking",  # 第2个图例名称
        # visible='legendonly'  #  将第2图例变成灰色，点击可见图形
        marker_color=colors[1]
    ), secondary_y=False, row=1, col=2)

    fig.add_trace(go.Scatter(
        x=df['IGA_name'],
        y=df['hs_access'],
        name="Access to hospital services per capita",  # 第2个图例名称
        marker_color=colors[2]
    ), secondary_y=True, row=1, col=2)

    fig["layout"]["xaxis2"].update({"title": "LGA city"})
    fig["layout"]["yaxis3"].update({"title": "Arithmetic scale"})
    fig["layout"]["yaxis4"].update({"title": "Access to hospital services per capita"})

    fig.update_layout(legend_orientation="h", legend_y=-0.5, width=1000)  # 图例放最下面
    return fig