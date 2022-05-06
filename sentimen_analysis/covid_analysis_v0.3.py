from itertools import groupby
import json
import os
import numpy as np
from torch import negative
from wordcloud import WordCloud, STOPWORDS, ImageColorGenerator
import matplotlib.pyplot as plt
from textblob import TextBlob,Blobber
from nltk.corpus import stopwords
import re
from PIL import Image
from textblob.sentiments import NaiveBayesAnalyzer,PatternAnalyzer
import time
import pandas as pd
from pyecharts.charts import Pie,Line
from pyecharts import options as opts
import math

WCD = dict() 

# produce wordcloud
# ref:https://www.kaggle.com/code/ahmedmsoliman/tweets-82-accuracy 
def MakeCloud(text , title = 'Word Clouds' , w = 7 , h = 7):
    stopword = STOPWORDS
    stopword.update(['COVID','US','years','one','U','corona','new','day','t']) # remove some unuseful word
    global WCD

    mask = np.array(Image.open('aus_color.png'))
    image_color = ImageColorGenerator(mask) # use mask toobtain underline shape and text color

    plt.figure(figsize=(w,h))
    WC = WordCloud(background_color="white", collocations=False,mask=mask,color_func = image_color,stopwords=stopword).generate(text)
    plt.tight_layout(pad=0)
    WCD = WC.words_
    plt.imshow(WC, interpolation="bilinear")
    plt.axis("off")
    plt.title(title)
    plt.show() 
    WC.to_file("img/first_review.png")


# 把simplified data里的text+情感分析预处理读成dict
def read_covid_data ():
    text_list = []
    english = other = 0
    # f = open("simplified_data.txt")
    f = open("covid_with_location_new.txt")
    lines = f.readline()
  
    while lines:
        lines = json.loads(lines)
        if lines["lang"] == "en":
            context = clean_data(lines)
            sentiment, polarity = get_sentimental(context)
            day,month,year,time_string = get_time(lines)
            data = {"text":context, "polarity":polarity,"sentiment":sentiment,
                            "day":day,"month":month,"year":year,"tweet_time":time_string}
            text_list.append(data)
            english += 1
        else:
            other += 1
        lines = f.readline() 

    f.close() 
    return english,other,text_list

# tweet text cleaning
def clean_data(lines):
    # regular expression for detecting url
    url = '((http|https)\:\/\/)?[a-zA-Z0-9\.\/\?\:@\-_=#]+\.([a-zA-Z]){2,6}([a-zA-Z0-9\.\&\/\?\:@\-_=#])*' 

    #去掉RT开头
    context = lines["text"].strip('RT') 
    # drop url
    context = ' '.join([re.sub(url,' ',tw) for tw in context.split()]) 
    # drop retweet's @ name
    context = ' '.join([re.sub('^@(\w)+',' ',tw) for tw in context.split()]) 

    return context

# check a single-line text is either neutral/positive/negative
def get_sentimental(context):
    tb = TextBlob(context)
    polarity = tb.sentiment.polarity

    if  math.isclose(polarity, 0, rel_tol=1e-5): #
        sentiment = "neutral"
    elif polarity > 0 :
        sentiment = "pos"
    elif polarity < 0:
        sentiment = "neg"
    return sentiment, polarity


def get_time(lines):
    time_list = lines['time'].split(" ")
    time_string = "{}-{}-{}".format(time_list[5],time_list[1],time_list[2])
    # month_dict = {"Jan":"01","Feb":"02","Mar":"03","Apr":"04","May":"05","Jun":"06",
                        # "July":"07","Aug":"08","Sep":"09","Oct":"10","Nov":"11","Dec":"12"}
    day = time_list[2]
    # month = month_dict[time_list[1]]
    month = time_list[1]
    year = time_list[5]
    return day,month,year,time_string


# get input data ready for plotting the melb-senti-count-pie-chart
def melb_pie_chart_data(df):
    positive = df[df['sentiment']=="pos"].count()
    negative = df[df['sentiment']=="neg"].count()
    neutral = df[df['sentiment']=="neutral"].count()
    input_data = [int(positive['sentiment']),int(negative['sentiment']),int(neutral['sentiment'])]
    return input_data


