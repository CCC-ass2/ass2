#!/usr/bin/env python
# coding: utf-8

import pandas as pd 
import json
from data_extraction import read_data

f = open('config.json')
localhost = json.load(f)['IP']

Weekdic = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
WeekM = {'Mon':"weekday", 'Tue':"weekday", 'Wed':"weekday", 'Thu':"weekday", 'Fri':"weekday", 'Sat':"weekend", 'Sun':"weekend"}


# Unemployment rate for lga city
def get_unemply():
    with open("backup_page1/unemployment_rate.json", "r") as f:
        unemploy = json.load(f)
    dfUnemploy = pd.DataFrame(unemploy['rows'])
    dfUnemploy['Greater city'] = dfUnemploy['key'].map(lambda x: x[0])
    dfUnemploy['City'] = dfUnemploy['key'].map(lambda x: x[1])
    dfUnemploy = dfUnemploy.drop(['key'],axis=1)
    dfUnemploy = dfUnemploy.dropna(axis=0)
    dfUnemploy.columns = ['Unemploy rate',"Greater city",'City']
    return dfUnemploy  


# Unemployment rate for lga city
greaterCity = ["ADELAIDE", "MELBOURNE", "SYDNEY", "BRISBANE"]
def get_greater_unemploy(greaterCity):
    UnemployGreater = []
    dfUnemploy = get_unemply()
    for city in greaterCity:
        unemploy = dfUnemploy[dfUnemploy["Greater city"] == city]['Unemploy rate'].mean()
        unemploy = format(unemploy, '.2f')
        UnemployGreater.append([city, unemploy])
    dfUnemployGreater = pd.DataFrame(UnemployGreater,columns=['Greater city','Unemploy rate'])
    return dfUnemployGreater


# Greater city tweets
def get_greater_twts():
    # file = "backup_page1/reduce_greater_count.json"
    # with open(file, 'r', encoding="utf-8") as f:
    #     gr_count = json.load(f)
    gr_count = read_data(f"http://admin:admin@{localhost}:5984/au_main/_design/language/_view/week_time?reduce=true&group_level=1")

    gr_count = pd.DataFrame(gr_count["rows"])
    gr_count['Greater city'] = gr_count['key'].map(lambda x: x[0])
    gr_count = gr_count.drop(['key'],axis=1)
    gr_count = gr_count.dropna(axis=0)
    gr_count.columns = ['Tweets', 'Greater city']
    return gr_count


# Greater city's population (/10 thousands people)
def greater_popu():
    file = "backup_page1/population_greater.json"
    with open(file, 'r', encoding="utf-8") as f:
        pop_greater = json.load(f)
    pop_greater = pd.DataFrame(pop_greater)
    pop_greater['Population'] = pop_greater['Population'].astype(int)
    popu = list(pop_greater['Population'])
    popu_10thou = [x/10000 for x in popu]
    pop_greater["Population"] = popu_10thou
    return pop_greater


# Count Greater city's tweets per 10 thousands people
def greater_twts_popu():
    gr_count = get_greater_twts()
    popu_greater = greater_popu()
    dfUnemployGreater = get_greater_unemploy(greaterCity)
    gr_popu = pd.merge(popu_greater, dfUnemployGreater, on=['Greater city'])
    gr_per_unemploy = pd.merge(gr_popu, gr_count, on=['Greater city'])
    gr_per_unemploy["Twts per person"] = gr_per_unemploy["Tweets"]/gr_per_unemploy["Population"]
    gr_per_unemploy = gr_per_unemploy.drop("Population", axis = 1)
    gr_per_unemploy = gr_per_unemploy.drop("Tweets", axis = 1)
    gr_per_unemploy.columns = ["city", "unemployment","count"]
    return gr_per_unemploy


