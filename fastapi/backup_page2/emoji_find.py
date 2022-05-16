import ast
import pandas as pd
import emoji
import emojis
import numpy as np
from collections import Counter
import itertools
import time
from data_extraction import read_data

import json

f = open('config.json')
localhost = json.load(f)['IP']


def read():
    # data = r"backup_page2/text.json"
    # data = r"text.json"

    # with open(data, 'r', encoding="utf-8") as f:
    #     datef = json.load(f)
    datef = read_data(f"http://admin:admin@{localhost}:5984/au_main/_design/language/_view/text?reduce=false")
    df = pd.DataFrame(datef['rows'])

    df['city'] = df['value'].map(lambda x: x[0])
    df['sentiment'] = df['value'].map(lambda x: x[1])
    df['text'] = df['value'].map(lambda x: x[2])
    df = df.drop(['value'], axis=1)
    return df


# put the text date separate four city
def sep_text(data):
    city_text = {"Melbourne": list(data[data["city"] == "MELBOURNE"]["text"]),
                 "Sydney": list(data[data["city"] == "SYDNEY"]["text"]),
                 "Adelaide": list(data[data["city"] == "ADELAIDE"]["text"]),
                 "Brisbane": list(data[data["city"] == "BRISBANE"]["text"])}
    return city_text


# if the content contain emoji
def check_emoji(character):
    return character in emoji.UNICODE_EMOJI['en']


# count the emoji in one twitter
def count_emoji(text):
    count = 0
    for x in text:
        a = check_emoji(x)
        if a == True:
            count += 1
    return count


def emoji_times(data):
    times = [0] * 6
    for i in range(len(data)):
        c = emojis.count(data[i])
        if c < 6:
            times[c] += 1
        else:
            times[5] += 1
    return times


# store each times(1,2,3,4,5 or above) of freq
def emoji_fre(data):
    fre = [0] * 6
    for i in range(len(data)):
        fre[i] = data[i] / sum(data)
    return fre


def call_emo_fre(text):
    # use list to store how emoji show in one text
    times_ade = emoji_times(text["Adelaide"])
    times_bri = emoji_times(text["Brisbane"])
    times_mel = emoji_times(text["Melbourne"])
    times_syd = emoji_times(text["Sydney"])
    fre_ade = emoji_fre(times_ade)
    fre_bri = emoji_fre(times_bri)
    fre_mel = emoji_fre(times_mel)
    fre_syd = emoji_fre(times_syd)
    count_data = {'num_of_emoji': ['0', '1', '2', '3', '4', '5 and above'], 'times_ade': times_ade,
                  'times_bri': times_bri, 'times_mel': times_mel, 'times_syd': times_syd, 'fre_ade': fre_ade,
                  'fre_bri': fre_bri, 'fre_mel': fre_mel, 'fre_syd': fre_syd}
    return count_data


# calculate the total freq
def fre_emoji(data):
    emoji_sum = 0
    for i in range(len(data)):
        emoji_sum += emojis.count(data[i])
    return (emoji_sum / len(data))


# frequency of tags
def tag_fre(data):
    # stop_words = set(stopwords.words('english'))
    with open('backup_page2/stopwords.txt') as f:
        lines = f.readlines()
        stop_words = ast.literal_eval(lines[0])

    words_filtered = []
    total = 0
    for text in data:
        for word in text.split():
            if word not in stop_words:
                if word[0] == "#":
                    words_filtered.append(word)
                    total += 1
    fre = total / len(data)
    return fre


# function to count words
def word_len(data):
    count = 0
    for text in data:
        for word in text.split():
            count += 1
    return int(count / len(data))