def melb_line_chart_data(df):
    unique_month = list(df['month'].unique())
    
    positive = df[df['sentiment']=="pos"].groupby(['year','month'],as_index = False).count()
    negative = df[df['sentiment']=="neg"].groupby(['year','month'],as_index = False).count()
    neutral = df[df['sentiment']=="neutral"].groupby(['year','month'],as_index = False).count()
    data = [list(positive[:]['sentiment']),list(negative[:]['sentiment']),
                    list(neutral[:]['sentiment']),list(positive['month'])]

    # Sort the month as this order          
    rule = ["Jan","Feb","Mar","Apr","May","Jun","July","Aug","Sep","Oct","Nov","Dec"]
    pos = []
    neg = []
    neutral = []
    month_ = []
    for i in rule:
        for j in range(4):
            if i == data[3][j]:
                pos.append(data[0][j])
                neg.append(data[1][j])
                neutral.append(data[2][j])
                month_.append(i)
    data2 = [pos,neg,neutral,month_]
    return data2

# Plot: Melbourne sentimental count pie chart,生成本地的html文件
# ref:https://blog.csdn.net/zc666ying/article/details/105080212
# ref:https://zhuanlan.zhihu.com/p/377519823 
def plot_pie(data):
    #
    attr = ["positive","negative","neutral"]

    melb_pie = Pie(init_opts=opts.InitOpts()
    ).add(

         series_name="Sentimental Count",
         data_pair=[list(x) for x in zip(attr,data)], 
         radius=["40%", "75%"],
         label_opts=opts.LabelOpts(is_show=True, position="center")
         
         ).set_global_opts(

             title_opts = opts.TitleOpts(title="Melbourne sentimental count pie chart"),
             legend_opts=opts.LegendOpts(is_show=True,orient="vertical",pos_top="15%",pos_left="2%"),
             
        ).set_series_opts(

            tooltip_opts=opts.TooltipOpts(
            trigger="item", formatter="{a} <br/>{b}: {c} ({d}%)"
        ),
        #设置标签颜色
         label_opts=opts.LabelOpts(formatter="{b}:{c}"),
        ).render("try.html")

# ref: https://zhuanlan.zhihu.com/p/377519823
def plot_lines(data):
    time_lines = (
        Line().add_xaxis(xaxis_data = data[3]).add_yaxis(
            series_name = "Positive",
            stack = "stack",
            y_axis=data[0],
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=True)
        ).add_yaxis(
            series_name = "Negative",
            stack = "stack",
            y_axis=data[1],
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=True)
        ).add_yaxis(
            series_name = "Neutral",
            stack = "stack",
            y_axis=data[2],
            areastyle_opts=opts.AreaStyleOpts(opacity=0.5),
            label_opts=opts.LabelOpts(is_show=True)
        ).set_global_opts(
            title_opts=opts.TitleOpts(title="Time Series change"),
            tooltip_opts=opts.TooltipOpts(trigger="axis",axis_pointer_type="cross"),
            yaxis_opts=opts.AxisOpts(
                type_="value",
                axistick_opts=opts.AxisTickOpts(is_show=True),
                splitline_opts=opts.SplitLineOpts(is_show=True),
            ),
            xaxis_opts=opts.AxisOpts(type_="category",boundary_gap=False),
        )
    ).render("line.html")


def main():

    _,_,text_list = read_covid_data()
    df = pd.DataFrame(text_list,columns = ["text","polarity","sentiment","day","month","year","tweet_time"])
    # MakeCloud(' '.join(df["text"]))
    df.reset_index(inplace=True)

    df['month'].iloc[:30] = "Jan"
    df['month'].iloc[31:87] = "Feb"
    df['month'].iloc[100:234] = "Mar"

    input_data_1 = melb_pie_chart_data(df)
    input_data_2 = melb_line_chart_data(df)
    plot_pie(input_data_1)
    plot_lines(input_data_2)

    print(df)
    


if __name__ == "__main__":
  print('Start Time:{}'.format(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))))
  main()
  print('End Time:{}'.format(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))))