# The hours that people post tweets in LGA
def lga_hour():
    # file = "backup_page1/reduce_city_hour.json"
    # with open(file, 'r', encoding="utf-8") as f:
    #     city_hour = json.load(f)
    city_hour = read_data(f"http://admin:admin@{localhost}:5984/au_main/_design/language/_view/date_time?reduce=true&group_level=4")
    city_hour = pd.DataFrame(city_hour["rows"])
    city_hour['Greater city'] = city_hour['key'].map(lambda x: x[0])
    city_hour['Date'] = city_hour['key'].map(lambda x: x[1])
    city_hour['Hour'] = city_hour['key'].map(lambda x: x[2])
    city_hour['City'] = city_hour['key'].map(lambda x: x[3])
    city_hour = city_hour.drop(['key'],axis=1)
    city_hour = city_hour.dropna(axis=0)
    city_hour = city_hour.drop(["Date"], axis = 1)
    city_hour = city_hour[city_hour["Greater city"] == "MELBOURNE"]
    city_hour = city_hour.drop(["Greater city"], axis = 1)

    return city_hour


# Count twts for Cities in Greater Mel
def twts_mel():
    mel_city = lga_hour()
    mel_city = mel_city.drop(["Hour"], axis = 1)
    mel_city = mel_city.groupby("City").sum()
    return mel_city


# Mel city population(10thousands people)
def mel_popu():
    file = "backup_page1/population_city.json"
    with open(file, 'r', encoding="utf-8") as f:  
        population_city = json.load(f)
    population_city = pd.DataFrame(population_city)
    population_city = population_city[population_city["Greater city"] == "MELBOURNE"]
    population_city['Population'] = population_city['Population'].astype(int)
    population_city = population_city.drop(['Greater city'], axis = 1)
    popu_m = list(population_city['Population'])
    popu_m_10thou = [x/10000 for x in popu_m]
    population_city["Population"] = popu_m_10thou
    return population_city


# Mel city with num of twts/10thousands people, unemployment rate
def mel_twts_unem():
    dfUnemploy = get_unemply()
    popu_mel = mel_popu()
    mel_twts = twts_mel()
    popu_unemploy = pd.merge(dfUnemploy, popu_mel, on=["City"])
    popu_unemploy = popu_unemploy.drop(['Greater city'], axis = 1)
    per_unemploy = pd.merge(popu_unemploy, mel_twts, on=[ "City"])
    per_unemploy["count"] = per_unemploy["value"]/per_unemploy["Population"]
    per_unemploy = per_unemploy.drop("Population", axis = 1)
    per_unemploy = per_unemploy.drop("value", axis = 1)
    per_unemploy.columns = ["unemployment", "district", "count"]
    
    return per_unemploy


# Weekly tweets in 4 geater city 
def greater_week_twts():
    # file = "backup_page1/mrc_result.json"
    # with open(file, 'r', encoding="utf-8") as f:
    #     week_greater = json.load(f)
    week_greater = read_data(f"http://admin:admin@{localhost}:5984/au_main/_design/language/_view/week_time?reduce=true&group_level=3")
    week_greater = pd.DataFrame(week_greater["rows"])
    week_greater['Greater city'] = week_greater['key'].map(lambda x: x[0])
    week_greater['Date'] = week_greater['key'].map(lambda x: x[1])
    week_greater['Week'] = week_greater['key'].map(lambda x: x[2])
    week_greater = week_greater.drop(['key'],axis=1)
    week_greater = week_greater.dropna(axis=0)
    week_greater = week_greater.drop(['Date'],axis=1)
    return week_greater


