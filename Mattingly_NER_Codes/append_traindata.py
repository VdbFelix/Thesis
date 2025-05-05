import spacy

nlp = spacy.load("en_core_web_sm")
text = "Treblinka is a small village in Poland. Wikipedia notes that Treblinka is not large."
corpus = []

doc = nlp(text)
for sent in doc.sents:
    corpus.append(sent.text)

nlp = spacy.blank("en")

ruler = nlp.add_pipe("entity_ruler")

patterns = [
                {"label": "GPE", "pattern": "Treblinka"}
            ]

ruler.add_patterns(patterns)

TRAIN_DATA = []
for sentence in corpus:
    doc = nlp(sentence)
    entities = []

    for ent in doc.ents:
        entities.append([ent.start_char, ent.end_char, ent.label_])
    TRAIN_DATA.append([sentence, {"entities": entities}])

print (TRAIN_DATA)
