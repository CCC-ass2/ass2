import json
import shapely.geometry

def read_geojson_file(str_datapath):
    f = open(str_datapath,'r',encoding="utf8")
    data = json.load(f)
    f.close()
    return data

# def geojson_processer(obj_geojson):

def get_boundingbox(obj_geojson):
    # for key in obj_geojson:
    #     print(key)
    boundingbox = []
    west_border = 9999
    east_border = -9999
    north_border = -9999
    south_border = 9999
    for item in obj_geojson["features"]:
        # for key in item:
            # print(key)
        for data in item["geometry"]["coordinates"][0]:
            # print(data)
            west_border = min(float(data[0]),west_border)
            east_border = max(float(data[0]),east_border)
            north_border = max(float(data[1]),north_border)
            south_border = min(float(data[1]),south_border)

    boundingbox.append(west_border)
    boundingbox.append(south_border)
    boundingbox.append(east_border)
    boundingbox.append(north_border)
    return boundingbox

def distract_file_name(file_path):
    file_name = file_path.split('.')[-2]
    return file_name.split('/')[-1]

class geo_dict(object):

    def __init__(self,geojson_location_list):
        self.geo_dict = {}
        self.poly_shape_dict = {}
        for location_file_path in geojson_location_list:
            geo_json = read_geojson_file(location_file_path)
            city_name = distract_file_name(location_file_path).upper()
            self.geo_dict[city_name] = {}
            self.poly_shape_dict[city_name] = {}
            city_poly_shape_dict = self.poly_shape_dict[city_name]
            city_dict = self.geo_dict[city_name]
            for item in geo_json['features']:
                district_name = item['properties']['clue_area']
                block_id = item['properties']['block_id']
                if district_name not in city_dict:
                    city_dict[district_name] = {}
                    city_poly_shape_dict[district_name] = {}
                city_dict[district_name][block_id] = item['geometry']['coordinates']
                city_poly_shape_dict[district_name][block_id] = shapely.geometry.shape(item['geometry'])

    # def coordinate_belongs_to(self,coodinate):


    # def coordinate_belongs_to(self,coodinate,location):
class city_boundaries(object):
    def __init__(self, geojson_location_list):
        self.city_dict = read_geojson_file(geojson_location_list)
        self.poly_shape_dict = {}
        for key in self.city_dict.keys():
            self.poly_shape_dict[key] = shapely.geometry.shape(self.city_dict[key])
        self.city_name_list = ['MELBOURNE','MELB','MEL','SYDNEY','SDY','BRISBANE','BNE','ADELAIDE','ADEL']

    def coordinate_check(self,coordinate):
        if coordinate==None or coordinate=='null':
            return None
        for key in self.poly_shape_dict.keys():
            point = shapely.geometry.Point(coordinate)
            if self.poly_shape_dict[key].intersects(point)==True:
                return key
        return None

    def location_check(self,str_location):
        if str_location==None or str_location=='null':
            return None
        str_list = str_location.upper().split(' ,')
        for word in str_list:
            if word =='MELBOURNE' or word == 'word' or word == 'MEL':
                return 'MELBOURNE'
            if word =='SYDNEY' or word == 'SDY':
                return 'SYDNEY'
            if word == 'BRISBANE' or word == 'BNE':
                return 'BNE'
            if word == 'ADELAIDE' or word == 'ADEL':
                return 'ADELAIDE'
        return None



# coordinates = [[144.7393646, -37.8993225],
# [149.0676, -35.2373],
# [144.99567, -37.83759],
# [151.30315, -32.77246],
# [140.37646111, -37.89761111],
# [115.858, -31.9513],
# [146.33087, -41.38452]]
# dict_test = city_boundaries('geojson_files\\aus_cities.geojson')
# for item in coordinates:
#     print(dict_test.coordinate_check(item))


