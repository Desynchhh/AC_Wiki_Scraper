from bs4 import BeautifulSoup
import requests, json, os, re, time, concurrent.futures

base_url = "https://nookipedia.com"
months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

def scrape_fish():
    source = requests.get("https://nookipedia.com/wiki/Fish/New_Horizons").text
    soup = BeautifulSoup(source, 'lxml')

    table = soup.find('div', class_='mw-collapsible-content').table

    table_cols = [th.text.strip() for th in table.find_all('th')]

    cols = len(table_cols)
    fishes = {}

    for i, fish in enumerate(table.find_all('td')):
        curr_col = i%cols

        if curr_col == 0:   # ID
            continue
        
        elif curr_col == 1:   # Name
            name = fish.a.text.strip()
            curr_fish = name.lower()
            details_link = base_url + fish.a.get('href')
            fishes[curr_fish] = {
                'name': name,
                'details_link': details_link
            }
            
        elif curr_col == 2:   # Img
            continue
        
        elif curr_col == 3:   # Price
            raw_price = fish.text.strip()
            price = int(re.sub(r'\D', '', raw_price))
            fishes[curr_fish]['nook_price'] = price
            fishes[curr_fish]['cj_price'] = int(price*1.5)
            continue
        
        elif curr_col == 4:   # Shadow
            shadow = fish.img['alt']
            fishes[curr_fish]['shadow_size'] = shadow
            continue
        
        elif curr_col == 5:   # Location
            location = fish.a.text.strip()
            fishes[curr_fish]['location'] = location
            continue
        
        elif curr_col == 6:   # Time
            active_hours = fish.text.strip()
            fishes[curr_fish]['active_hours'] = active_hours
            continue
        
        elif curr_col == 7:   # Months
            fishes[curr_fish]['months_available'] = {'northern': [], 'southern': []}
            fishes[curr_fish]['months_unavailable'] = {'northern': [], 'southern': []}
            n, s = handle_months(fish)
            
            for k, m in enumerate(months):
                if n[k][1] is True:
                    fishes[curr_fish]['months_available']['northern'].append(m)
                else:
                    fishes[curr_fish]['months_unavailable']['northern'].append(m)
                
                if s[k][1] is True:
                    fishes[curr_fish]['months_available']['southern'].append(m)
                else:
                    fishes[curr_fish]['months_unavailable']['southern'].append(m)
            continue
        
        elif i == 8:    # Rarity
            continue

        elif i == 9:    # Total Catches
            continue

        # if i >= 10:  # Done with 1st fish (Used for testing purposes)
        #     break

    with concurrent.futures.ThreadPoolExecutor() as executor:
        detail_links = tuple(fish['details_link'] for fish in fishes.values())
        results = executor.map(scrape_quote, detail_links)

        fish_keys = list(fishes)
        for i, result in enumerate(results):
            fishes[fish_keys[i]]['catchquote'] = result

    with open(os.path.join('json', 'fish.json'), 'w') as f:
        json.dump(fishes, f)