def call_other_fre(text):
    fre_emo_ade = fre_emoji(text["Adelaide"])
    fre_emo_bri = fre_emoji(text["Brisbane"])
    fre_emo_mel = fre_emoji(text["Melbourne"])
    fre_emo_syd = fre_emoji(text["Sydney"])
    tag_fre_ade = tag_fre(text["Adelaide"])
    tag_fre_bri = tag_fre(text["Brisbane"])
    tag_fre_mel = tag_fre(text["Melbourne"])
    tag_fre_syd = tag_fre(text["Sydney"])
    word_len_ade = word_len(text["Adelaide"])
    word_len_bri = word_len(text["Brisbane"])
    word_len_mel = word_len(text["Melbourne"])
    word_len_syd = word_len(text["Sydney"])
    final_data = {'city': ["Adelaide", "Brisbane", "Melbourne", "Sydney"],
                  'text_size': [np.size(text["Adelaide"]), np.size(text["Brisbane"]), np.size(text["Melbourne"]),
                                np.size(text["Sydney"])],
                  'fre_emo': [fre_emo_ade, fre_emo_bri, fre_emo_mel, fre_emo_syd],
                  'tag_fre': [tag_fre_ade, tag_fre_bri, tag_fre_mel, tag_fre_syd],
                  'word_len': [word_len_ade, word_len_bri, word_len_mel, word_len_syd]}
    return final_data


# find top10 emoji for each country
def top10_emoji(data):
    with open('backup_page2/stopwords.txt') as f:
        lines = f.readlines()
        stop_words = ast.literal_eval(lines[0])
    words_filtered = []
    for text in data:
        for word in text.split():
            if word not in stop_words:
                words_filtered.append(word)
    c = Counter(words_filtered)
    d_c = dict(c)
    emoji_list = []
    for item in d_c:
        if check_emoji(item):
            emoji_list.append(item)
    emoji_dict = {}

    for emoji in d_c:
        v = c[emoji]
        if emoji in emoji_list:
            emoji_dict[emoji] = v
    sorted_emojis = {key: value for key, value in sorted(emoji_dict.items(), key=lambda item: item[1], reverse=True)}
    # get top 10 values
    top_10_emoji = dict(itertools.islice(sorted_emojis.items(), 10))
    top_10_emoji_series = pd.Series(top_10_emoji)
    e_list = []
    for each in top_10_emoji_series.index:
        e = emojis.decode(each)
        e_list.append(e)

    e_df = {'emoji': list(top_10_emoji_series.index), 'freq': [int(i) for i in list(top_10_emoji_series.values)]}
    e_df['decoded'] = e_list
    return (e_df)


def get_top10(text):
    ade_top10_emo = top10_emoji(text["Adelaide"])
    bri_top10_emo = top10_emoji(text["Brisbane"])
    mel_top10_emo = top10_emoji(text["Melbourne"])
    syd_top10_emo = top10_emoji(text["Sydney"])
    top10 = {"Adelaide": ade_top10_emo, "Brisbane": bri_top10_emo, "Melbourne": mel_top10_emo, "Sydney": syd_top10_emo}
    return top10


def get_text():
    df1 = read()
    text = sep_text(df1)
    return text

def twitter_df(text):
    df2 = call_other_fre(text)

    df = {
        "Emoji Frequency": df2['fre_emo'],
        "Tag Frequency": df2['tag_fre'],
        "Word Length": df2['word_len'],
        "Number of twitters": df2['text_size'],
        "City": ["Adelaide", "Brisbane", "Melbourne", "Sydney"]
    }
    return df

def top10_df(text):
    top10 = get_top10(text)
    return top10


def get_df():
    text = get_text()
    res = {'twitter_analysis': twitter_df(text), 'top10': top10_df(text)}

    return res


def main():
    df1 = read()
    text = sep_text(df1)
    # add num of emoji
    count_emo = call_emo_fre(text)
    # store other result
    count_fre = call_other_fre(text)
    # get top10 emoji for each city
    top10 = get_top10(text)

    print(count_emo)
    print(count_fre)
    print(get_top10())
    print(type(top10))
    print(top10["Adelaide"])
    print(list(count_fre.keys()))

    print(count_fre['fre_emo'][0:4])
    print(count_fre['fre_emo']+count_fre['tag_fre'])


if __name__ == "__main__":
    print('Start Time:{}'.format(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))))
    df1 = read()
    text = sep_text(df1)
    top10 = get_top10(text)
    print(top10)
    print('End Time:{}'.format(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))))
