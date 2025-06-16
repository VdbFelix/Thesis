import spacy
import re
import string
import gensim

def load_data(file):
    with open(file, "r", encoding="utf-8") as f:
        data = f.read()
    return data

corpus = load_data("/Users/felixvdb/Desktop/DigHum/Thesis/Foxe_Thesis_Codes/Training Dataset/TRAINING CODE/foxe_w2vec_corpus.txt")

#Because corpus is too long, need to chunk the text
import string
nlp = spacy.load("en_core_web_sm")

def chunk_text(text, max_chars=1_000_000):
    for i in range(0, len(text), max_chars):
        yield text[i:i + max_chars]

#now tokenise sentences and words, delete puncutation
corpus_sentences = []
for chunk in chunk_text(corpus):
    doc = nlp(chunk)
    for sent in doc.sents:
        sentence = sent.text.translate(str.maketrans("", "", string.punctuation))
        words = sentence.split()
        corpus_sentences.append(words)

#Create word vectors (from mattingly)
def create_wordvecs(corpus, model_name):
    from gensim.models.word2vec import Word2Vec
    from gensim.models.phrases import Phrases, Phraser
    from collections import defaultdict
    
    print (len(corpus))
    

    phrases = Phrases(corpus, min_count=30, progress_per=10000)
    print ("Made Phrases")
    
    bigram = Phraser(phrases)
    print ("Made Bigrams")
    
    sentences = phrases[corpus]
    print ("Found sentences")
    word_freq = defaultdict(int)

    for sent in sentences:
        for i in sent:
            word_freq[i]+=1

    print (len(word_freq))
    
    print ("Training model now...")
    w2v_model = Word2Vec(min_count=1,
                        window=2,
                        vector_size=10,
                        sample=6e-5,
                        alpha=0.03,
                        min_alpha=0.0007,
                        negative=20)
    w2v_model.build_vocab(sentences, progress_per=10000)
    w2v_model.train(sentences, total_examples=w2v_model.corpus_count, epochs=30, report_delay=1)
    w2v_model.wv.save_word2vec_format(f"{model_name}.txt")
    
create_wordvecs(corpus_sentences, "word_vecs")

#check word vectors
with open("word_vecs.txt", "r") as f:
    data = f.readlines()
    print(data[1])
