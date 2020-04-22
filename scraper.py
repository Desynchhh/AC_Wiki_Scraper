from bs4 import BeautifulSoup
import requests
import json

def scrape_fish():
    # Get source data
    source = requests.get('https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)').text
    soup = BeautifulSoup(source, 'lxml')

    # Get 'Northern Hemisphere' table data
    n_table_div = soup.find('div', title='Northern Hemisphere')
    n_table = n_table_div.table.table

    # Get 'Southern Hemisphere' table data
    s_table_div = soup.find('div', title='Southern Hemisphere')
    s_table = s_table_div.table.table

    # Get the columns and names in the tables
    table_cols = [col.text.strip() for col in n_table.find_all('th')]
    months = tuple(table_cols[6:])

    # Constant number of rows in the tables
    rows = len(table_cols)
    
    # Init dict
    fishes={}

    base_url = 'https://animalcrossing.fandom.com'

    for i, fish in enumerate(n_table.find_all('td')):
        curr_col = i%rows

        if curr_col == 0:               # Name
            name = fish.a.text.strip().lower().replace(' ', '').replace('-','')
            details_uri = fish.a['href']
            fishes[name] = {'details_link': base_url + details_uri}
        elif curr_col == 1:             # Image
            img_link = fish.a['href']
            fishes[name]['image'] = img_link

        elif curr_col == 2:             # Price
            price = int(fish.text.strip())
            fishes[name]['nook_price'] = price
            fishes[name]['cj_price'] = int(price*1.5)

        elif curr_col == 3:             # Location
            location = fish.text.strip()
            fishes[name]['location'] = location

        elif curr_col == 4:             # Shadow size
            shadow = fish.text.strip()
            fishes[name]['shadow_size'] = shadow

        elif curr_col == 5:             # Time
            time = fish.small.text.strip()
            fishes[name]['active_hours'] = time

        elif curr_col == 6:             # Months
            # Prep dict with arrays for both hemispheres
            fishes[name]['months_available'] = {'northern': [], 'southern': []}
            fishes[name]['months_unavailable'] = {'northern': [], 'southern': []}

            # Handle all months in one loop iterations (with nested loops)
            n_months = n_table.find_all('td')[i:i+12]
            s_months = s_table.find_all('td')[i:i+12]
            
            # Northern Hemisphere
            for x, month in enumerate(n_months):
                if month.text.strip() == '-':
                    fishes[name]['months_unavailable']['northern'].append(months[x])
                else:
                    fishes[name]['months_available']['northern'].append(months[x])
            
            # Southern Hemisphere
            for x, month in enumerate(s_months):
                if month.text.strip() == '-':
                    fishes[name]['months_unavailable']['southern'].append(months[x])
                else:
                    fishes[name]['months_available']['southern'].append(months[x])

    with open('json/fish.json', 'w') as f:
        json.dump(fishes, f)


def scrape_bugs():
    # Get data from wiki
    source = requests.get('https://animalcrossing.fandom.com/wiki/Bugs_(New_Horizons)').text
    soup = BeautifulSoup(source, 'lxml')
    
    # Get table divs for ease of access
    n_table_div = soup.find(title="Northern Hemisphere")
    s_table_div = soup.find(title="Southern Hemisphere")

    # Get tables for even more ease of access
    n_table = n_table_div.table.table
    s_table = s_table_div.table.table

    # Table header names
    table_cols = [col.text.strip() for col in n_table.find_all('th')]
    
    months = table_cols[5:]
    rows = len(table_cols)

    # Init dict
    bugs={}

    base_url = 'https://animalcrossing.fandom.com'

    for i, bug in enumerate(n_table.find_all('td')):
        curr_col = i%rows
        
        if curr_col == 0:               # Name
            name = bug.a.text.strip().lower().replace(' ', '').replace('-','')
            details_uri = bug.a['href']
            bugs[name] = { 'details_link': base_url + details_uri }
        
        elif curr_col == 1:             # Image
            img_link = bug.a['href']
            bugs[name]['image'] = img_link
        
        elif curr_col == 2:             # Price
            price = int(bug.text.strip())
            bugs[name]['nook_price'] = price
            bugs[name]['flick_price'] = int(price*1.5)
       
        elif curr_col == 3:             # Location
            location = bug.text.strip()
            bugs[name]['location'] = location
        
        elif curr_col == 4:             # Time
            time = bug.small.text.strip()
            bugs[name]['active_hours'] = time
       
        elif curr_col == 5:             # Months
            # Prep dict with arrays for both hemispheres
            bugs[name]['months_available'] = { 'northern': [], 'southern': [] }
            bugs[name]['months_unavailable'] = { 'northern': [], 'southern': [] }

            # Handle all months in one loop iteration
            n_months = n_table.find_all('td')[i:i+12]
            s_months = s_table.find_all('td')[i:i+12]

            # Northern Hemisphere
            for x, month in enumerate(n_months):
                if month.text.strip() == '-':
                    bugs[name]['months_unavailable']['northern'].append(months[x])
                else:
                    bugs[name]['months_available']['northern'].append(months[x])

            for x, month in enumerate(s_months):
                if month.text.strip() == '-':
                    bugs[name]['months_unavailable']['southern'].append(months[x])
                else:
                    bugs[name]['months_available']['southern'].append(months[x])

    with open('json/bugs.json', 'w') as f:
        json.dump(bugs, f)



def run_scraper():
    scrape_fish()
    scrape_bugs()