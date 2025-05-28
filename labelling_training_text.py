import csv
import re
import json
import pandas as pd
import spacy

def load_json(file):
    with open(file, "r", encoding="utf-8") as f:
        data = json.load(f)
    return (data)

def save_json(file, data):
    with open (file, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=True)

def clean_text(file):
    file = file.replace(".", " ")
    return re.sub(r"[^\w\s]", "", file)
#note that this function serves specifically to clean the JOSN strings by replacing periods by spaces

def clean_json_strings(obj):
    if isinstance(obj, dict):
        return {k: clean_json_strings(v) for k, v in obj.items()}
    elif isinstance(obj, list):
        return [clean_json_strings(item) for item in obj]
    elif isinstance(obj, str):
        return clean_text(obj)
    else:
        return obj

def clean_csv(text):
    return re.sub(r"[^\w\s]", "", text)
  
#training_1563 = load_json("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/training_1563.json")
#training_1563 = clean_json_strings(training_1563)
#save_json("training_1563_clean.json", training_1563)

#training_1570 = load_json("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/training_1570.json")
#training_1570 = clean_json_strings(training_1570)
#save_json("training_1570_clean.json", training_1570)

#training_1576 = load_json("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/training_1576.json")
#training_1576 = clean_json_strings(training_1576)
#save_json("training_1576_clean.json", training_1576)

#Foxe_PERSON = pd.read_csv("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/TRAINING CODE/Foxe_PERSON.csv"\
                          #, header=None, names=["text"])
#Foxe_PERSON["text"] = Foxe_PERSON["text"].apply(clean_csv)
#Foxe_PERSON.to_csv("Foxe_PERSON_clean.csv", index=False, header=False)

#Foxe_PLACES = pd.read_csv("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/TRAINING CODE/Foxe_PLACES.csv"\
                          #, header=None, names=["text"])
#Foxe_PLACES["text"] = Foxe_PLACES["text"].apply(clean_csv)
#Foxe_PLACES.to_csv("Foxe_PLACES_clean.csv", index=False, header=False)

Foxe_PERSON = pd.read_csv("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/TRAINING CODE/Foxe_PERSON_clean.csv", header=None, names=["entity"])
Foxe_PERSON["label"] = "PERSON"

Foxe_PLACE = pd.read_csv("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/TRAINING CODE/Foxe_PLACES_clean.csv", header=None, names=["entity"])
Foxe_PLACE["label"] = "PLACE"

Foxe_NORP = pd.read_csv("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/TRAINING CODE/Foxe_NORP.csv", header=None, names=["entity"])
Foxe_NORP["label"] = "NORP"

Foxe_labels = pd.concat([Foxe_PERSON, Foxe_PLACE, Foxe_NORP], ignore_index=True)
Foxe_labels.drop_duplicates()

patterns = [{"label": row["label"], "pattern": row["entity"]} for _, row in Foxe_labels.iterrows()]
patterns.append({"label": "YEAR", "pattern": [{"TEXT": {"REGEX": r"\b\d{3,4}\b"}}]})
#NB: cannot combine DF patterns list with manually-defined rule in one string, hence patterns.append()
print(patterns[0])

#save_json("NER_patterns.json", patterns)

nlp = spacy.blank("en") #load blank model
ruler = nlp.add_pipe("entity_ruler") #create entity ruler
ruler.add_patterns(patterns) #adding patterns

training_corpus = load_json("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/TRAINING CODE/training_text_merged.json")

corpus = []
for item in training_corpus:
    doc = nlp(item["content"])
    corpus.append(doc)

TRAIN_DATA = []

#careful not to repeat doc object
for doc in corpus:
    entities= []
    for ent in doc.ents:
        entities.append([ent.start_char, ent.end_char, ent.label_])
    TRAIN_DATA.append([doc.text, {"entities": entities}])

#now to train and save the model
import srsly
import typer
import warnings
from pathlib import Path
from tqdm import tqdm 

from spacy.tokens import DocBin
#mattingly function
def create_training_data(TRAIN_DATA):
    db = DocBin()
    for text, annot in tqdm(TRAIN_DATA):
        doc = nlp.make_doc(text)
        ents = []
        for start, end, label in annot["entities"]:
            span = doc.char_span(start, end, label=label)
            if span is None:
                print("SKipping entity")
            else:
                ents.append(span)
        doc.ents = ents
        db.add(doc)
    return (db)

db = create_training_data(TRAIN_DATA=TRAIN_DATA)
db.to_disk("foxe_ner_model.spacy")
