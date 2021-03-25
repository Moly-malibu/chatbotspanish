import numpy as np 
import nltk  # nltk.download('punkt')
import nltk 
import numpy as np
from nltk.stem.porter import PorterStemmer

stemmer = PorterStemmer()

#FUNCTIONS:

# 1. Pass sentences: each words split and  tokenize.
# 2. Stemmer: find root of word.
# 3. Create bag and return array.

def token(sentence):
    return nltk.word_tokenize(sentence) 

def stem(word):
    return stemmer.stem(word.lower())

def bag_words(sentenceToken, words):
    wordsSent = [stem(word) for word in sentenceToken]
    bag = np.zeros(len(words), dtype=np.float32)
    for i, w in enumerate(words):
        if w in wordsSent:
            bag[i] = 1
    return bag