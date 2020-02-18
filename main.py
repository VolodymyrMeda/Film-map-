import folium
import pandas as pd
import csv
import ssl
import geocoder
from math import cos, asin, sqrt


def year_films(year, file):
    '''
    int, file -> list(tuple)
    Function returns a list of tuples in which first element is a film
    name, second element is year and the third one is location.
    That reduces the number of elements that have to be investigated
    '''
    year_list = []

    for yr in range(10000):
        try:
            if int(file['year'][yr]) == year:
                year_list.append((file['movie'][yr], file['year'][yr], file['location'][yr]))
        except ValueError:
            continue

    return year_list


def closest_films(year_list):
    '''
    list(tuples) -> list(tuples)
    Function reads the file, gets locations of the films stared in
    entered year and returns a list with 10 closest films
    depending on the location user entered
    '''
    lat_lon_list = []
    ssl._create_default_https_context = ssl._create_unverified_context

    for film in range(len(year_list)):
        film_place = year_list[film][2]
        location = geocoder.osm(film_place)

        try:
            if location.latlng == None:
                continue
            else:
                lat_lon_list.append((year_list[film][0], year_list[film][1], year_list[film][2],
                                     location.latlng[0], location.latlng[1]))
        except AttributeError:
            continue

    return lat_lon_list


def distance_count(lat1, lon1, lat2, lon2):
    '''
    float, float, float, float -> float
    Function counts the distance between two lat-lon coordinates
    '''
    p = 0.017453292519943295
    dist = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * \
           cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2

    return round(12742 * asin(sqrt(dist)), 2)


def distance_sorter(lat, lon, lat_lon_list):
    '''
    float, float, list -> list(tuples)
    Function returns sorted by distance list of tuples
    '''

    distance_list = []

    for el in lat_lon_list:
        distance_list.append((el[0], el[1], el[2], el[3], el[4], distance_count(lat, lon, el[3], el[4])))

    return sorted(distance_list, key=lambda ls: ls[5])


def main_map(distance_list):
    '''
    list -> None
    Function generates a map with film icons
    '''
    map = folium.Map(location=[49.817930, 24.022602], zoom_start=3)

    population = folium.FeatureGroup(name='Population')
    population.add_child(folium.GeoJson(data=open('world.json', 'r', encoding='utf-8-sig').read(),
                                        style_function=lambda x: {
                                        'fillColor': 'green' if x['properties']['POP2005'] < 40000000
                                        else 'orange' if 40000000 <= x['properties']['POP2005'] < 100000000
                                        else 'red'}))
    map.add_child(population)
    map.add_child(folium.LayerControl())
    map.add_child(folium.Marker(location=[lat, lon], icon=folium.Icon(color='black'), popup='Location entered'))
    try:
        for sign in range(10):
            map.add_child(folium.Marker(location=[distance_list[sign][3] + sign/1000000,
                                                  distance_list[sign][4] + sign/1000000],
                                        icon=folium.Icon(), popup=f'name: {distance_list[sign][0]}'))
    except IndexError:
        map.save('map.html')

    map.save('map.html')


if __name__ == '__main__':
    loc_read = pd.read_csv('locations.csv', error_bad_lines=False, quoting=csv.QUOTE_NONE)
    year = int(input('Enter the year: '))
    lat = float(input('Enter your latitude: '))
    lon = float(input('Enter your longitude: '))
    year_list = year_films(year, loc_read)

    main_map(distance_sorter(lat, lon, closest_films(year_list)))