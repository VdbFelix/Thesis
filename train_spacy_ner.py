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
