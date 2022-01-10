from owlready2 import *
import csv
import pandas as pd
from datetime import datetime


# load ontology
onto_path.append("islands")
onto = get_ontology("./islandsv3.owl")
onto.load()

#load data
cities = pd.read_csv('../crawl/cities.csv')
islands = pd.read_csv('../crawl/islands.csv')
places = pd.read_csv('../crawl/places.csv')
restaurants = pd.read_csv('../crawl/restaurants.csv')
restaurants_islands = pd.read_csv('../crawl/restaurants_islands.csv')

cities_islands = islands.merge(cities, left_on = 'cityId', right_on= 'id', how='left')
tourist_attraction = places.merge(islands, left_on = 'islandId', right_on= 'id', how='left')
restaurants_tmp = restaurants.merge(restaurants_islands, left_on = 'id', right_on= 'restaurantId', how='left')
restaurants_res = restaurants_tmp.merge(islands, left_on = 'islandId', right_on= 'id', how='left')


#add individual City
for index, row in cities.iterrows():
    city=onto.City(row['name'].replace(' ', '_'))
    city.hasCityName=[row['name']]
    city.atCountry=[onto.Country("Việt Nam")]

#add individual Island
for index, row in cities_islands.iterrows():
    island=onto.Island(row['name_x'].replace(' ', '_'))
    island.belongTo=[onto.City(row['name_y'].replace(' ', '_'))]
    island.hasIslandName = [row['name_x']]
    if (str(row['longitude']) != 'nan'):
        island.hasLongitude = [row['longitude']]
    if (str(row['latitude']) != 'nan'):
        island.hasLatitude=[row['latitude']]
    if (str(row['summary']) != 'nan'):
        island.hasAbstract = [row['summary']]

#add individual Tourist Attraction
for index, row in tourist_attraction.iterrows():
    tourist = onto.TouristAttraction(row['name_x'].replace(' ', '_'))
    tourist.hasPlaceName= [row['name_x']]
    tourist.placeAt=[onto.Island(row['name_y'].replace(' ', '_'))]

#add individual Restaurant
for index, row in restaurants_res.iterrows():
    restaurant = onto.Restaurant(row['name_x'].replace(' ', '_'))
    restaurant.hasPlaceName=[row['name_x']]
    restaurant.placeAt.append(onto.Island(row['name_y'].replace(' ', '_')))

onto.save('islands_individualv3.owl')
