import json

FILEPATH = 'json/'

def get_critter(filename, critter_name, hemisphere='northern'):
    critter_name = critter_name.strip().lower().replace(' ','').replace('-','')
    with open(f'{FILEPATH}/{filename}.json', 'r') as f:
        data = json.load(f)
    if critter_name in data:
        return data[critter_name]
    else:
        return None