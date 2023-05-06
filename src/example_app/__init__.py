from flask import Flask, request
import pandas as pd
import numpy as np
import json
from flask_cors import CORS, cross_origin

app = Flask(__name__)
CORS(app)

distances = pd.read_csv('distances.csv')
distances.loc[distances['Common_Name'].isna(), 'Common_Name'] = distances['Latin_Name']
# subset = pd.read_csv('subset.csv')
# df = pd.read_csv('df.csv')

flag_cols = ['site_part_shade',
       'site_shade', 'site_sun', 'soil_clay', 'soil_loam', 'soil_many',
       'soil_rock', 'soil_sand', 'habitat_buds/greens', 'habitat_cover',
       'habitat_fruit', 'habitat_nesting', 'habitat_pollinator', 'water_low',
       'water_moderate', 'water_none', 'loc_garden', 'loc_potted_plant',
       'loc_roof', 'loc_sidewalk']

meta_cols = ['Latin_Name', 'Common_Name', 'Climate_Appropriate_Plants', 'Plant_Type', 'Suitable_Site_Conditions', 'Size_at_Maturity', 'Plant_Communities']


def get_subset(query):
  subset = distances
#   print(subset.columns)
  if 'type' in query:
    subset = distances[distances['Plant_Type']==query['type']]
  if 'size' in query:
    subset = subset[subset['Size_at_Maturity']==query['size']]
  if 'site_part_shade' in query:
    subset = subset[subset['site_part_shade']==1]
  if 'site_shade' in query:
    subset = subset[subset['site_shade']==1]
  if 'site_sun' in query:
    subset = subset[subset['site_sun']==1]
  if 'soil_loam' in query:
    subset = subset[subset['soil_loam']==1]
  if 'soil_many' in query:
    subset = subset[subset['soil_many']==1]
  if 'soil_rock' in query:
    subset = subset[subset['soil_rock']==1]
  if 'soil_sand' in query:
    subset = subset[subset['soil_sand']==1]
  if 'habitat_buds/greens' in query:
    subset = subset[subset['habitat_buds/greens']==1]
  if 'habitat_cover' in query:
    subset = subset[subset['habitat_cover']==1]
  if 'habitat_fruit' in query:
    subset = subset[subset['habitat_fruit']==1]
  if 'habitat_nesting' in query:
    subset = subset[subset['habitat_nesting']==1]
  if 'habitat_pollinator' in query:
    subset = subset[subset['habitat_pollinator']==1]
  if 'water_low' in query:
    subset = subset[subset['water_low']==1]
  if 'water_moderate' in query:
    subset = subset[subset['water_moderate']==1]
  if 'water_none' in query:
    subset = subset[subset['water_none']==1]
  if 'loc_garden' in query:
    subset = subset[subset['loc_garden']==1]
  if 'water_low' in query:
    subset = subset[subset['water_low']==1]
  if 'loc_potted_plant' in query:
    subset = subset[subset['loc_potted_plant']==1]
  if 'loc_roof' in query:
    subset = subset[subset['loc_roof']==1]
  if 'loc_sidewalk' in query:
    subset = subset[subset['loc_sidewalk']==1]
    

# Plant_Communities,,,,,,,,,,,,,,,,,,,,

#   print("Len", len(subset))
  native_indices = np.where(subset['Climate_Appropriate_Plants']=="CA Native")[0].astype(str)
  exotic_indices = np.where(subset['Climate_Appropriate_Plants']!="CA Native")[0].astype(str)

  native_labels = list(subset.iloc[native_indices]['Common_Name'])
  exotic_labels = list(subset.iloc[exotic_indices]['Common_Name'])

  

  subset = subset.iloc[exotic_indices]
  subset = subset[native_indices]
  for col in flag_cols:
    # print(distances.iloc[exotic_indices][col])
    subset[col] = list(distances.iloc[exotic_indices][col])
  subset['plant_type'] = list(distances.iloc[exotic_indices]['Plant_Type'])
  subset['size'] = list(distances.iloc[exotic_indices]['Size_at_Maturity'])
  subset['name'] = list(distances.iloc[exotic_indices]['Common_Name'])
  subset['latin'] = list(distances.iloc[exotic_indices]['Latin_Name'])

  # return subset.columns

  data = []
  for i, row in subset.iterrows():
      r = {}
      # print(row)
      r['key'] = row['name']
      r['value'] = []
      for col in subset.columns:
        if col.isnumeric():
            # print(row[1][col])
            r['value'].append(row[col])
        # if col == 'name':
            # print(row[1])

      data.append(r)

  return {"data": data, "native_labels": list(native_labels), "exotic_labels": list(exotic_labels)}

@app.route('/')
def hello():
  return "Hello bro"

@app.route('/get-json')
def getjson():
    args = request.args.to_dict()
    # print( get_subset(args))
    # return "success"
    return get_subset(args)

if __name__ == "__main__":
    # for debugging locally
    app.run(debug=True, host='0.0.0.0',port=5000)

    # for production
    # app.run(host='0.0.0.0', port=3200)