import requests
import json

f = open('config.json')
localhost = json.load(f)['IP']


def read_data(command):
    r = requests.get(command)
    r = r.json()
    return r
read_data(f"http://admin:admin@{localhost}:5984/au_covid/_design/language/_view/sentiment?reduce=true&group_level=3")


if __name__ == '__main__':
    import pandas as pd
    # print(pd.DataFrame(read_data(f"http://admin:admin@localhost:5984/au_main/_design/language/_view/text?reduce=false")['rows']))
    print(localhost)