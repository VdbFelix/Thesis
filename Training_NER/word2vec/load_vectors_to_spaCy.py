import spacy
import json
from gensim.models import KeyedVectors

nlp = spacy.blank("en") #load blank model

vectors = KeyedVectors.load_word2vec_format("word_vecs2.txt", binary=False) #load vectors

#loading vectors into nlp
for word in vectors.key_to_index:
    nlp.vocab.set_vector(word, vectors[word])

#checking that vector size is correct (here, 100)
print(nlp.vocab.vectors_length)

#saving vectors
nlp.vocab.vectors.to_disk("foxe_ner_vec_model.spacy")

#This creates a folder called "foxe_ner_vec_model.spacy". However, to turn this into a binary readable .spacy object, 
# you need to run the following in the command line. 
! python -m spacy init vectors en vectors.txt output_path/vectors.spacy

#Then, we follow Mattingly as normal, creating a base config. cfg in which we declare our vectors, then a config.cfg 
# and finally we train the model 
