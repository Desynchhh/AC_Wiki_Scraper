import json, os
from datetime import datetime

FILEPATH = 'json'
MONTHS = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

def get_critter(filename:str, critter_name:str):
    """Gets the specified critter in it's respective JSON file. Returns None if it doesn't exist.

    :type filename: str
    :type critter_name: str
    :rtype: dict, None
    """
    critter_name = critter_name.strip().lower()
    with open(os.path.join(FILEPATH, f'{filename}.json'), 'r') as f:
        data = json.load(f)
    if critter_name in data:
        return data[critter_name]
    else:
        return None


def get_monthly_critters(filename:str, hemisphere:str, month_period:int=-1) -> dict:
    """Gets all of the given critter type available in a 3 month period.

    :type filename: str
    :type hemisphere: str
    :type month_period: int, optional
    :rtype: dict
    """
    this_month = MONTHS[datetime.now().month+month_period]
    prev_month = MONTHS[datetime.now().month-1+month_period]
    next_month = MONTHS[datetime.now().month+1+month_period]
    
    with open(os.path.join(FILEPATH, f'{filename}.json'), 'r') as f:
        data = json.load(f)

    monthly_critters = [critter for _, critter in data.items() if this_month in critter['months_available'][hemisphere]]
    
    new_critters = [critter for critter in monthly_critters if prev_month not in critter['months_available'][hemisphere]]
    recurring_critters = [critter for critter in monthly_critters if critter not in new_critters]
    leaving_critters = [critter for critter in monthly_critters if next_month not in critter['months_available'][hemisphere]]

    if len(new_critters) <= 0:
        new_critters = f'No new {filename} have appeared in {this_month}'
    else:
        new_critters = ", ".join([critter['name'] for critter in new_critters])

    if len(recurring_critters) <= 0:
        recurring_critters = f'No {filename} have stayed since {prev_month}'
    else:
        recurring_critters = ", ".join([critter['name'] for critter in recurring_critters])

    if len(leaving_critters) <= 0:
        leaving_critters = f'No {filename} will be leaving in {next_month}'
    else:
        leaving_critters = ", ".join([critter['name'] for critter in leaving_critters])

    return {
        'prev_month': prev_month,
        'this_month': this_month,
        'next_month': next_month,
        'recurring_critters': recurring_critters,
        'new_critters': new_critters,
        'leaving_critters': leaving_critters
    }