def scrape_bugs():
    source = requests.get("https://nookipedia.com/wiki/Bugs/New_Horizons").text
    soup = BeautifulSoup(source, 'lxml')

    table = soup.find('div', class_='mw-collapsible-content').table

    table_cols = [th.text.strip() for th in table.find_all('th')]

    cols = len(table_cols)
    bugs = {}

    for i, bug in enumerate(table.find_all('td')):
        curr_col = i%cols

        if curr_col == 0:   # ID
            continue
        
        elif curr_col == 1:   # Name
            name = bug.a.text.strip()
            curr_bug = name.lower()
            details_link = base_url + bug.a.get('href')
            bugs[curr_bug] = {
                'name': name,
                'details_link': details_link
            }
            continue

        elif curr_col == 2:   # Img
            continue
        
        elif curr_col == 3:   # Price
            raw_price = bug.text.strip()
            price = int(re.sub(r'\D', '', raw_price))
            bugs[curr_bug]['nook_price'] = price
            bugs[curr_bug]['flick_price'] = int(price*1.5)
            continue
        
        elif curr_col == 4:   # Rarity
            rarity = bug.text.strip()
            bugs[curr_bug]['rarity'] = rarity
            continue
        
        elif curr_col == 5:   # Size
            continue
        
        elif curr_col == 6:   # Location
            location = bug.text.strip()
            bugs[curr_bug]['location'] = location
            continue
        
        elif curr_col == 7:   # Time
            active_hours = bug.text.strip()
            bugs[curr_bug]['active_hours'] = active_hours
            continue
        
        elif curr_col == 8:   # Months
            bugs[curr_bug]['months_available'] = {'northern': [], 'southern': []}
            bugs[curr_bug]['months_unavailable'] = {'northern': [], 'southern': []}
            n, s = handle_months(bug)
            
            for k, m in enumerate(months):
                if n[k][1] is True:
                    bugs[curr_bug]['months_available']['northern'].append(m)
                else:
                    bugs[curr_bug]['months_unavailable']['northern'].append(m)
                
                if s[k][1] is True:
                    bugs[curr_bug]['months_available']['southern'].append(m)
                else:
                    bugs[curr_bug]['months_unavailable']['southern'].append(m)
            continue

        elif curr_col == 9:   # Peak
            continue
        
        # elif i >= 10:  # Done with 1st bug (Used for testing purposes)
        #     break

    with concurrent.futures.ThreadPoolExecutor() as executor:
        detail_links = tuple(bug['details_link'] for bug in bugs.values())
        results = executor.map(scrape_quote, detail_links)

        bug_keys = list(bugs)
        for i, result in enumerate(results):
            bugs[bug_keys[i]]['catchquote'] = result

    with open(os.path.join('json', 'bugs.json'), 'w') as f:
        json.dump(bugs, f)


def scrape_sea_creatures():
    source = requests.get("https://nookipedia.com/wiki/Sea_creatures/New_Horizons").text
    soup = BeautifulSoup(source, 'lxml')
    
    table = soup.find('div', class_='mw-collapsible-content').table

    table_cols = [th.text.strip() for th in table.find_all('th')]

    cols = len(table_cols)
    sea_creatures = {}
    
    for i, sea_creature in enumerate(table.find_all('td')):
        curr_col = i%cols

        if curr_col == 0:   # ID
            continue



def handle_months(critter):
    n_month_availability = []
    s_month_availability = []
    for span in critter.span:
        if not span.name:   # Unavailable
            for m in span.strip().split(' '):
                n_month_availability.append((m, False))
        else:               # Available
            for m in span.text.strip().split(' '):
                n_month_availability.append((m, True))
    
    for span in critter.p.span:
        if not span.name:   # Unavailable
            for m in span.strip().split(' '):
                s_month_availability.append((m, False))
        else:               # Available
            for m in span.text.strip().split(' '):
                s_month_availability.append((m, True))
    
    return (n_month_availability, s_month_availability)


def scrape_quote_deprecated(critter_name:str, details_link:str):
    source = requests.get(details_link).text
    soup = BeautifulSoup(source, 'lxml')
    try:
        i = soup.find('i', text='New Horizons')
        return i.find_previous_sibling('i').text.strip()
    except AttributeError as e:
        return 'The catch quote for this critter is not yet available on the wiki. Sorry.'


def scrape_quote(details_link:str):
    source = requests.get(details_link).text
    soup = BeautifulSoup(source, 'lxml')
    try:
        nh_h3 = soup.find('span', id='In_New_Horizons').parent
        nh_div = nh_h3.find_next('div')
        raw_quote = nh_div.p.text.strip()
        quote = raw_quote[1:-1]
        return quote if quote != "" else None
    except:
        return None


async def run_scraper():
    if not os.path.exists('json'):
        os.mkdir('json')

    t0 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor() as executor:
        print('Running "scrape_fish"...')
        f_fish = executor.submit(scrape_fish)
        
        print('Running "scrape_bugs"...')
        f_bugs = executor.submit(scrape_bugs)
    
    t2 = time.perf_counter()
    print('Total time taken:', t2-t0, 'seconds')


if __name__ == '__main__':
    import asyncio
    asyncio.run(run_scraper())