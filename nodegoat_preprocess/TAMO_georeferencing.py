# Need to install libraries to convert NGR/BGN and OS Grid to lat/long: OSGridConverter and pyproj
#need to save the below somewhere because it was kinda slay
    # dms_lat, dms_long = map(str.strip, [x for xs in coordinates for x in xs.split(",")])
#used to separate a string at the comma

import json
import pandas as pd
import re

from OSGridConverter import grid2latlong

def read_json(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

places = read_json("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/Data_Scraping_TAMO/places_geocodes.json")
results = []

#parse place names into standard and alt spellings
def parse_placenames(place_str):
    parts = re.split(r"[\(\,\;\[]", place_str)
    cleaned_str = []

    for part in parts:
        # Strip leading/trailing whitespace
        word = part.strip()

        # Remove unwanted characters at the start or end
        # Allow letters, spaces, and hyphens only
        word = re.sub(r"^[^\w\s\-]+|[^\w\s\-]+$", "", word)

        # Match words that contain letters (including Unicode), spaces, or hyphens
        if re.match(r"^[\w\s\-]+$", word) and any(c.isalpha() for c in word):
            cleaned_str.append(word)
    
    if cleaned_str:
        standard_name = cleaned_str[0]
        alt_spellings = cleaned_str[1:]
    else:
        standard_name = None
        alt_spellings = [] 

    return standard_name, alt_spellings

# transform degree, minute and second location to decimal degrees
def dms_to_dd(d, m, s):
    dd = d + float(m)/60 + float(s)/3600
    return dd

def parse_coords(coords_str):
    coordinates = list(map(int, re.findall(r"\d+", coords_str)))

    if len(coordinates) != 6:
        return None, None
    
    #degree, minute, second
    lat_d, lat_m, lat_s = coordinates[0:3]
    long_d, long_m, long_s = coordinates[3:6]

    #dd = decimal degrees
    lat_dd = dms_to_dd(lat_d, lat_m, lat_s)
    long_dd = dms_to_dd(long_d, long_m, long_s)
    #long = dms_to_dd(dms_long)

    return lat_dd, long_dd

#transform UK Grid referencing to lat/long
def OS_to_latlong(OS_str):
    OS_list = re.findall(r":\s*(.+)", OS_str) #to only capture text after ": + whitespace"

    #below to translate list into string without square brackets
    delimiter = " "
    OS_number = delimiter.join(OS_list)

    l = grid2latlong(OS_number) #not always wholly accurate
    return l.latitude, l.longitude

#iterating over json file
for entry in places:
    standard_name, alt_spellings = parse_placenames(entry["place"])

    if entry.get("ngr"):
        try:
            lat, long = OS_to_latlong(entry["ngr"])
        except Exception as e:
            print(f"Error with NGR '{entry['ngr']}' for place '{entry['place']}': {e}")
    elif entry.get("coords"):
        try:
            lat, long = parse_coords(entry["coords"])
        except Exception as e:
            print(f"Error parsing coords for {entry['place']}: {e}")
    elif entry.get("OS grid"):
        try:
            lat, long = OS_to_latlong(entry["OS grid"])
        except Exception as e:
            print(f"Error at OS Grid {entry["OS grid"]} for place '{entry['place']}': {e} ")

    results.append({
        "standard_name": standard_name,
        "alternate_spellings": alt_spellings,
        "latitude": lat,
        "longitude": long
    })
