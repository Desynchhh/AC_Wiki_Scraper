from bs4 import BeautifulSoup
import requests, json, os
#asyncio

base_url = "https://nookipedia.com"
months = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')

async def scrape_fish():
    source = requests.get("https://nookipedia.com/wiki/Fish/New_Horizons").text
    soup = BeautifulSoup(source, 'lxml')

    table = soup.find('div', class_='mw-collapsible-content').table

    table_cols = [th.text.strip() for th in table.find_all('th')]

    cols = len(table_cols)
    fishes = {}

    for i, fish in enumerate(table.find_all('td')):
        curr_col = i%cols

        # if curr_col == 0:   # ID
        #     pass
        
        if curr_col == 1:   # Name
            name = fish.a.text.strip()
            curr_fish = name.lower()
            details_link = base_url + fish.a.get('href')
            quote = await scrape_quote(name, details_link)
            fishes[curr_fish] = {
                'name': name,
                'details_link': details_link,
                'catchquote': quote
            }
        # if curr_col == 2:   # Img
        #     pass
        
        if curr_col == 3:   # Price
            price = int(fish.text.strip().replace(',',''))
            fishes[curr_fish]['nook_price'] = price
            fishes[curr_fish]['cj_price'] = int(price*1.5)
        
        if curr_col == 4:   # Shadow
            shadow = fish.text.strip()
            fishes[curr_fish]['shadow_size'] = shadow
        
        # if curr_col == 5:   # Size
        #     pass
        
        # if curr_col == 6:   # Tank
        #     pass
        
        if curr_col == 7:   # Location
            location = fish.a.text.strip()
            fishes[curr_fish]['location'] = location
        
        if curr_col == 8:   # Time
            active_hours = fish.text.strip()
            fishes[curr_fish]['active_hours'] = active_hours
        
        if curr_col == 9:   # Months
            fishes[curr_fish]['months_available'] = {'northern': [], 'southern': []}
            fishes[curr_fish]['months_unavailable'] = {'northern': [], 'southern': []}
            n, s = await handle_months(fish)
            
            for k, m in enumerate(months):
                if n[k][1] is True:
                    fishes[curr_fish]['months_available']['northern'].append(m)
                else:
                    fishes[curr_fish]['months_unavailable']['northern'].append(m)
                
                if s[k][1] is True:
                    fishes[curr_fish]['months_available']['southern'].append(m)
                else:
                    fishes[curr_fish]['months_unavailable']['southern'].append(m)

        # if curr_col == 10:   # Peak
        #     pass
        
        # if i >= 11:  # Done with 1st fish (Used for testing purposes)
        #     break

    with open(os.path.join('json', 'fish.json'), 'w') as f:
        json.dump(fishes, f)


async def scrape_bugs():
    source = requests.get("https://nookipedia.com/wiki/Bugs/New_Horizons").text
    soup = BeautifulSoup(source, 'lxml')

    table = soup.find('div', class_='mw-collapsible-content').table

    table_cols = [th.text.strip() for th in table.find_all('th')]

    cols = len(table_cols)
    bugs = {}

    for i, bug in enumerate(table.find_all('td')):
        curr_col = i%cols

        # if curr_col == 0:   # ID
        #     pass
        
        if curr_col == 1:   # Name
            name = bug.a.text.strip()
            curr_bug = name.lower()
            details_link = base_url + bug.a.get('href')
            quote = await scrape_quote(name, details_link)
            bugs[curr_bug] = {
                'name': name,
                'details_link': details_link,
                'catchquote': quote
            }
        # if curr_col == 2:   # Img
        #     pass
        
        if curr_col == 3:   # Price
            price = int(bug.text.strip().replace(',',''))
            bugs[curr_bug]['nook_price'] = price
            bugs[curr_bug]['flick_price'] = int(price*1.5)
        
        if curr_col == 4:   # Rarity
            rarity = bug.text.strip()
            bugs[curr_bug]['rarity'] = rarity
        
        # if curr_col == 5:   # Size
        #     pass
        
        if curr_col == 6:   # Location
            location = bug.text.strip()
            bugs[curr_bug]['location'] = location
        
        if curr_col == 7:   # Time
            active_hours = bug.text.strip()
            bugs[curr_bug]['active_hours'] = active_hours
        
        if curr_col == 8:   # Months
            bugs[curr_bug]['months_available'] = {'northern': [], 'southern': []}
            bugs[curr_bug]['months_unavailable'] = {'northern': [], 'southern': []}
            n, s = await handle_months(bug)
            
            for k, m in enumerate(months):
                if n[k][1] is True:
                    bugs[curr_bug]['months_available']['northern'].append(m)
                else:
                    bugs[curr_bug]['months_unavailable']['northern'].append(m)
                
                if s[k][1] is True:
                    bugs[curr_bug]['months_available']['southern'].append(m)
                else:
                    bugs[curr_bug]['months_unavailable']['southern'].append(m)

        # if curr_col == 9:   # Peak
        #     pass
        
        # if i >= 10:  # Done with 1st bug (Used for testing purposes)
        #     break

    with open(os.path.join('json', 'bugs.json'), 'w') as f:
        json.dump(bugs, f)


async def handle_months(critter):
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


async def scrape_quote(critter_name:str, details_link:str):
    source = requests.get(details_link).text
    soup = BeautifulSoup(source, 'lxml')
    try:
        i = soup.find('i', text='New Horizons')
        return i.find_previous_sibling('i').text.strip()
    except AttributeError as e:
        return 'The catch quote for this critter is not yet available on the wiki. Sorry.'


async def run_scraper():
    await scrape_fish()
    await scrape_bugs()

# asyncio.run(run_scraper())