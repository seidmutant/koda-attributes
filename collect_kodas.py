import csv
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

def parse_koda(token_id, response_json):
        
    koda = {
        "token_id": token_id,
        "image": response_json['image']
    }
    attributes = response_json['attributes']

    for attribute in attributes:

        koda[attribute['trait_type']] = attribute['value']         

    return koda

def run():

     with open("data/kodas.csv", "a") as kodas_file:

        writer = csv.writer(kodas_file)
        header = ['token_id', 'image', 'head', 'eyes', 'core', 'clothing', 'weapon']
        writer.writerow(header)         

        for token_id in np.arange(0, 10000):

            print (token_id)

            response = requests.get('https://api.otherside.xyz/kodas/{}'.format(token_id))
            if response.status_code == 200:
                response_json = response.json()
                koda = parse_koda(token_id, response_json)

                row = [
                    koda['token_id'],
                    koda['image'],
                    koda.get('Head', None),
                    koda.get('Eyes', None),
                    koda.get('Core', None),
                    koda.get('Clothing', None),
                    koda.get('Weapon', None)
                ]
                writer.writerow(row)

run()