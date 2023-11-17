import numpy as np
import pandas as pd
import geopandas as gpd
import utm as utm
import re as re
import sys
import requests

path_file = str(sys.argv[1])

# reading file
gdf = gpd.read_file(path_file)

def to_arr(cor):
    polygon_string = f"{cor}"

    # Extracting coordinates from the string using regular expression
    coord_pattern = re.compile(r'(\d+\.\d+) (\d+\.\d+)')
    coordinates = coord_pattern.findall(polygon_string)

    # Converting coordinates to array of arrays
    array_of_arrays = [[float(x), float(y)] for x, y in coordinates]

    # Converting coordinates from UTM to longitud/latitud
    ar = []
    for cor in array_of_arrays:
        ar.append(utm.to_latlon(cor[0], cor[1], 31, 'T'))
    return np.array(ar)

# Apply function on each row
gdf["coordinates"] = gdf["geometry"].apply(lambda x: to_arr(x))

# Select columns
gdf = gdf[['DN', 'coordinates']]

# Change column names
gdf.columns = ['dn', 'coordinates']

# Convert DataFrame to JSON
json_data_gdf = gdf.to_json(orient='records')

# Specify the file path where you want to save the JSON data
file_path_json = path_file.replace(".gpkg", ".json")

# Save the JSON data to a file
with open(file_path_json, 'w') as json_file:
    json_file.write(json_data_gdf)

# Post request
requests.post("localhost:5173/docs", json = json_data_gdf)