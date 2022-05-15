#!/usr/bin/env python
# coding: utf-8
import pandas as pd
import json

Weekdic = {'Mon': 1, 'Tue': 2, 'Wed': 3, 'Thu': 4, 'Fri': 5, 'Sat': 6, 'Sun': 7}
WeekM = {'Mon': "weekday", 'Tue': "weekday", 'Wed': "weekday", 'Thu': "weekday", 'Fri': "weekday", 'Sat': "weekend",
         'Sun': "weekend"}


# Unemployment rate for lga city
def get_unemply():
    with open("pages/backup_page1/Data/unemployment_rate.json", "r") as f:
        unemploy = json.load(f)
    dfUnemploy = pd.DataFrame(unemploy['rows'])
    dfUnemploy['Greater city'] = dfUnemploy['key'].map(lambda x: x[0])
    dfUnemploy['City'] = dfUnemploy['key'].map(lambda x: x[1])
    dfUnemploy = dfUnemploy.drop(['key'], axis=1)
    dfUnemploy = dfUnemploy.dropna(axis=0)
    dfUnemploy.columns = ['Unemploy rate', "Greater city", 'City']
    return dfUnemploy

# Mel city population(10thousands people)
def mel_popu():
    file = "pages/backup_page1/Data/population_city.json"
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


# Unemployment rate for lga city
greaterCity = ["ADELAIDE", "MELBOURNE", "SYDNEY", "BRISBANE"]


def get_greater_unemploy(greaterCity):
    UnemployGreater = []
    dfUnemploy = get_unemply()
    for city in greaterCity:
        unemploy = dfUnemploy[dfUnemploy["Greater city"] == city]['Unemploy rate'].mean()
        unemploy = format(unemploy, '.2f')
        UnemployGreater.append([city, unemploy])
    dfUnemployGreater = pd.DataFrame(UnemployGreater, columns=['Greater city', 'Unemploy rate'])
    return dfUnemployGreater


# Greater city's population (/10 thousands people)
def greater_popu():
    file = "pages/backup_page1/Data/population_greater.json"
    with open(file, 'r', encoding="utf-8") as f:
        pop_greater = json.load(f)
    pop_greater = pd.DataFrame(pop_greater)
    pop_greater['Population'] = pop_greater['Population'].astype(int)
    popu = list(pop_greater['Population'])
    popu_10thou = [x / 10000 for x in popu]
    pop_greater["Population"] = popu_10thou
    return pop_greater


# work & not work in greater city
def gr_work(grHour, s1, e1, s2, e2, s3, e3):
    population_greater = greater_popu()
    dfUnemployGreater = get_greater_unemploy(greaterCity)

    grHour = grHour[(grHour["Hournum"] >= s1) & (grHour["Hournum"] <= e1) | (grHour["Hournum"] >= s2) & (
            grHour["Hournum"] <= e2) | (grHour["Hournum"] >= s3) & (grHour["Hournum"] <= e3)]

    grHour.loc[(grHour["Hournum"] >= s1) & (grHour["Hournum"] <= e1), "hour"] = "work"
    grHour.loc[(grHour["Hournum"] >= s2) & (grHour["Hournum"] <= e2), "hour"] = "after work"
    grHour.loc[(grHour["Hournum"] >= s3) & (grHour["Hournum"] <= e3), "hour"] = "late night"

    grHour = grHour.groupby(["Greater city", "hour"]).mean()
    grHour = pd.DataFrame(grHour)
    grHour.reset_index(inplace=True)
    grHour = grHour.drop(["Hournum"], axis=1)

    grHour_popu = pd.merge(grHour, population_greater, on=['Greater city'])
    grHour_popu["count"] = grHour_popu["value"] / grHour_popu["Population"]
    grHour_popu = grHour_popu.drop(["value"], axis=1)
    grHour_popu = grHour_popu.drop(["Population"], axis=1)

    grHour_popu = grHour_popu.groupby(["Greater city", "hour"]).sum()
    grHour_popu = pd.DataFrame(grHour_popu)
    grHour_popu.reset_index(inplace=True)
    grHour_popu = grHour_popu.pivot(index='Greater city', columns='hour', values='count').fillna(value=0).reset_index()
    grHour_unem_popu = pd.merge(grHour_popu, dfUnemployGreater, on=['Greater city'])
    grHour_unem_popu.columns = ["city", "after work", "late night", "work", "unemployment"]

    return grHour_unem_popu


# Mel hour work& after work & late night
def melHour(work_mel, s1, e1, s2, e2, s3, e3):
    population_city = mel_popu()
    dfUnemploy = get_unemply()

    work_mel = work_mel[(work_mel["Hournum"] >= s1) & (work_mel["Hournum"] <= e1) | (work_mel["Hournum"] >= s2) & (
                work_mel["Hournum"] <= e2) | (work_mel["Hournum"] >= s3) & (work_mel["Hournum"] <= e3)]

    work_mel.loc[(work_mel["Hournum"] >= s1) & (work_mel["Hournum"] <= e1), "Hour"] = "work"
    work_mel.loc[(work_mel["Hournum"] >= s2) & (work_mel["Hournum"] <= e2), "Hour"] = "after work"
    work_mel.loc[(work_mel["Hournum"] >= s3) & (work_mel["Hournum"] <= e3), "Hour"] = "late night"

    work_mel = work_mel.drop(["Hournum"], axis=1)

    work_mel = work_mel.groupby(["City", "Hour"]).mean()
    work_mel = pd.DataFrame(work_mel)
    work_mel.reset_index(inplace=True)

    work_mel_popu = pd.merge(work_mel, population_city, on=["City"])
    # print(work_mel_popu)

    work_mel_popu["count"] = work_mel_popu["value"] / work_mel_popu["Population"]
    work_mel_popu = work_mel_popu.drop(['value'], axis=1)
    work_mel_popu = work_mel_popu.drop(['Population'], axis=1)
    # print(work_mel_popu)

    work_mel_popu = pd.DataFrame(work_mel_popu)
    work_mel_popu.reset_index(inplace=True)
    work_mel_popu = work_mel_popu.pivot(index='City', columns='Hour', values='count').fillna(value=0).reset_index()
    work_mel_popu_unem = pd.merge(work_mel_popu, dfUnemploy, on=['City'])
    work_mel_popu_unem = work_mel_popu_unem.drop(["Greater city"], axis=1)
    work_mel_popu_unem.columns = ["district", "after work", "late night", "work", "unemployment"]

    return work_mel_popu_unem