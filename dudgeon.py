import os
from azure.storage.blob import BlobServiceClient, BlobClient
from dotenv import load_dotenv
import pandas as pd
from download_files import DATA_DIR
import math
import numpy as np
from geopy.distance import distance, lonlat
load_dotenv()

coords_path = os.path.join(DATA_DIR, 'Dudgeon_coordinates.csv')
dataframe = pd.read_csv(coords_path, sep=";")

ANCHOR_LAT = 53.212322
ANCHOR_LON = 1.319792
anchor_lonlat = lonlat(ANCHOR_LON, ANCHOR_LAT)

def get_name_spesific(raw_name):
    return raw_name.split('-')[-1]

degree_to_meter_factor = 111100


def haversine_distance(lat1, lon1, lat2, lon2, unit='K'):
        r = 6371009  # radius of the earth in meters
        if unit == 'M':
            r = 3960  # radius of the earth in miles
        dLat = np.radians(lat2 - lat1)
        dLon = np.radians(lon2 - lon1)
        a = np.sin(dLat / 2) * np.sin(dLat / 2) + \
            np.cos(np.radians(lat1)) * np.cos(np.radians(lat2)) * \
        np.sin(dLon / 2) * np.sin(dLon / 2)
        c = 2 * np.arctan2(np.sqrt(a), np.sqrt(1 - a))
        distance = r * c
        return distance

def get_distance_from_names(a:str, b:str):

    lat_a = dataframe.loc[dataframe['Asset'] == 'DOW-'+a].iloc[0]['Latitude']
    lon_a = dataframe.loc[dataframe['Asset'] == 'DOW-'+a].iloc[0]['Longitude']
    lat_b = dataframe.loc[dataframe['Asset'] == 'DOW-'+b].iloc[0]['Latitude']
    lon_b = dataframe.loc[dataframe['Asset'] == 'DOW-'+b].iloc[0]['Longitude']

    dist = haversine_distance(lat1=lat_a, lon1=lon_a, lat2=lat_b, lon2=lon_b)
    return dist

def get_x_distance_from_anchor(lon):
     x = haversine_distance(lat1=ANCHOR_LAT, lon1=ANCHOR_LON, lat2=ANCHOR_LAT, lon2=lon)
     return x

def get_y_distance_from_anchor(lat):
     y = haversine_distance(lat1=ANCHOR_LAT, lon1=ANCHOR_LON, lat2=lat, lon2=ANCHOR_LON)
     return y

def get_x_desic_distance_from_anchor(lon):
     lon_lat = lonlat(lon, ANCHOR_LAT)
     x = distance(anchor_lonlat, lon_lat)
     return x

def get_y_desic_distance_from_anchor(lat):
     lon_lat = lonlat(ANCHOR_LON, lat)
     y = distance(anchor_lonlat, lon_lat)
     return y



NAMES = dataframe['Asset'].apply(get_name_spesific).to_numpy()
x = []
y = []
for lat, lon in zip(dataframe['Latitude'].to_numpy(), dataframe['Longitude'].to_numpy()):
     x.append(get_x_desic_distance_from_anchor(lon=lon).meters)
     y.append(get_y_desic_distance_from_anchor(lat=lat).meters)
WT_X = np.array(x)
WT_Y = np.array(y)

WT_X_HAV = get_x_distance_from_anchor(dataframe['Longitude'].to_numpy())
WT_Y_HAV= get_y_distance_from_anchor(dataframe['Latitude'].to_numpy())
