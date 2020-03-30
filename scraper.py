from bs4 import BeautifulSoup
import requests
import json

def method_1():
    source = requests.get('https://animalcrossing.fandom.com/wiki/Fish_(New_Horizons)').text
    soup = BeautifulSoup(source, 'lxml')

    n_table_div = soup.find('div', title='Northern Hemisphere')
    n_table = n_table_div.table.table

    s_table_div = soup.find('div', title='Southern Hemisphere')
    s_table = s_table_div.table.table

    table_cols = [col.text.strip() for col in n_table.find_all('th')]

    ROWS = len(table_cols)
    row_counter = 1
    fishes = {"northern": {}, "southern": {}}
    for fish in n_table.find_all('td'):
        expr = row_counter%ROWS
        if expr == 1:   # Name
            name = fish.a.text.strip()
            fishes['northern'][name] = {}
        elif expr == 2: # Image
            image = fish.a['href']
            fishes['northern'][name]['image'] = image
        elif expr == 3: # Price
            price = fish.text.strip()
            fishes['northern'][name]['price'] = price
        elif expr == 4: # Location
            location = fish.text.strip()
            fishes['northern'][name]['location'] = location
        elif expr == 5: # Shadow
            shadow = fish.text.strip()
            fishes['northern'][name]['shadow_size'] = shadow
        elif expr == 6: # Time
            time = fish.small.text.strip()
            fishes['northern'][name]['time'] = time
            fishes['northern'][name]['available_in'] = []
            fishes['northern'][name]['unavailable_in'] = []
        else:           # Months
            if fish.text.strip() == '✓':   # Catchable
                fishes['northern'][name]['available_in'].append(table_cols[row_counter%len(table_cols)-1])
            else:                          # Uncatchable
                fishes['northern'][name]['unavailable_in'].append(table_cols[row_counter%len(table_cols)-1])
        row_counter+=1
    row_counter = 1
    for fish in s_table.find_all('td'):
        expr = row_counter%ROWS
        if expr == 1:   # Name
            name = fish.a.text.strip()
            fishes['southern'][name] = {}
        elif expr == 2: # Image
            image = fish.a['href']
            fishes['southern'][name]['image'] = image
        elif expr == 3: # Price
            price = fish.text.strip()
            fishes['southern'][name]['price'] = price
        elif expr == 4: # Location
            location = fish.text.strip()
            fishes['southern'][name]['location'] = location
        elif expr == 5: # Shadow
            shadow = fish.text.strip()
            fishes['southern'][name]['shadow_size'] = shadow
        elif expr == 6: # Time
            time = fish.small.text.strip()
            fishes['southern'][name]['time'] = time
            fishes['southern'][name]['available_in'] = []
            fishes['southern'][name]['unavailable_in'] = []
        else:           # Months
            if fish.text.strip() == '✓':   # Catchable
                fishes['southern'][name]['available_in'].append(table_cols[row_counter%len(table_cols)-1])
            else:                          # Uncatchable
                fishes['southern'][name]['unavailable_in'].append(table_cols[row_counter%len(table_cols)-1])
        row_counter+=1

    with open(f'json/fish.json', 'w') as f:
        json.dump(fishes, f)

def method_2():
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

    # Constant number of rows in the tables
    ROWS = len(table_cols)
    
    # Get <tr> tags from the tables (1st <tr> are the table headers)
    n_table_rows = n_table.find_all('tr')[1:]
    s_table_rows = s_table.find_all('tr')[1:]
    
    # Init dict
    fishes={}

    print(n_table_rows)

    for fish in n_table_rows:
        for i, td in enumerate(fish):
            with open('test.txt', 'w', encoding='utf-8') as f:
                f.write(str(i))
                f.write(str(fish))
            break
        break

    # Get all data on each fish
    # for i, fish in enumerate(n_table_rows):
    #     expr = i%ROWS
    #     print(fish)
    #     if expr == 1:   # Name
    #         name = fish.td.a.text.strip()
        # elif expr == 2: # Image
        #     fishes[name]['image'] = fish.a['href']
        #     print(fishes[name])
        # elif expr == 3: # Price
        #     fishes[name]['price'] = fish.text.strip()
        #     print(fishes[name])
        # elif expr == 4: # Location
        #     fishes[name]['location'] = fish.text.strip()
        #     print(fishes[name])
        # elif expr == 5: # Shadow
        #     fishes[name]['shadow_size'] = fish.text.strip()
        #     print(fishes[name])
        # elif expr == 6: # Time
        #     fishes[name]['time'] = fish.small.text.strip()
        #     print(fishes[name])
        # elif expr == 7: # Months
        #     pass
        # else:
        #     pass
        # if i >= ROWS:
        #     break
    # print(fishes)
        



if __name__ == '__main__':
    # method_1()
    method_2()
    pass
