import json
from datetime import datetime

FILEPATH = 'json/'
MONTHS = ['Jan','Feb','Mar','Apr','May','Jun','Jul','Aug','Sep','Oct','Nov','Dec']

def get_critter(filename:str, critter_name:str, hemisphere:str):
    critter_name = critter_name.strip().lower().replace(' ','').replace('-','')
    with open(f'{FILEPATH}/{filename}.json', 'r') as f:
        data = json.load(f)
    if critter_name in data:
        return data[critter_name]
    else:
        return None


def get_monthly_critters(filename:str, hemisphere:str, month_period:int=-1):
    month = MONTHS[datetime.now().month+month_period]
    with open(f'{FILEPATH}/{filename}.json', 'r') as f:
        data = json.load(f)
    critters = [critter['name'] for _, critter in data.items() if month in critter['months_available'][hemisphere]]
    return critters