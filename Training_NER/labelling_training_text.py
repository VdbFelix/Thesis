import re
import pandas as pd
import json
import spacy

def load_json(file):
    with open (file, "r", encoding="utf-8) as f:
             data = json.load(f)
    return data

#transform CSV of labels to NER patterns

Foxe_PERSON = pd.read_csv("your_data", header=None, names=["entity"])
Foxe_PERSON["label"] = "PERSON"

Foxe_PLACE = pd.read_csv("your_data", header=None, names=["entity"])
Foxe_PLACE["label"] = "PLACE"

Foxe_NORP = pd.read_csv("your_data", header=None, names=["entity"])
Foxe_NORP["label"] = "NORP"

Foxe_labels = pd.concat([Foxe_PERSON, Foxe_PLACE, Foxe_NORP], ignore_index=True)
Foxe_labels.drop_duplicates()

patterns = [{"label": row["label"], "pattern": row["entity"]} for _, row in Foxe_labels.iterrows()]
patterns.append({"label": "YEAR", "pattern": [{"TEXT": {"REGEX": r"\b\d{3,4}\b"}}]})
#NB: cannot combine DF patterns list with manually-defined rule in one string, hence patterns.append()
print(patterns[0])

#save patterns to JSON format
save_json("NER_patterns.json", patterns)

nlp = spacy.blank("en") #load blank model
ruler = nlp.add_pipe("entity_ruler") #create entity ruler
ruler.add_patterns(patterns) #adding patterns

training_corpus = load_json("your_data.json")

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

#now to train and save the model - see Mattingly
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
