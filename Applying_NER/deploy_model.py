import spacy
import pandas as pd
import os

text_dir = "your_directory"
model = "path_to_your_model"

nlp = spacy.load(model)

# prepare storage
entity_to_id = {}
next_id = 1
records = []

for filename in os.listdir(text_dir):
    # parse book and file numbers from filenames =
    _, book_str, file_str_with_ext = filename.split("_")
    file_str = file_str_with_ext.replace(".txt", "")
    book_num = int(book_str)
    file_num = int(file_str)

    with open(os.path.join(text_dir, filename), "r", encoding="utf-8") as f:
        text = f.read()

    doc = nlp(text)

    # count entities in given document
    counts = {}
    for ent in doc.ents:
        key = (ent.text, ent.label_)
        counts[key] = counts.get(key, 0) + 1
    
    # create records
    for (ent_text, ent_label), count in counts.items():
        # assign or retrieve unique ID
        if (ent_text, ent_label) not in entity_to_id:
            entity_to_id[(ent_text, ent_label)] = next_id
            next_id += 1
        ent_id = entity_to_id[(ent_text, ent_label)]
        
        records.append({
            "Book": book_num,
            "File": file_num,
            "Entity type": ent_label,
            "Entity text": ent_text,
            "ID": ent_id,
            "Count in File": count
        })

df = pd.DataFrame(records, columns=["Book", "File", "Entity type", "Entity text", "ID", "Count in File"])

df.to_csv("foxe_database.csv")
