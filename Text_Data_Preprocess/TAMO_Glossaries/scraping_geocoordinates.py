from bs4 import BeautifulSoup
import requests
import json

places_list = []

def extract_places_geocodes(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    for item in soup.find_all("div", class_="apparatus_item"):
        place = item.find("div", class_="apparatus_head1")
        ngr = item.find("div", class_="apparatus_head2", string=lambda s: s and s.startswith("NGR"))

        paragraphs = item.find_all("p")
        coords = next((p.get_text(strip=True) for p in paragraphs if p.text.startswith("Coordinates")), None)
        os_grid = next((p.get_text(strip=True) for p in paragraphs if p.text.startswith("OS grid ref")), None)

        places_list.append({
            "place": place.get_text(strip=True) if place else None,
            "ngr": ngr.get_text(strip=True) if ngr else None,
            "coords": coords if coords else None,
            "OS grid": os_grid if os_grid else None
        })

    return places_list

for i in range(97, 123):
    extract_places_geocodes(f"https://www.dhi.ac.uk/foxe/index.php?realm=more&gototype=&type=place&letter={chr(i)}")

def write_json(file, data):
    with open(file, "w", ) as f:
        json.dump(data, f, indent=4)

write_json("places_geocodes.json", places_list)
