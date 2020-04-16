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
    MONTHS = tuple(table_cols[6:])

    # Constant number of rows in the tables
    ROWS = len(table_cols)
    
    # Init dict
    fishes={}

    base_url = 'https://animalcrossing.fandom.com'

    for i, fish in enumerate(n_table.find_all('td')):
        curr_col = i%ROWS

        if curr_col == 0:               # Name
            # print(curr_col, fish)
            name = fish.a.text.strip().lower().replace(' ', '').replace('-','')
            fishes[name] = {}
            details_uri = fish.a['href']
            fishes[name]['details_link'] = base_url + details_uri
            
        elif curr_col == 1:             # Image
            # print(curr_col, fish)
            img_link = fish.a['href']
            fishes[name]['image'] = img_link

        elif curr_col == 2:             # Price
            # print(curr_col, fish)
            price = int(fish.text.strip())
            fishes[name]['nook_price'] = price
            fishes[name]['cj_price'] = int(price*1.5)

        elif curr_col == 3:             # Location
            # print(curr_col, fish)
            location = fish.text.strip()
            fishes[name]['location'] = location

        elif curr_col == 4:             # Shadow size
            # print(curr_col, fish)
            shadow = fish.text.strip()
            fishes[name]['shadow_size'] = shadow

        elif curr_col == 5:             # Time
            # print(curr_col, fish)
            time = fish.small.text.strip()
            fishes[name]['active_hours'] = time
            fishes[name]['months_available'] = {'northern': [], 'southern': []}
            fishes[name]['months_unavailable'] = {'northern': [], 'southern': []}

        elif curr_col == 6:             # Months
            n_fish_months = n_table.find_all('td')[i:i+11]
            s_fish_months = s_table.find_all('td')[i:i+11]
            
            # Northern Hemisphere
            for x, month in enumerate(n_fish_months):
                if month.text.strip() == '-':
                    fishes[name]['months_unavailable']['northern'].append(MONTHS[x])
                else:
                    fishes[name]['months_available']['northern'].append(MONTHS[x])
            
            # Southern Hemisphere
            for x, month in enumerate(s_fish_months):
                if month.text.strip() == '-':
                    fishes[name]['months_unavailable']['southern'].append(MONTHS[x])
                else:
                    fishes[name]['months_available']['southern'].append(MONTHS[x])
        else:
            pass
    with open('json/fish.json', 'w') as f:
        json.dump(fishes, f)

def scrape_bugs():
    pass

if __name__ == '__main__':
    scrape_fish()
    # scrape_bugs()