#  Twts in 4 geater city on the weekday & weekend
def week_gr():
    week4City = greater_week_twts()
    population_greater = greater_popu()
    dfUnemployGreater = get_greater_unemploy(greaterCity)
    week_list = list(week4City["Week"])
    week_disp = []
    for i in week_list:
        week_disp.append(WeekM[i])
    week4City["Week"] = week_disp
    newdf = week4City.groupby(["Greater city", "Week"]).mean()
    week4City = pd.DataFrame(newdf)
    week4City.reset_index(inplace = True)
    week4City  = week4City.pivot(index='Greater city', columns='Week', values='value').fillna(value=0).reset_index()

    gr_week_popu = pd.merge(week4City, population_greater, on = ["Greater city"])

    if 'weekend' not in gr_week_popu.columns:
        gr_week_popu['weekend'] = 0

    gr_week_popu["weekday"] = gr_week_popu["weekday"] / gr_week_popu["Population"]
    gr_week_popu["weekend"] = gr_week_popu["weekend"] / gr_week_popu["Population"]
    gr_week_popu = gr_week_popu.drop(["Population"], axis = 1)
    gr_week_popu_une = pd.merge(gr_week_popu, dfUnemployGreater, on=["Greater city"])
    gr_week_popu_une.columns = ["city", "weekday", "weekend","unemployment"]
    return gr_week_popu_une


# Twts in Mel on the weekday & weekend 
def wk_mel():
    file = "backup_page1/mrc_res1.json"
    with open(file, 'r', encoding="utf-8") as f:
        week = json.load(f)
    # week = read_data(f"http://admin:admin@{localhost}:5984/au_main/_design/language/_view/week_time?reduce=true&group_level=4")
    week_city = pd.DataFrame(week["rows"])
    week_city['Greater city'] = week_city['key'].map(lambda x: x[0])
    week_city['Date'] = week_city['key'].map(lambda x: x[1])
    week_city['Week'] = week_city['key'].map(lambda x: x[2])
    week_city['City'] = week_city['key'].map(lambda x: x[3])
    week_city = week_city.drop(['key'],axis=1)
    week_city = week_city.dropna(axis=0)
    week_city = week_city[week_city["Greater city"] == "MELBOURNE"]
    week_city = week_city.drop(['Greater city'],axis=1)
    week_city = week_city.drop(["Date"], axis = 1)
    return week_city


# weekday& weekend
def weekMel():
    population_city = mel_popu() 
    week2Mel = wk_mel()
    dfUnemploy = get_unemply()
    week_list = list(week2Mel["Week"])
    week_disp = []
    for i in week_list:
        week_disp.append(WeekM[i])

    week2Mel["Week"] = week_disp
    week2Mel = week2Mel.groupby(["City", "Week"]).mean()
    week2Mel.reset_index(inplace = True)
    week2Mel_popu = pd.merge(week2Mel, population_city, on = ["City"])
    #week2Mel_popu = week2Mel_popu.drop(["Greater city"], axis = 1)
    week2Mel_popu["count"] = week2Mel_popu["value"] / week2Mel_popu["Population"] 
    week2Mel_popu = week2Mel_popu.drop(["Population"], axis = 1)
    week2Mel_popu = week2Mel_popu.drop(["value"], axis = 1)
    week2Mel_popu  = week2Mel_popu.pivot(index='City', columns='Week', values='count').fillna(value=0).reset_index()
    week2Mel_popu_unem = pd.merge(week2Mel_popu, dfUnemploy, on = ["City"])
    week2Mel_popu_unem = week2Mel_popu_unem.drop(["Greater city"], axis=1)

    if 'weekend' not in week2Mel_popu_unem.columns:
        week2Mel_popu_unem['weekend'] = 0
    week2Mel_popu_unem.columns = ["district", "weekday", "weekend", "unemployment"]
    return week2Mel_popu_unem


