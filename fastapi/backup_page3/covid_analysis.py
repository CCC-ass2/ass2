import time
import pandas as pd
from data_extraction import read_data

import json

f = open('config.json')
localhost = json.load(f)['IP']

def read_reduce():
    # city-district-sentiment as index
    # reduced = r"backup_page3/reduce3.json"
    # reduced = r"reduce3.json"

    # with open (reduced,'r') as f:
    #     reduced_dict = json.load(f)
    reduced_dict = read_data(f"http://admin:admin@{localhost}:5984/au_covid/_design/language/_view/sentiment?reduce=true&group_level=3")
    df = pd.DataFrame(reduced_dict['rows'])
    df['city'] = df['key'].map(lambda x: x[0])
    df['district'] = df['key'].map(lambda x: x[1])
    df['sentiment'] = df['key'].map(lambda x: x[2])
    df = df.drop(['key'],axis=1)

    # city-date-sentiment as index
    # reduced_2 = r"backup_page3/reduce2.json"
    # reduced_2 = r"reduce2.json"
    #
    # with open (reduced_2,'r') as f:
    #     reduced2_dict = json.load(f)
    reduced2_dict = read_data(f"http://admin:admin@{localhost}:5984/au_covid/_design/language/_view/city_time?reduce=true&group_level=3")
    df2 = pd.DataFrame(reduced2_dict['rows'])
    df2['city'] = df2['key'].map(lambda x: x[0])
    df2['sentiment'] = df2['key'].map(lambda x: x[1])
    df2['date'] = df2['key'].map(lambda x: x[2])
    df2 = df2[df2['city'] != 'null']
    df2 = df2.drop(['key'],axis=1)

    return df, df2

def get_df():
    data, data2 = read_reduce()
    res = {'data': data.to_dict(), 'data2': data2.to_dict()}

    return res


def main():
    df,df2 = read_reduce()
    print(df)
    


if __name__ == "__main__":
  print('Start Time:{}'.format(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))))
  main()
  print('End Time:{}'.format(time.strftime('%Y.%m.%d %H:%M:%S', time.localtime(time.time()))))