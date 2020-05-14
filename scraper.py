from bs4 import BeautifulSoup
import requests, json, os, re

base_url = 'https://animalcrossing.fandom.com'


def scrape_fish():
    """Scrapes the ACNH Wiki for various data on the game's fish and saves the data in a JSON file."""
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

    # Constant number of cols in the tables
    cols = len(table_cols)
    
    # Init dict
    fishes={}

    for i, fish in enumerate(n_table.find_all('td')):
        curr_col = i%cols

        if curr_col == 0:               # Name
            name = fish.a.text.strip()
            cur_fish = name.lower()
            details_link = base_url + fish.a['href']
            quote = scrape_quote(name, details_link)
            fishes[cur_fish] = {
                'name': name,
                'details_link': details_link,
                'catchquote': quote    
            }
        
        elif curr_col == 1:             # Image
            img_link = fish.a['href']
            fishes[cur_fish]['image'] = img_link

        elif curr_col == 2:             # Price
            price = int(fish.text.strip().replace(',',''))
            fishes[cur_fish]['nook_price'] = price
            fishes[cur_fish]['cj_price'] = int(price*1.5)

        elif curr_col == 3:             # Location
            location = fish.text.strip()
            fishes[cur_fish]['location'] = location

        elif curr_col == 4:             # Shadow size
            shadow = fish.text.strip()
            fishes[cur_fish]['shadow_size'] = shadow

        elif curr_col == 5:             # Time
            time = fish.small.text.strip()
            fishes[cur_fish]['active_hours'] = time

        elif curr_col == 6:             # Months
            # Prep dict with arrays for both hemispheres
            fishes[cur_fish]['months_available'] = {'northern': [], 'southern': []}
            fishes[cur_fish]['months_unavailable'] = {'northern': [], 'southern': []}

            # Handle all months in one loop iterations (using nested loops)
            n_months = n_table.find_all('td')[i:i+12]
            s_months = s_table.find_all('td')[i:i+12]
            
            # Northern Hemisphere
            for x, month in enumerate(n_months):
                if month.text.strip() == '-':
                    fishes[cur_fish]['months_unavailable']['northern'].append(months[x])
                else:
                    fishes[cur_fish]['months_available']['northern'].append(months[x])
            
            # Southern Hemisphere
            for x, month in enumerate(s_months):
                if month.text.strip() == '-':
                    fishes[cur_fish]['months_unavailable']['southern'].append(months[x])
                else:
                    fishes[cur_fish]['months_available']['southern'].append(months[x])

    with open('json/fish.json', 'w') as f:
        json.dump(fishes, f)


def scrape_bugs():
    """Scrapes the ACNH Wiki for various data on the game's fish and saves the data in a JSON file."""
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
    cols = len(table_cols)

    # Init dict
    bugs={}

    for i, bug in enumerate(n_table.find_all('td')):
        curr_col = i%cols
        
        if curr_col == 0:               # Name
            name = bug.a.text.strip()
            cur_bug = name.lower()
            details_link = base_url + bug.a['href']
            quote = scrape_quote(name, details_link)
            
            bugs[cur_bug] = {
                'name': name,
                'details_link': details_link,
                'catchquote': quote
            }
        
        elif curr_col == 1:             # Image
            img_link = bug.a['href']
            bugs[cur_bug]['image'] = img_link
        
        elif curr_col == 2:             # Price
            price = int(bug.text.strip().replace(',',''))
            bugs[cur_bug]['nook_price'] = price
            bugs[cur_bug]['flick_price'] = int(price*1.5)
       
        elif curr_col == 3:             # Location
            location = bug.text.strip()
            bugs[cur_bug]['location'] = location
        
        elif curr_col == 4:             # Time
            time = bug.small.text.strip()
            bugs[cur_bug]['active_hours'] = time
       
        elif curr_col == 5:             # Months
            # Prep dict with arrays for both hemispheres
            bugs[cur_bug]['months_available'] = { 'northern': [], 'southern': [] }
            bugs[cur_bug]['months_unavailable'] = { 'northern': [], 'southern': [] }

            # Handle all months in one loop iteration
            n_months = n_table.find_all('td')[i:i+12]
            s_months = s_table.find_all('td')[i:i+12]

            # Northern Hemisphere
            for x, month in enumerate(n_months):
                if month.text.strip() == '-':
                    bugs[cur_bug]['months_unavailable']['northern'].append(months[x])
                else:
                    bugs[cur_bug]['months_available']['northern'].append(months[x])

            for x, month in enumerate(s_months):
                if month.text.strip() == '-':
                    bugs[cur_bug]['months_unavailable']['southern'].append(months[x])
                else:
                    bugs[cur_bug]['months_available']['southern'].append(months[x])

    with open('json/bugs.json', 'w') as f:
        json.dump(bugs, f)


def scrape_quote(critter_name:str, details_link:str):
    no_quote = 'The catch quote for this critter is not yet available on the wiki. Sorry.'
    source = requests.get(details_link).text
    soup = BeautifulSoup(source, 'lxml')
    header = soup.find(None, {'id': 'New_Horizons'})
    try:
        table = header.find_next('table').table
        quote = table.find_next('td').text.strip()
        quote = re.sub(r'[\\"“”]', '', quote)
        if critter_name.lower() not in quote.lower():
            quote = no_quote
    except:
        quote = no_quote
    return quote


# def scrape_quotes():
#     no_quote = 'The catch quote for this critter is not yet available on the wiki. Sorry.'
#     for fj in os.listdir('json'):
#         if fj.endswith('.json'):
#             with open(f'json/{fj}', 'r') as f:
#                 data = json.load(f)
            
#             for _, critter in data.items():
#                 print(critter['name'])
#                 source = requests.get(critter['details_link']).text
#                 soup = BeautifulSoup(source, 'lxml')
#                 print(soup.find_all(None, {'id': 'New_Horizons'}))
#                 header = soup.find(None, {'id': 'New_Horizons'})
#                 try:
#                     table = header.find_next('table').table
#                     quote = table.find_next('td').text.strip().replace('"','')
#                     if critter['name'].lower() not in quote.lower():
#                         quote = no_quote
#                 except:
#                     quote = no_quote
#                 print(quote)
#                 print()



async def run_scraper():
    """Runs all 'scrape' functions, as well as ensuring the JSON file exists."""
    if not os.path.exists('./json'):
        os.mkdir('json')
    scrape_fish()
    scrape_bugs()