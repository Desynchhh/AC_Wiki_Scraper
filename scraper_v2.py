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

        elif curr_col == 4:   # Shadow
            shadow = fish.img['alt']
            fishes[curr_fish]['shadow_size'] = shadow

        elif curr_col == 5:   # Location
            location = fish.a.text.strip()
            fishes[curr_fish]['location'] = location

        elif curr_col == 6:   # Time
            active_hours = fish.text.strip()
            fishes[curr_fish]['active_hours'] = active_hours

        elif curr_col == 7:   # Months
            fishes[curr_fish]['months_available'] = {'northern': [], 'southern': []}
            fishes[curr_fish]['months_unavailable'] = {'northern': [], 'southern': []}
            n, s = handle_months(fish)

            for month_number, month in enumerate(months):
                if n[month_number] is True:
                    fishes[curr_fish]['months_available']['northern'].append(month)
                else:
                    fishes[curr_fish]['months_unavailable']['northern'].append(month)

                if s[month_number] is True:
                    fishes[curr_fish]['months_available']['southern'].append(month)
                else:
                    fishes[curr_fish]['months_unavailable']['southern'].append(month)

        elif curr_col == 8:    # Rarity
            rarity = fish.text.strip()
            fishes[curr_fish]['rarity'] = rarity

        elif curr_col == 9:    # Total Catches
            total_catches = fish.text.strip()
            fishes[curr_fish]['total_catches'] = total_catches

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

        elif curr_col == 2:   # Img        
            continue

        elif curr_col == 3:   # Price
            raw_price = bug.text.strip()
            price = int(re.sub(r'\D', '', raw_price))
            bugs[curr_bug]['nook_price'] = price
            bugs[curr_bug]['flick_price'] = int(price*1.5)

        elif curr_col == 4:   # Location
            location = bug.text.strip()
            bugs[curr_bug]['location'] = location

        elif curr_col == 5:   # Time
            active_hours = bug.text.strip()
            bugs[curr_bug]['active_hours'] = active_hours

        elif curr_col == 6:   # Months
            bugs[curr_bug]['months_available'] = {'northern': [], 'southern': []}
            bugs[curr_bug]['months_unavailable'] = {'northern': [], 'southern': []}
            n, s = handle_months(bug)

            for k, m in enumerate(months):
                if n[k] is True:
                    bugs[curr_bug]['months_available']['northern'].append(m)
                else:
                    bugs[curr_bug]['months_unavailable']['northern'].append(m)

                if s[k] is True:
                    bugs[curr_bug]['months_available']['southern'].append(m)
                else:
                    bugs[curr_bug]['months_unavailable']['southern'].append(m)

        elif curr_col == 7:   # Rarity
            rarity = bug.text.strip()
            bugs[curr_bug]['rarity'] = rarity

        elif curr_col == 8:   # Total catches required
            total_catches = bug.text.strip()
            bugs[curr_bug]['total_catches'] = total_catches

        # if i >= 8:  # Done with 1st bug (Used for testing purposes)
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

        elif curr_col == 1: # Name
            name = sea_creature.text.strip()
            curr_sc = name.lower()
            details_link = base_url + sea_creature.a.get('href')
            sea_creatures[curr_sc] = {
                "name": name,
                "details_link": details_link
            }

        elif curr_col == 2: # Image
            continue

        elif curr_col == 3: # Price
            raw_price = sea_creature.text.strip()
            price = int(re.sub(r'\D', '', raw_price))
            sea_creatures[curr_sc]['nook_price'] = price

        elif curr_col == 4: # Size
            size = sea_creature.text.strip()
            sea_creatures[curr_sc]['shadow_size'] = size

        elif curr_col == 5: # Movement
            movement = sea_creature.text.strip()
            sea_creatures[curr_sc]['shadow_movement'] = movement

        elif curr_col == 6: # Time
            time = sea_creature.text.strip()
            sea_creatures[curr_sc]['active_hours'] = time

        elif curr_col == 7: # Months
            sea_creatures[curr_sc]['months_available'] = {'northern': [], 'southern': []}
            sea_creatures[curr_sc]['months_unavailable'] = {'northern': [], 'southern': []}
            n, s = handle_months(sea_creature)

            for k, m in enumerate(months):
                if n[k] is True:
                    sea_creatures[curr_sc]['months_available']['northern'].append(m)
                else:
                    sea_creatures[curr_sc]['months_unavailable']['northern'].append(m)

                if s[k] is True:
                    sea_creatures[curr_sc]['months_available']['southern'].append(m)
                else:
                    sea_creatures[curr_sc]['months_unavailable']['southern'].append(m)

        elif curr_col == 8: # Total catches
            total_catches = sea_creature.text.strip()
            sea_creatures[curr_sc]['total_catches'] = total_catches

        # if i >= 9:   # Done with 1st sea creature (Used for testing purposes)
        #     break

    with concurrent.futures.ThreadPoolExecutor() as executor:
        detail_links = tuple(sea_creature['details_link'] for sea_creature in sea_creatures.values())
        results = executor.map(scrape_quote, detail_links)

        sea_creature_keys = list(sea_creatures)
        for i, result in enumerate(results):
            sea_creatures[sea_creature_keys[i]]['catchquote'] = result

    with open(os.path.join('json', 'seacreatures.json'), 'w') as f:
        json.dump(sea_creatures, f)



def handle_months(critter):
    n_month_availability = []
    s_month_availability = []

    n_spans = critter.span.find_all('span')
    s_spans = critter.p.span.find_all('span')
    
    for span in n_spans:
        n_month_availability.append('font-weight' in span['style'])
    for span in s_spans:
        s_month_availability.append('font-weight' in span['style'])

    return (n_month_availability, s_month_availability)


def scrape_quote(details_link:str):
    source = requests.get(details_link).text
    soup = BeautifulSoup(source, 'lxml')
    try:
        nh_h3 = soup.find('span', id='In_New_Horizons').parent
        nh_div = nh_h3.find_next('div')
        raw_quote = nh_div.p.i.text.strip()
        quote = raw_quote[1:-1]
        return quote if quote != "" else None
    except:
        return None


async def run_scraper():
    if not os.path.exists('json'):
        os.mkdir('json')

    t0 = time.perf_counter()

    funcs_to_run = (scrape_fish, scrape_bugs, scrape_sea_creatures)


    with concurrent.futures.ThreadPoolExecutor() as executor:
        executor.map(lambda x: x(), funcs_to_run)

    t2 = time.perf_counter()
    print('Total time taken:', t2-t0, 'seconds')


if __name__ == '__main__':
    import asyncio
    asyncio.run(run_scraper())