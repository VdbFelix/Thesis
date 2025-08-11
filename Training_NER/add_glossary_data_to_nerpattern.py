import json
import pandas as pd

def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def save_json(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=True)

glossary_names = pd.read_csv("your_file.csv")
glossary_names["label"] = "PERSON"

glossary_places = pd.read_csv("your_file.csv")
glossary_places["label"] = "PLACE"

glossary_labels = pd.concat([glossary_names, glossary_places], ignore_index=False)
#glossary_places.drop_duplicates()
glossary_labels["entity"] = glossary_labels["name"].combine_first(glossary_labels["places"])

glossary_labels = glossary_labels.drop(["Unnamed: 0","name", "places"], axis=1)
glossary_labels = glossary_labels.drop_duplicates()

import re

def remove_whitespace(text):
    return re.sub(r"^\s+|\s+$", "", text)

def remove_punctuation(text):
    return re.sub(r'[^\w\s]', "", text)

glossary_labels["entity"] = glossary_labels["entity"].apply(remove_whitespace)
glossary_labels["entity"] = glossary_labels["entity"].apply(remove_punctuation)

#turn into json and combine with existing NER patterns
glossary_patterns = [{"label": row["label"], "pattern": row["entity"]} for _, row in glossary_labels.iterrows()]

with open("existing_patterns.json",\
           "r", encoding="utf-8") as f:
    ner_patterns = json.load(f)

ner_patterns.extend(glossary_patterns)
len(ner_patterns) #to verify it worked

#remove duplicates
seen_patterns = set()
unique_data = []

for entry in ner_patterns:
    pattern = entry['pattern']
    if pattern not in seen_patterns:
        unique_data.append(entry)
        seen_patterns.add(pattern)

save_json("NER_extended_patterns.json", unique_data)
