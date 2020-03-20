import geopandas
import json
import numpy as np
import pandas as pd
import math

def update_mk_covid_geojson():
    mk_municipalities = geopandas.read_file("https://raw.githubusercontent.com/klupp/opendata/master/mk/opstini-municipalities/municipalities_mq.geojson")
    mk_cities = mk_municipalities.dissolve(by='entity_mk', aggfunc='sum')                                
    # mk_cities['entity_mk'] = mk_cities.index
    mk_cities['id'] = mk_cities.index

    infected_df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=0&single=true&output=csv", 
                              names=['city', 'infected_in', 'date', 'count', 'age', 'source'], header=0)

    healed_df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=757629356&single=true&output=csv",
                           names=['city', 'date', 'count', 'age', 'source'], header=0)

    dead_df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=1754038661&single=true&output=csv",
                                                   header=0, names=['city', 'date', 'count', 'age', 'source'])
    dead_df

    infected_by_city = infected_df[['city', 'count']].copy().groupby('city').sum()
    healded_by_city = healed_df[['city', 'count']].copy().groupby('city').sum()
    dead_by_city = dead_df[['city', 'count']].copy().groupby('city').sum()
    covid_mk = pd.merge(infected_by_city, healded_by_city, on='city', how='outer', suffixes=['_infected', '_healed'])
    covid_mk['count'] = covid_mk.count_infected
    covid_mk = pd.merge(covid_mk, dead_by_city, on='city', how='outer', suffixes=['', '_dead'])
    covid_mk.fillna(int(0), inplace=True)
    covid_mk['count'] = covid_mk.count_infected - covid_mk.count_healed - covid_mk.count_dead
    covid_mk = covid_mk.astype(int)
    covid_mk

    covid_mk_cities = mk_cities.merge(covid_mk, left_on='id', right_on='city', how='left')

    covid_mk_cities['count'] = covid_mk_cities['count'].fillna(0).astype(int)
    covid_mk_cities['count_infected'] = covid_mk_cities['count_infected'].fillna(0).astype(int)
    covid_mk_cities['count_healed'] = covid_mk_cities['count_healed'].fillna(0).astype(int)
    covid_mk_cities['count_dead'] = covid_mk_cities['count_dead'].fillna(0).astype(int)

    covid_mk_cities[['geometry', 'id', 'count', 'count_infected', 'count_healed', 'count_dead', 'population']].to_file("../../opendata/mk/covid19/maps/mk_municipalities_covid.geojson", 'GeoJSON')
    
def update_mk_covid_datasets(): 
    infected_df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=0&single=true&output=csv", names=['city', 'infected_in', 'date', 'count', 'age', 'source'], header=0)
    infected_df.to_csv('../../opendata/mk/covid19/datasets/infected_by_municipality.csv', index=False)
    
    healed_df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=757629356&single=true&output=csv", names=['city', 'date', 'count', 'age', 'source'], header=0)
    healed_df.to_csv('../../opendata/mk/covid19/datasets/recovered_by_municipality.csv', index=False)
    
    dead_df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=1754038661&single=true&output=csv", header=0, names=['city', 'date', 'count', 'age', 'source'])
    dead_df.to_csv('../../opendata/mk/covid19/datasets/dead_by_municipality.csv', index=False)

    sick_hospitals = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=480309052&single=true&output=csv", header=0, names=['hospital', "date", "count", "age_range", 'origin', 'source'])
    sick_hospitals.to_csv('../../opendata/mk/covid19/datasets/infected_by_hospital.csv', index=False)

    recovered_hospitals = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=1488187986&single=true&output=csv", header=0, names=['hospital', "date", "count", "age_range", 'source'])
    recovered_hospitals.to_csv('../../opendata/mk/covid19/datasets/recovered_by_hospital.csv', index=False)

    dead_hospitals = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=514503617&single=true&output=csv", header=0, names=['hospital', "date", "count", "age_range", 'link'])
    dead_hospitals.to_csv('../../opendata/mk/covid19/datasets/dead_by_hospital.csv', index=False)

    quarantine = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=325857359&single=true&output=csv", header=0, names=['municipality', "from", "to"])
    quarantine.to_csv('../../opendata/mk/covid19/datasets/quarantine_by_municipality.csv', index=False)

    hospitals = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=695931938&single=true&output=csv", header=0, names=['hosital', "lon", "lat"])
    hospitals.to_csv('../../opendata/mk/bolnici-hospitals/hospitals.csv', index=False)
    hospitals


    hospitals_geojson = geopandas.GeoDataFrame(hospitals, geometry=geopandas.points_from_xy(hospitals.lon, hospitals.lat))

    hospitals_geojson.to_file('../../opendata/mk/bolnici-hospitals/hospitals.geojson', 'GeoJSON')

def update_mk_covid_quarantine_geojson():
    mk_municipalities = geopandas.read_file("https://raw.githubusercontent.com/klupp/opendata/master/mk/opstini-municipalities/municipalities_mq.geojson")
    mk_cities = mk_municipalities.dissolve(by='entity_mk', aggfunc='sum')                                
    # mk_cities['entity_mk'] = mk_cities.index
    mk_cities['id'] = mk_cities.index

    quarantine_df = pd.read_csv("https://docs.google.com/spreadsheets/d/e/2PACX-1vR-Ul4NMiPvca7QH-RlYk2Q1hrVmjjGp5tr5n64l1z-SH5S2NoMeqjSd5Ulo171tHKM2Crfr7u0tpcz/pub?gid=325857359&single=true&output=csv")

    mk_cities_quarantine = mk_cities.merge(quarantine_df, left_on='entity_mk', right_on='Општина', how='inner')

    mk_cities_quarantine['dissolvefield'] = 1
    quarantine = mk_cities_quarantine.dissolve(by='dissolvefield', aggfunc='sum')

    quarantine[['geometry', 'population']].to_file("../../opendata/mk/covid19/maps/covid-quarantine.geojson", 'GeoJSON')