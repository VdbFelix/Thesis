#from Mattingly's NER videos
#basic one
def train_spacy(data, iterations):
    TRAIN_DATA = data
    nlp = spacy.blank("en")
    if "ner" not in nlp.pipe_names:
        ner = nlp.create_pipe("ner")
        nlp.add_pipe(ner, last=True)
    for _, annotations in TRAIN_DATA:
        for ent in annotations.get("entities"):
            ner.add_label(ent[2])
    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print ("Starting iteration " + str(itn))
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update(
                            [text],
                            [annotations],
                            drop=0.2,
                            sgd=optimizer,
                            losses=losses
                )
            print (losses)
    return (nlp)

#more detailed one to add custom LABEL and PIPELINE based on TRAINING DATA
def train_spacy(TRAIN_DATA, iterations):
    nlp = spacy.blank("en")
    ner = nlp.create_pipe("ner")
    ner.add_label("CONC_CAMP")
    nlp.add_pipe(ner, name="conc_camp_ner")

    other_pipes = [pipe for pipe in nlp.pipe_names if pipe != "conc_camp_ner"]
    with nlp.disable_pipes(*other_pipes):
        optimizer = nlp.begin_training()
        for itn in range(iterations):
            print (f"Starting iteration {str(itn)}")
            random.shuffle(TRAIN_DATA)
            losses = {}
            for text, annotations in TRAIN_DATA:
                nlp.update( [text],
                            [annotations],
                            drop=0.2,
                            sgd=optimizer,
                            losses=losses

                )
            print (losses)
    return (nlp)

TRAIN_DATA = load_data("data/camp_training_data.json")
random.shuffle(TRAIN_DATA)
TRAIN_DATA = TRAIN_DATA[0:100]

nlp = train_spacy(TRAIN_DATA, 5)


doc = nlp("But you traveled from Lakhva to Lodz with your father. So, when the Germans came to Lakhva, did they form the ghetto immediately?  So, have nothing to do there, and they start the ghetto in Warsaw? And after they start to evacuate the ghetto, to take to Majdanek, to Treblinka, and the peoples they start to know they kill these people. This is the town of Plonsk. Warsaw is also a city in Poland. Pomiechowek is also a city in Poland. The Lakvha ghetto. USHMM Archive. United States Holocaust Memorial Museum. David A. Kochalski, born May 5, 1928 in Poland")
for ent in doc.ents:
    print (ent.text, ent.label_)
