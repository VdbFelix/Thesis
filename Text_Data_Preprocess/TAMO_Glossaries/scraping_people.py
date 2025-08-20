from bs4 import BeautifulSoup
import pandas as pd
import json
import re
import requests

#first scraping from people glossary
df = pd.DataFrame()
names_list = []

def get_names(url):
    response = requests.get(url)
    if response.status_code != 200:
        return None
    
    soup = BeautifulSoup(response.text, "html.parser")

    name_div = soup.find_all("div", class_="apparatus_head1")
    for div in name_div:
        names_list.append(div.text)
        if div is None:
            print("No div found with the specified apapratus_head1 class")

#iterating through url using the alphabet (glossary is organised alphabetically with one page per letter)
for i in range(97, 123):
	get_names(f"https://www.dhi.ac.uk/foxe/index.php?realm=more&gototype=&type=person&letter={chr(i)}")

#turn to dataframe
df["name"] = names_list
df = df.drop_duplicates()

#clean dataframe
def add_names_dataframe(df, column='name'):
    new_rows = []

    for index, row in df.iterrows():
        name_field = row[column]

        #extract bracketed names first
        bracket_match = re.match(r'^(.*?)\s*\(([^)]+)\)\s*$', name_field.strip())
        names_to_process = []

        if bracket_match:
            original_name = bracket_match.group(1).strip()
            alias = bracket_match.group(2).strip()
            names_to_process.extend([original_name, alias])
        else:
            names_to_process.append(name_field.strip())

        #fr each name (including aliases), split on ',', 'and', or 'or'
        for name in names_to_process:
            parts = re.split(r'\s*(?:,| and | or )\s*', name)
            for part in parts:
                if part:
                    new_rows.append({column: part.strip()})

    #create a new DataFrame from cleaned entries
    cleaned_df = pd.DataFrame(new_rows)

    return cleaned_df.reset_index(drop=True)

clean_df.to_csv("name_glossary_fpxe.csv")
