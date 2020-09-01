import collections
import numpy as np
from keras.preprocessing.text import text_to_word_sequence
from keras_preprocessing.sequence import pad_sequences
from keras.utils.np_utils import to_categorical
from keras.models import Sequential, load_model
from keras.layers import LSTM, Dense, Embedding
from keras.preprocessing.text import Tokenizer
from keras.optimizers import RMSprop
import tokenize
import pickle
import re
from keras.layers import LSTM, Dense, Embedding
import tensorflow as tf


def load_object(filename):
    infile = open(filename, 'rb')
    obj = pickle.load(infile)
    infile.close()
    return obj
#if text empty return the (top_n-1) occurrence words
model=None
def fillModel():
    global model
    model = load_model('Resources/Prediction/keras_next_word_model.h5')

def predict_next_word(input_text,top_n=6):
    # not tested
    if len(input_text)==0:
        word_dict=load_object("Resources/Prediction/word_dict")
        sug=[]

        for x in dict(collections.Counter(word_dict).most_common(top_n)):
            if x != 'â':
                sug.append(x)
        return sug
    input_text="emp emp emp "+input_text
    tokenizer=load_object("Resources/Prediction/tokenizer.pkl")
    seq_len = load_object("Resources/Prediction/seq_len.pkl")
    encoded_text = tokenizer.texts_to_sequences([input_text])[0]
    pad_encoded = pad_sequences([encoded_text], maxlen=seq_len, truncating='pre')

    suggestion=[]
    #print("holla")
    classes=model.predict(pad_encoded)
    #print("holla")
    for i in (classes[0]).argsort()[-top_n:][::-1]:
        pred_word = tokenizer.index_word[i]
        if pred_word !='â':
            suggestion.append(pred_word)
    return suggestion [:top_n-1]

# spell checking
def train(features):
    pred_words = collections.defaultdict(lambda: 1)
    for f in features:
        pred_words[f] += 1
    return pred_words

# spell checking 1 edit away from the word
def edits1(pred_word):
    alphabet = 'abcdefghijklmnopqrstuvwxyz'
    s = [(pred_word[:i], pred_word[i:]) for i in range(len(pred_word) + 1)]
    deletes    = [a + b[1:] for a, b in s if b]
    transposes = [a + b[1] + b[0] + b[2:] for a, b in s if len(b)>1]
    replaces   = [a + c + b[1:] for a, b in s for c in alphabet if b]
    inserts    = [a + c + b     for a, b in s for c in alphabet]
    return set(deletes + transposes + replaces + inserts)

#spell checking 2 edits away
def known_edits2(word,NWORDS):
    return set(e2 for e1 in edits1(word) for e2 in edits1(e1) if e2 in NWORDS)

#existing word
def known(words,NWORDS):
    return set(w for w in words if w in NWORDS)

# check 1 edit, 2 edits, alreay exist
def correct(word,NWORDS):
    candidates = known([word],NWORDS) or known(edits1(word),NWORDS) or known_edits2(word,NWORDS) or [word]
    return max(candidates, key=NWORDS.get)

# get predict_next_word for the previous text
# return top 4 form them
# then check if it already exist or 1/2 edits away from the rest
# of the words generated from predict_next_word
def predict_current_word(input_text):
    input_text = re.sub("[^0-9a-zA-Z]+", " ", input_text)
    input_text=input_text.lower()
    if input_text[0]==' ':
        input_text=input_text[1:]
    last_word=input_text.split()[-1]
    input_text=' '.join(input_text.split()[:-1])
    top_n=10
    suggestion=predict_next_word(input_text,top_n+1)

    NWORDS=train(suggestion[4:])
    new_last_word=correct(last_word,NWORDS)
    sug = [new_last_word]+suggestion[:4]
    return sug

#state =1 predict current word
#state =0 predict next word
def predict_word(input_text,state=False):
    if state==1:
        return predict_current_word(input_text)
    return predict_next_word(input_text)

if __name__ == '__main__':
    #predict_word take the text
    #and a bool state
    # True if you want to predict the current word
    # False if you want to predict the next word
    # build_model()
    fillModel()
    print(predict_word("the old man had ben", True))