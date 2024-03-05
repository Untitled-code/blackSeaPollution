#!/home/investigator/EnvPy/jupyter_venv/bin/python
# coding: utf-8
import os
from pathlib import Path
import csv
from time import strptime
import pandas as pd
from geojson import Feature, FeatureCollection, Point
import json

PATH = './'
files = []
concatenated = pd.DataFrame() #create empty dataframe
def date_convert(df): # froming date and unix timestamp columns
    for i in range(len(df)):
        time = df['date'][i] #getting date from a cell
        print(f"Getting date column {time}")
        time_ms = pd.Timestamp(time).timestamp()
        df.loc[i,['timestamp']] = time_ms*1000 #converting to miliseconds

for filename in os.listdir(PATH):
    if filename.endswith('db_circles.csv'):
        print(filename)
        files.append(filename)
print(files)
for filepath in files:
    print(f'Working with ...{filepath}')
    # creating dataframe from file csv
    df = pd.read_csv(filepath)
    print(df)
    del(df['timestamp']) #deleting old timestamp column
    date_convert(df)
    concatenated = pd.concat([concatenated, df])  # concate multiple tables into one


"""Converting into geojson"""

# from here https://notebook.community/captainsafia/nteract/applications/desktop/example-notebooks/pandas-to-geojson
def df_to_geojson(df, properties, lat='la', lon='lo'):
    # create a new python dict to contain our geojson data, using geojson format
    geojson = {'type':'FeatureCollection', 'features':[]}

    # loop through each row in the dataframe and convert each row to geojson format
    for _, row in df.iterrows():
        # create a feature template to fill in
        feature = {'type':'Feature',
                   'properties':{},
                   'geometry':{'type':'Point',
                               'coordinates':[]}}

        # fill in the coordinates
        feature['geometry']['coordinates'] = [row[lon],row[lat]]

        # for each column, get the value and add it as a new feature property
        for prop in properties:
            feature['properties'][prop] = row[prop]
        
        # add this feature (aka, converted dataframe row) to the list of features inside our dict
        geojson['features'].append(feature)
    
    return geojson

# cols = ['sheet_name','title','description','link', 'date','timestamp']
cols = ['weapon', 'target', 'title','description','link', 'date','timestamp']

geojson = df_to_geojson(df, cols)

with open(f'db.geojson', 'w', encoding='utf-8') as f:
    json.dump(geojson, f, ensure_ascii=False)
