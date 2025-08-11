from bs4 import BeautifulSoup
import pandas as pd
import re
import requests

df = pd.DataFrame()
places_list = []

def get_places(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    name_div = soup.find_all("div", class_="apparatus_head1")
    for div in name_div:
        places_list.append(div.text)
        if div is None:
            print("No div found with the specified apapratus_head1 class")

for i in range(97, 123):
    get_places(f"https://www.dhi.ac.uk/foxe/index.php?realm=more&gototype=&type=place&letter={chr(i)}")

df["places"] = places_list

def add_places(df, column="places"):
    new_rows = []

    for entry in df[column].dropna():
        # remove all non-letter characters (keep only letters and spaces)
        cleaned = re.sub(r'[^a-zA-Z\\s]', ' ', entry)

        # split into words
        words = cleaned.split()

        # keep only words that start with a capital letter
        for word in words:
            if word[0].isupper():
                new_rows.append({column: word})

    return pd.DataFrame(new_rows).reset_index(drop=True)

clean_df = add_places(df)
clean_df.to_csv("places_glossary_foxe.csv")
