import csv
import numpy as np
import pandas as pd
import requests

from os.path import exists

# {
#   "attributes": [
#     { "trait_type": "Category", "value": "Decay" },
#     { "trait_type": "Sediment", "value": "Infinite Expanse" },
#     { "trait_type": "Sediment Tier", "value": 1, "display_type": "number" },
#     { "trait_type": "Environment", "value": "Ruins" },
#     { "trait_type": "Environment Tier", "value": 3, "display_type": "number" },
#     { "trait_type": "Eastern Resource", "value": "Lumileaf" },
#     {
#       "trait_type": "Eastern Resource Tier",
#       "value": 2,
#       "display_type": "number"
#     },
#     { "trait_type": "Southern Resource", "value": "Chroma" },
#     {
#       "trait_type": "Southern Resource Tier",
#       "value": 2,
#       "display_type": "number"
#     },
#     { "trait_type": "Western Resource", "value": "Moldium" },
#     {
#       "trait_type": "Western Resource Tier",
#       "value": 1,
#       "display_type": "number"
#     },
#     { "trait_type": "Plot", "value": 54638, "display_type": "number" }
#   ],
#   "image": "https://assets.otherside.xyz/otherdeeds/d3c053d16b9d93c2636a0c1a2f18535920047b0e9a5d25b64879fde35e44b1b9.jpg"
# }

def parse_land(token_id, response_json):
        
    koda = {
        "token_id": token_id,
        "image": response_json['image']
    }
    attributes = response_json['attributes']

    for attribute in attributes:

        koda[attribute['trait_type']] = attribute['value']         

    return koda

def get_token_ids(filename):
    """
    Return a list of token ids to process.
    """

    if exists(filename):
        df = pd.read_csv(filename)
        token_ids_saved = np.array(df['token_id'])
        return sorted(list(set(np.arange(0, 100000)) - set(token_ids_saved)))
    else:
        return np.arange(0, 100000)    

def run():

    filename = "data/kodas.csv"
    token_ids = get_token_ids(filename)
    
    with open(filename, "a") as f:

        writer = csv.writer(f)
        if not exists(filename):
            header = ['token_id', 'image', 'category', 'sediment', 'sediment_tier', 'environment', 'environment_tier',
                'eastern', 'eastern_tier', 'southern', 'southern_tier', 'western', 'western_tier', 'northern', 'northern_tier',
                'artifact', 'plot', 'koda'
            ]            
            writer.writerow(header)  

        for token_id in token_ids:

            print (token_id)

            response = requests.get('https://api.otherside.xyz/lands/{}'.format(token_id))
            if response.status_code == 200:
                response_json = response.json()
                land = parse_land(token_id, response_json)

                row = [
                    land['token_id'],
                    land['image'],
                    land.get('Category', None),
                    land.get('Sediment', None),
                    land.get('Sediment Tier', None),
                    land.get('Environment', None),
                    land.get('Environment Tier', None),
                    land.get('Eastern Resource', None),
                    land.get('Eastern Resource Tier', None),
                    land.get('Southern Resource', None),
                    land.get('Southern Resource Tier', None),
                    land.get('Western Resource', None),
                    land.get('Western Resource Tier', None),
                    land.get('Northern Resource', None),
                    land.get('Northern Resource Tier', None),                    
                    land.get('Artifact', None),
                    land.get('Plot', None),
                    land.get('Koda', None)
                ]
                writer.writerow(row)

run()