# Check correlation of unemployment rate and num of tweets on weekdays in Mel
def cor_week_mel():
    week_mel = wk_mel()
    dfUnemploy = get_unemply()
    population_city = mel_popu() 
    week_mel = week_mel.groupby(["City", "Week"]).mean()
    week_mel = pd.DataFrame(week_mel)
    week_mel.reset_index(inplace = True)
    week_mel_unem = pd.merge(week_mel, dfUnemploy, on = ["City"])
    week_mel_unem_popu = pd.merge(week_mel_unem, population_city, on = ["City"])
    week_mel_unem_popu["Tweets per person"] = week_mel_unem_popu["value"] / week_mel_unem_popu["Population"]
    week_mel_unem_popu = week_mel_unem_popu.drop(["Greater city"], axis = 1)
    week_mel_unem_popu = week_mel_unem_popu.drop(["value"], axis = 1)
    week_mel_unem_popu = week_mel_unem_popu.drop(["Population"], axis = 1)
    week_list = list(week_mel_unem_popu["Week"])
    weekdaynum = []
    for i in week_list:
        weekdaynum.append(Weekdic[i])
    week_mel_unem_popu["weekdaynum"] = weekdaynum
    week_mel_unem_popu.columns = ["district", "weekday", "unemployment", "count", "weekdaynum"]
    return week_mel_unem_popu


#  hour
def gr_hour():
    # with open("backup_page1/reduce_greater_hour.json") as f:
    #     grHour = json.load(f)
    grHour = read_data(f"http://admin:admin@{localhost}:5984/au_main/_design/language/_view/date_time?reduce=true&group_level=3")
    grHour = pd.DataFrame(grHour["rows"])

    grHour['Greater city'] = grHour['key'].map(lambda x: x[0])
    grHour['date'] = grHour['key'].map(lambda x: x[1])
    grHour['hour'] = grHour['key'].map(lambda x: x[2])
    grHour = grHour.drop(['date'],axis=1)
    grHour = grHour.drop(['key'],axis=1)
    grHour = grHour.dropna(axis=0)
    return grHour


# work & not work in greater city
def gr_work():
    grHour = gr_hour()
    grHour["Hournum"] = list(map(int, list(grHour["hour"])))
    return grHour


# Mel hour work& after work & late night
def melHour():
    work_mel = lga_hour()
    work_mel["Hournum"] = list(map(int, list(work_mel["Hour"])))

    return work_mel


# scatter  hour
def cor_hour_mel():
    mel_hour = lga_hour()
    population_city = mel_popu() 
    dfUnemploy = get_unemply()
    
    mel_hour_popu = pd.merge(mel_hour, population_city, on = ["City"])
    mel_hour_popu["count"] = mel_hour_popu["value"] / mel_hour_popu["Population"]
    mel_hour_popu = mel_hour_popu.drop(['value'],axis=1)
    mel_hour_popu = mel_hour_popu.drop(['Population'],axis=1)
    mel_hour_popu_unem = pd.merge(mel_hour_popu, dfUnemploy, on = ["City"])
    mel_hour_popu_unem = mel_hour_popu_unem.drop(["Greater city"], axis = 1)
    mel_hour_popu_unem["hournum"] = list(map(int, list(mel_hour_popu_unem["Hour"])))
    
    mel_hour_popu_unem.columns = ["hour","district", "count", "unemployment", "hournum"]
    return mel_hour_popu_unem


def get_df():
    city1 = greater_twts_popu()
    city2 = week_gr()
    city3 = gr_work()
    mel1 = mel_twts_unem()
    mel2 = weekMel()
    mel3 = melHour()
    mel_week = cor_week_mel()
    mel_hour = cor_hour_mel()
    res = {'city1': city1.to_dict(), 'city2': city2.to_dict(), 'city3': city3.to_dict(),
           'mel1': mel1.to_dict(), 'mel2': mel2.to_dict(), 'mel3': mel3.to_dict(),
           'mel_week': mel_week.to_dict(), 'mel_hour': mel_hour.to_dict()}

    return res



def main():
    city1 = greater_twts_popu()
    city2 = week_gr()
    city3 = gr_work()
    mel1 = mel_twts_unem()
    mel2 = weekMel()
    mel3 = melHour()
    mel_week = cor_week_mel()
    mel_hour =  cor_hour_mel()
    return city1, city2, city3, mel1, mel2, mel3, mel_week, mel_hour


if __name__ == "__main__":
    main()

