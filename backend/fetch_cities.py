import requests
from bs4 import BeautifulSoup
import json
import os

def fetch_us_cities():
    url = "https://www.craigslist.org/about/sites"
    print(f"Fetching {url}...")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()
    except Exception as e:
        print(f"Failed to fetch sites: {e}")
        return

    soup = BeautifulSoup(response.content, 'html.parser')
    
    # The page is structured with headers for continents/countries.
    # We want "US"
    # Structure: div.colmask -> div.box -> h4 (Country) -> ul -> li -> a
    
    cities = []
    
    # Locate the US section. This is often heuristic as the page structure varies.
    # We'll look for the map/list container. 
    # Usually, the first "h4" in the columns is US states or regions.
    
    # Let's iterate through all links and filter by simple heuristics or grab specific containers
    # Better: The US section is usually the first big block.
    
    # Getting all links in the main content area
    colmask = soup.select_one(".colmask")
    if not colmask:
        print("Could not find .colmask")
        return

    # In colmask, there are multiple 'box' divs. 
    # We need to find the one associated with "United States" or just grab all known US-looking matches.
    # Actually, the page structure is: <h1>cl > about > sites</h1> ... then columns.
    # The US list is typically spread across the first few columns.
    
    # Let's just grab ALL site links and filter them? 
    # Or parsing the H4s.
    
    boxes = colmask.select(".box")
    for box in boxes:
        # Check if this box is for US. 
        # Often it just has H4s for States (Alabama, Alaska...). 
        # If headers are US states, it's US.
        h4s = box.select("h4")
        if not h4s:
            continue
            
        first_header = h4s[0].text.strip()
        # Heuristic: If header is 'Alabama' or 'California', it's US. 
        # If it's 'Asia', 'Europe', it's not.
        # Quick list of some states to check
        us_indicators = ['Alabama', 'California', 'Florida', 'New York', 'Texas', 'Washington']
        
        is_us = False
        for head in h4s:
            if head.text.strip() in us_indicators:
                is_us = True
                break
        
        # Another check: US URLs usually end in .org, non-US often .org too but different paths.
        # Actually simplest way: US craigslist subdomains are just `city.craigslist.org`.
        
        if is_us or any(h.text in ['Alabama', 'Alaska', 'Arizona'] for h in h4s):
            links = box.select("a")
            for link in links:
                href = link.get('href', '')
                text = link.text.strip()
                
                # extracting subdomain: https://sfbay.craigslist.org/ -> sfbay
                if 'craigslist.org' in href and '//' in href:
                    parts = href.split('//')[1].split('.')
                    subdomain = parts[0]
                    
                    # exclude 'www' or others if necessary, but sites lists usually direct to subdomains
                    if subdomain and subdomain != 'www':
                        cities.append({"label": text, "value": subdomain})

    # Sort alphabet
    cities.sort(key=lambda x: x['label'])
    
    # Save to frontend data dir
    output_path = '/app/src/data/cities.json' # Container path
    # If running locally for test:
    if not os.path.exists('/app'):
        output_path = 'frontend/src/data/cities.json'

    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    
    with open(output_path, 'w') as f:
        json.dump(cities, f, indent=2)
    
    print(f"Saved {len(cities)} cities to {output_path}")

if __name__ == "__main__":
    fetch_us_cities()
