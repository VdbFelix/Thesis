#This code will be used to load 1563, 1570, and 1576, clean them, and prepare a corpus for word vectorisation with Gensim

import re
import glob
import os

#loading all eds in one variable

def load_txt_files(directory):
    file_paths = glob.glob(os.path.join(directory, "*.txt"))

    txt_files = []
    for file in file_paths:
        with open(file, "r", encoding="utf-8") as f:
            txt_files.append(f.read())
    return txt_files

txt_1563 = load_txt_files("your_1563_directory")
txt_1570 = load_txt_files("your_1570_directory")
txt_1576 = load_txt_files("your_1576_directory")

corpus = txt_1563 + txt_1570 + txt_1576
print(corpus[:100])

#Cleaning the corpus
#add a space after a period where a period is followed by a capital letter such as them.However
corpus = re.sub(r'(?<=[a-z])\.(?=[A-Z])', '. ', corpus)
print(corpus[:100])
# Remove periods after single capital letters if followed by a capital word such as M. Hopkins
corpus = re.sub(r"\b([A-Z])\.(?=\s+[A-Z])", r"\1", corpus)

#Custom stop word list

stop_words = ["i","me","my","myself","we","our","ours","ourselves","you","your","yours","yourself","yourselves",
             "he","him","his","himself","she","her","hers","herself","it","its","itself","they","them","their",
             "theirs","themselves","what","which","who","whom","this","that","these","those","am","is","are","was",
             "were","be","been","being","have","has","had","having","do","does","did","doing","a","an","the","and",
             "but","if","or","because","as","until","while","of","at","by","for","with","about","against","between",
             "into","through","during","before","after","above","below","to","from","up","down","in","out","on","off",
             "over","under","again","further","then","once","here","there","when","where","why","how","all","any","both",
             "each","few","more","most","other","some","such","no","nor","not","only","own","same","so","I", "Me", "My", "Myself", "We", "Our", "Ours", "Ourselves", "You", "Your", "Yours", "Yourself", "Yourselves",
 "He", "Him", "His", "Himself", "She", "Her", "Hers", "Herself", "It", "Its", "Itself", "They", "Them", "Their",
 "Theirs", "Themselves", "What", "Which", "Who", "Whom", "This", "That", "These", "Those", "Am", "Is", "Are", "Was",
 "Were", "Be", "Been", "Being", "Have", "Has", "Had", "Having", "Do", "Does", "Did", "Doing", "A", "An", "The", "And",
 "But", "If", "Or", "Because", "As", "Until", "While", "Of", "At", "By", "For", "With", "About", "Against", "Between",
 "Into", "Through", "During", "Before", "After", "Above", "Below", "To", "From", "Up", "Down", "In", "Out", "On", "Off",
 "Over", "Under", "Again", "Further", "Then", "Once", "Here", "There", "When", "Where", "Why", "How", "All", "Any", "Both",
 "Each", "Few", "More", "Most", "Other", "Some", "Such", "No", "Nor", "Not", "Only", "Own", "Same", "So"
"than","too","very","s","t","can","will","just","don","should","now", "thē", "thā", "bene", "wich", "ourselues", "yourselues", "vve",
             "themselues", "haue", "dont", "&", "&amp", "amp", "amp&", "art", "thou", "thy", "and", "In", "The", "Thē",
             "Them", "Then", "That", "I", "We", "You", "They", "He", "His", "Is", "During", "duringe","By", "Now", "Thou",
             "A", "Where", "Were", "Be", "Can", "Haue", "Have", "Again", "Between", "Of", "ye", "whiche", "upon",
             "vpon", "hys", "þe", "us", "vs"]


words = corpus.split()

new_corpus = []
for word in words:
    if word not in stop_words:
        new_corpus.append(word)

corpus = " ".join(new_corpus)

print(len(corpus))

def save_txt(text, file):
    with open(file, "w", encoding="utf-8") as f:
        f.write(str(text))

save_txt(corpus, "foxe_w2vec_corpus.txt")
