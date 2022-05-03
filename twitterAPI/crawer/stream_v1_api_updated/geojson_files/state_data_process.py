import json
import shapely.geometry

def read_geojson_file(str_datapath):
    f = open(str_datapath,'r',encoding="utf8")
    data = json.load(f)
    f.close()
    return data

def read_district_list(str_district_path):
    districts_f = open(str_district_path, 'r', encoding='utf8')
    district_list = []
    line = districts_f.readline()
    while line != '':
        district_list.append(line.strip().upper())
        line = districts_f.readline()
    districts_f.close()
    return district_list

def create_melbourne_district():
    district_list = read_district_list('city_district_not_finished/melbourne_districts.txt')
    print(district_list)
    district_dict = {}
    data = read_geojson_file('suburb-2-vic.geojson')['features']
    f = open('city_district_not_finished/melbourne_district.geojson', 'w', encoding='utf8')
    for item in data:
        district_name = item['properties']['vic_loca_2'].upper()
        if district_name in district_list:
            if district_name not in district_dict:
                district_dict[district_name] = []
            district_dict[district_name].append(item['geometry'])
    json.dump(district_dict,f)
    f.close()

def create_sydney_district():
    district_list = read_district_list('city_district_not_finished/sydney_districts.txt')
    print(district_list)
    district_dict = {}
    data = read_geojson_file('suburb-2-nsw.geojson')['features']
    f = open('sydney_district.geojson', 'w', encoding='utf8')
    for item in data:
        district_name = item['properties']['nsw_loca_2'].upper()
        if district_name in district_list:
            if district_name not in district_dict:
                district_dict[district_name] = []
            district_dict[district_name].append(item['geometry'])
    json.dump(district_dict,f)
    f.close()

data = read_geojson_file('aus_lga.geojson')['features']
city_dict = {}
f = open('aus_cities.geojson', 'w', encoding='utf8')
city_name_list = ['Melbourne (C)','Adelaide (C)','Brisbane (C)','Sydney (C)']
for item in data:
    city_name = item['properties']['Name']
    if city_name in city_name_list:
        city_dict[city_name.split(' ')[0]] = item['geometry']
json.dump(city_dict,f)
f.close()
