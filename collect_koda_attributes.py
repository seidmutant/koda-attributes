import json
import numpy as np
import requests

# {
#   "image": "https://assets.otherside.xyz/kodas/246116ea482a2923e0349f22060af31242fdd4fa5dfc41a82111a89208ee63f2.png",
#   "attributes": [
#     { "trait_type": "Head", "value": "Chomp Chomp" },
#     { "trait_type": "Eyes", "value": "Veggie" },
#     { "trait_type": "Core", "value": "Onyx Doom" },
#     { "trait_type": "Clothing", "value": "Unknown Beast Armor" },
#     { "trait_type": "Weapon", "value": "Skulds Renown" }
#   ]
# }

def parse_attributes(attribute_dict, response_json):
    
    attributes = response_json['attributes']

    for attribute in attributes:
        
        trait_type = attribute['trait_type']
        trait_value = attribute['value']

        if trait_type not in attribute_dict:
            attribute_dict[trait_type] = {}
        
        if trait_value not in attribute_dict[trait_type]:
            attribute_dict[trait_type][trait_value] = 1
        else:
            attribute_dict[trait_type][trait_value] += 1

    return attribute_dict

def run():
    
    attribute_dict = {}
    for token_id in np.arange(0, 10000):

        print (token_id)

        response = requests.get('https://api.otherside.xyz/kodas/{}'.format(token_id))
        if response.status_code == 200:
            response_json = response.json()
            parse_attributes(attribute_dict, response_json)
        
    with open('data/attribute_count.json', 'w') as f:
        json.dump(attribute_dict, f)

run()