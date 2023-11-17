import numpy as np
import pandas as pd
import sys
import requests

path_file =  str(sys.argv[1])

# reading file
df = pd.read_csv(path_file)

# select column
df = df[['Nom_Equipament', 'Tipus_Us', 'Tipus_Equipament', 'Ambit', 'Latitud', 'Longitud']]

# change column names
df.columns = ['names', 'use_type', 'equipment_type', 'ambit', 'latitude', 'longitude']

# drop duplicates
df = df.drop_duplicates()

# drop NaN
df = df.dropna()

# Convert DataFrame to JSON
json_data_df = df.to_json(orient='records')

# Specify the file path where you want to save the JSON data
file_path_json = path_file.replace(".csv", ".json")

# Save the JSON data to a file
with open(file_path_json, 'w') as json_file:
    json_file.write(json_data_df)

print(f'The JSON data has been saved to {file_path_json}')

# Post request
requests.post("localhost:5173/docs", json = json_data_df)